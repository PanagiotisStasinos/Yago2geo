import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.layers import Dense
import time
import network
import matplotlib.pyplot as plt


def plots(temp_history):
    # summarize history for accuracy
    plt.plot(temp_history.history['accuracy'])
    plt.plot(temp_history.history['val_accuracy'])
    plt.title('model accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    path = '../plots/accuracy.png'
    plt.savefig(path)
    plt.show()
    # summarize history for loss
    plt.plot(temp_history.history['loss'])
    plt.plot(temp_history.history['val_loss'])
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    path = '../plots/loss.png'
    plt.savefig(path)
    plt.show()


if __name__ == '__main__':
    start = time.time()

    learning_rate = 0.0038113223272439388
    num_dense_layers = 4
    num_input_nodes = 348
    num_dense_nodes = 577
    activation = 'relu'
    batch_size = 83
    adam_decay = 0.005689749519548906

    path = '../datasets/center_distance/vectors_2/window_size_31/2steps_10walks/data2_80.csv'
    train_data, train_labels, input_shape = network.read_datasets.read_data(path)
    print(np.unique(train_labels))

    # callback = [
    #     tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=2),
    #     tf.keras.callbacks.EarlyStopping(monitor='val_accuracy', patience=2),
    #     tf.keras.callbacks.EarlyStopping(monitor='loss', patience=2),
    #     tf.keras.callbacks.EarlyStopping(monitor='accuracy', patience=2)
    # ]

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

    classWeight = network.read_datasets.get_classWeight(train_labels)
    print(classWeight)
    history = model.fit(train_data, train_labels, batch_size=batch_size, epochs=30, shuffle=True,
                        class_weight=classWeight,
                        validation_split=0.3,
                        # callbacks=callback,
                        verbose=2)

    plots(history)

####################################################
#   2 : os_area, os_type, center
#   we have 4 features for each neighbor, and 20 neihgbors (2 steps x 10 walks), so 80-len vectors
#   features : 0 os_area
#              1 os_type, [0,14]
#              2 center.x
#              3 center.y
#
####################################################
    # print("Stats for the vectors")
    # raw_train_data, labels = network.read_datasets.get_raw_data(path)
    #
    # for i in range(0, len(labels)-1):
    #     print(i, " ", raw_train_data[i])
    #     print(labels[i])






    end = time.time()
    print("Processor time (in seconds):", end)
    print("Time elapsed:", end - start)
    total = end - start
    minutes, secs = divmod(total, 60)
    hours, minutes = divmod(minutes, 60)
    print(hours, ' : ', minutes, ' : ', secs)
