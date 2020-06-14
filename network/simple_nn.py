import numpy as np
import pandas as pd

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Activation
# from tensorflow.keras.layers. import Dense
from tensorflow.keras.optimizers import Adam

from network import read_datasets


def simple_nn_1():
    train_data, train_labels, test_data, test_labels = read_datasets.read_from_json()
    # train_data, train_labels, test_data, test_labels = read_datasets.read_from_csv()

    # print("train_data ", str(type(train_data)), " size ", train_data.shape, " ", train_data[0])
    # print("train_labels ", str(type(train_labels)), " size ", train_labels.shape)
    # print(np.unique(train_labels))
    # print("test_data ", str(type(test_data)), " size ", test_data.shape)
    # print("test_labels ", str(type(test_labels)), " size ", test_labels.shape)
    # print(np.unique(test_labels))

    model = Sequential([
        keras.layers.Dense(20, input_shape=(40,), activation="relu"),
        keras.layers.Dense(160, activation="relu"),
        keras.layers.Dense(15, activation="softmax")
    ])

    model.summary()

    opt1 = Adam(learning_rate=.0001)
    # opt2 = SGD(learning_rate=0.001)
    # opt3 = SGD(learning_rate=0.01, decay=1e-6, momentum=0.9, nesterov=True)
    model.compile(optimizer=opt1, loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    classWeight = read_datasets.get_classWeight(train_labels)
    model.fit(train_data, train_labels, batch_size=64, epochs=3, shuffle=True,
              class_weight=classWeight,
              validation_split=0.1,
              verbose=2)
    #
    model.evaluate(x=test_data, y=test_labels)

    # exit(0)


def simple_nn_2():
    # from sklearn.utils import compute_class_weight
    # classWeight = compute_class_weight('balanced', outputLabels, outputs)
    # classWeight = dict(enumerate(classWeight))
    # model.fit(X_train, y_train, batch_size = batch_size, nb_epoch = nb_epochs, show_accuracy = True, verbose = 2, \
    #           validation_data = (X_test, y_test), class_weight=classWeight)

    path = '../datasets/window_size_11/2steps_10walks/data4_60.csv'
    train_data, train_labels = read_datasets.read_data(path)
    print(np.unique(train_labels))
    model = Sequential([
        keras.layers.Dense(20, input_shape=(60,), activation="relu"),
        keras.layers.Dense(160, activation="relu"),
        # keras.layers.Dense(400, activation="relu"),
        # keras.layers.Dense(160, activation="relu"),
        keras.layers.Dense(15, activation="softmax")
    ])
    model.summary()
    opt1 = Adam(learning_rate=.0001)
    model.compile(optimizer=opt1, loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    classWeight = read_datasets.get_classWeight(train_labels)
    print(classWeight)
    model.fit(train_data, train_labels, batch_size=8, epochs=20, shuffle=True,
              class_weight=classWeight,
              validation_split=0.1,
              verbose=2)

    # exit(1)


def simple_nn_3():
    train_data, train_labels = read_datasets.read_data()
    print(np.unique(train_labels))
    model = Sequential([
        keras.layers.Dense(218, input_shape=(40,), activation="relu"),
        keras.layers.Dense(382, activation="relu"),
        keras.layers.Dense(382, activation="relu"),
        keras.layers.Dense(382, activation="relu"),
        keras.layers.Dense(382, activation="relu"),
        keras.layers.Dense(15, activation="softmax")
    ])
    model.summary()
    opt1 = Adam(learning_rate=.000094878)
    model.compile(optimizer=opt1, loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    classWeight = read_datasets.get_classWeight(train_labels)
    print(classWeight)
    model.fit(train_data, train_labels, batch_size=41, epochs=20, shuffle=True,
              class_weight=classWeight,
              validation_split=0.1,
              verbose=2)


def simple_nn_4():
    train_data, train_labels = read_datasets.read_data()
    print(np.unique(train_labels))
    model = Sequential([
        keras.layers.Dense(512, input_shape=(40,), activation="relu"),
        keras.layers.Dense(256, activation="relu"),
        keras.layers.Dense(15, activation="softmax")
    ])
    model.summary()
    opt1 = Adam(learning_rate=.0001)
    model.compile(optimizer=opt1, loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    classWeight = read_datasets.get_classWeight(train_labels)
    print(classWeight)
    model.fit(train_data, train_labels, batch_size=64, epochs=20, shuffle=True,
              class_weight=classWeight,
              validation_split=0.1,
              verbose=2)


def simple_nn_5():
    train_data, train_labels = read_datasets.read_data()
    print(np.unique(train_labels))
    model = Sequential([
        keras.layers.Dense(768, input_shape=(40,), activation="relu"),
        keras.layers.Dense(256, activation="relu"),
        keras.layers.Dense(15, activation="softmax")
    ])
    model.summary()
    opt1 = Adam(learning_rate=.00335888)
    model.compile(optimizer=opt1, loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    classWeight = read_datasets.get_classWeight(train_labels)
    print(classWeight)
    model.fit(train_data, train_labels, batch_size=78, epochs=20, shuffle=True,
              class_weight=classWeight,
              validation_split=0.1,
              verbose=2)


def simple_nn_6():
    train_data, train_labels = read_datasets.read_data()
    print(np.unique(train_labels))
    model = Sequential([
        keras.layers.Dense(768, input_shape=(40,), activation="relu"),
        keras.layers.Dense(256, activation="relu"),
        # keras.layers.Dense(256, activation="relu"),
        # keras.layers.Dense(256, activation="relu"),
        keras.layers.Dense(15, activation="softmax")
    ])
    model.summary()
    opt1 = Adam(learning_rate=.00335888)
    model.compile(optimizer=opt1, loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    classWeight = read_datasets.get_classWeight(train_labels)
    print(classWeight)
    model.fit(train_data, train_labels, batch_size=78, epochs=20, shuffle=True,
              class_weight=classWeight,
              validation_split=0.1,
              verbose=2)


def simple_nn_7():
    path = '../datasets/window_size_11/2steps_10walks/data4_60.csv'
    train_data, train_labels = read_datasets.read_data(path)
    print(np.unique(train_labels))
    model = Sequential([
        keras.layers.Dense(768, input_shape=(60,), activation="relu"),
        keras.layers.Dense(256, activation="relu"),
        # keras.layers.Dense(256, activation="relu"),
        # keras.layers.Dense(256, activation="relu"),
        keras.layers.Dense(15, activation="softmax")
    ])
    model.summary()
    opt1 = Adam(learning_rate=.00335888)
    model.compile(optimizer=opt1, loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    classWeight = read_datasets.get_classWeight(train_labels)
    print(classWeight)
    model.fit(train_data, train_labels, batch_size=78, epochs=20, shuffle=True,
              # class_weight=classWeight,
              # validation_split=0.1,
              verbose=2)