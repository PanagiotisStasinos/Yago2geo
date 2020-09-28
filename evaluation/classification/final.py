import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.layers import Dense
import time
import matplotlib.pyplot as plt

from evaluation.classification.classification_utils import read_feature_vectors


def plots(temp_history):
    # summarize history for accuracy
    plt.plot(temp_history.history['accuracy'])
    plt.plot(temp_history.history['val_accuracy'])
    plt.title('model accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    path = '../../plots/accuracy.png'
    plt.savefig(path)
    plt.show()
    # summarize history for loss
    plt.plot(temp_history.history['loss'])
    plt.plot(temp_history.history['val_loss'])
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    path = '../../plots/loss.png'
    plt.savefig(path)
    plt.show()


if __name__ == '__main__':
    start = time.time()

    learning_rate = 0.0038113223272439388
    num_dense_layers = 4
    num_input_nodes = 348
    num_dense_nodes = 577
    activation = 'relu'
    batch_size = 40
    adam_decay = 0.005689749519548906

# collect data
    path = '../../datasets/center_distance/window_size_10/5steps_10walks/cbow/100/feature_vectors_1.csv'
    train_data, train_labels, input_shape = read_feature_vectors.get_vectors(path)
    # exit(-1)
    print(np.unique(train_labels))


# model
    model = Sequential()
    input_shape = (input_shape,)
    model.add(Dense(num_input_nodes, input_shape=input_shape, activation=activation
                    ))

    for i in range(num_dense_layers):
        name = 'layer_dense_{0}'.format(i + 1)
        model.add(Dense(num_dense_nodes,
                        activation=activation,
                        name=name
                        ))
    # add classification layer (15 categories) .
    num_output_nodes = 15
    model.add(Dense(num_output_nodes, activation='softmax'))

    # setup our optimizer and compile
    adam = Adam(lr=learning_rate, decay=adam_decay)
    model.compile(optimizer=adam, loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])



    classWeight = read_feature_vectors.get_classWeight(train_labels)
    print(classWeight)
    # data_tensor = tf.convert_to_tensor(train_labels)
    history = model.fit(train_data, train_labels, batch_size=batch_size, epochs=10, shuffle=True,
                        class_weight=classWeight,
                        validation_split=0.3,
                        # callbacks=callback,
                        verbose=2)

    plots(history)

    end = time.time()
    print("Processor time (in seconds):", end)
    print("Time elapsed:", end - start)
    total = end - start
    minutes, secs = divmod(total, 60)
    hours, minutes = divmod(minutes, 60)
    print(hours, ' : ', minutes, ' : ', secs)
