import tensorflow as tf
from tensorflow.keras import backend as K
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, Dense, Flatten
from tensorflow.keras.callbacks import TensorBoard
from tensorflow.keras.optimizers import Adam

# imports we know we'll need
import skopt
from skopt import gbrt_minimize, gp_minimize
from skopt.utils import use_named_args
from skopt.space import Real, Categorical, Integer

from tensorflow.python.keras import backend as K

import h5py
import matplotlib.pyplot as plt
import math

import pandas as pd

from network import read_datasets

dim_learning_rate = Real(low=1e-6, high=1e-2, prior='log-uniform',
                         name='learning_rate')
# dim_learning_rate = Real(low=1e-4, high=1e-2, prior='log-uniform',
#                          name='learning_rate')


# the number of dense layers in the neural network, at least 1 dense layer and at most 7 dense layers
dim_num_dense_layers = Integer(low=1, high=7, name='num_dense_layers')
# dim_num_dense_layers = Integer(low=1, high=5, name='num_dense_layers')


# number of nodes for each dense layer
# at least 5 and at most 512 nodes in each layer
dim_num_dense_nodes = Integer(low=256, high=1024, name='num_dense_nodes')
# dim_num_dense_nodes = Integer(low=1, high=28, name='num_dense_nodes')

# search-dimension for the activation-function
# a combinatorial or categorical parameter which can be either 'relu' or 'sigmoid'
dim_activation = Categorical(categories=['relu', 'sigmoid'],
                             name='activation')
# dim_activation = Categorical(categories=['relu', 'sigmoid'],
#                              name='activation')

dim_num_input_nodes = Integer(low=16, high=768, name='num_input_nodes')

dim_batch_size = Integer(low=32, high=96, name='batch_size')
dim_adam_decay = Real(low=1e-6, high=1e-2, name="adam_decay")

dimensions = [dim_learning_rate,
              dim_num_dense_layers,
              dim_num_input_nodes,
              dim_num_dense_nodes,
              dim_activation,
              dim_batch_size,
              dim_adam_decay
              ]

# default_parameters = [1e-3, 1, 512, 13, 'relu', 64, 1e-3]
default_parameters = [1e-3, 1, 512, 256, 'relu', 64, 1e-3]

# X_train, y_train, test_data, test_labels = read_datasets.read_from_json()
# path = '../datasets/center_distance/vectors_1/window_size_11/2steps_10walks/data4_60.csv'
# X_train, y_train = read_datasets.read_data(path)


def create_model(learning_rate, num_dense_layers, num_input_nodes,
                 num_dense_nodes, activation, adam_decay):
    """
    Hyper-parameters:
    learning_rate:     Learning-rate for the optimizer.
    num_dense_layers:  Number of dense layers.
    num_dense_nodes:   Number of nodes in each dense layer.
    activation:        Activation function for all layers.
    """
    # start the model making process and create our first layer
    model = Sequential()
    input_shape = (temp_input_shape,)
    model.add(Dense(num_input_nodes, input_shape=input_shape, activation=activation
                    ))
    # create a loop making a new dense layer for the amount passed to this model.
    # naming the layers helps avoid tensorflow error deep in the stack trace.
    for i in range(num_dense_layers):
        name = 'layer_dense_{0}'.format(i + 1)
        model.add(Dense(num_dense_nodes,
                        activation=activation,
                        name=name
                        ))
    # add our classification layer.
    num_output_nodes = 15
    model.add(Dense(num_output_nodes, activation='softmax'))

    # setup our optimizer and compile
    adam = Adam(lr=learning_rate, decay=adam_decay)
    model.compile(optimizer=adam, loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
    return model


@use_named_args(dimensions=dimensions)
def fitness(learning_rate, num_dense_layers, num_input_nodes,
            num_dense_nodes, activation, batch_size, adam_decay):
    model = create_model(learning_rate=learning_rate,
                         num_dense_layers=num_dense_layers,
                         num_input_nodes=num_input_nodes,
                         num_dense_nodes=num_dense_nodes,
                         activation=activation,
                         adam_decay=adam_decay
                         )
    # named blackbox because it represents the structure
    blackbox = model.fit(x=x_train,
                         y=y_train,
                         epochs=3,
                         batch_size=batch_size,
                         validation_split=0.15,
                         verbose=0,
                         )
    # return the validation accuracy for the last epoch.
    accuracy = blackbox.history['val_accuracy'][-1]

    # Print the classification accuracy.
    # print()
    print("Accuracy: {0:.2%}".format(accuracy))
    # print()

    # Delete the Keras model with these hyper-parameters from memory.
    del model

    # Clear the Keras session, otherwise it will keep adding new
    # models to the same TensorFlow graph each time we create
    # a model with a different set of hyper-parameters.
    K.clear_session()
    # tf.reset_default_graph()  # deprecated
    tf.compat.v1.reset_default_graph()

    # the optimizer aims for the lowest score, so we return our negative accuracy
    return -accuracy


def optimize(X_train, Y_train, input_shape_x):
    # This is the search-dimension for the learning-rate. It is a real number (floating-point) with a lower
    # bound of 1e-6 and an upper bound of 1e-2. But instead of searching between these bounds directly, we use
    # a logarithmic transformation, so we will search for the number k in 1ek which is only bounded between -6 and -2
    global x_train
    x_train = X_train
    global y_train
    y_train = Y_train
    global temp_input_shape
    temp_input_shape = input_shape_x

    gp_result = gp_minimize(func=fitness,
                            dimensions=dimensions,
                            n_calls=12,
                            noise=0.01,
                            n_jobs=-1,
                            kappa=5,
                            x0=default_parameters)

    print("best accuracy was " + str(round(gp_result.fun * -100, 2)) + "%.")

    # dim_learning_rate, 0.00094878
    # dim_num_dense_layers, 4
    # dim_num_input_nodes, 218
    # dim_num_dense_nodes, 382
    # dim_activation, relu
    # dim_batch_size, 41
    # dim_adam_decay, 0.0069439
    print(gp_result.x)
    print("dim_learning_rate : ", gp_result.x[0])
    print("dim_num_dense_layers : ", gp_result.x[1])
    print("dim_num_input_nodes : ", gp_result.x[2])
    print("dim_num_dense_nodes : ", gp_result.x[3])
    print("dim_activation : ", gp_result.x[4])
    print("dim_batch_size : ", gp_result.x[5])
    print("dim_adam_decay : ", gp_result.x[6])

    print(gp_result.func_vals)

    pd.concat([pd.DataFrame(gp_result.x_iters,
                            columns=["learning rate", "hidden layers", "input layer nodes", "hidden layer nodes",
                                     "activation function", "batch size", "adam learning rate decay"]),
               (pd.Series(gp_result.func_vals * -100, name="accuracy"))], axis=1)

    best_accuracy = round(gp_result.fun * -100, 2)
    return gp_result, best_accuracy
