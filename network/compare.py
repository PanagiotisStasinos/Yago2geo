import numpy as np
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam

from network import read_datasets


def compare_1():
    path = '../datasets/center_distance/vectors_1/window_size_51/10steps_5walks/data4_150.csv'
    simple_model(path)
    path = '../datasets/center_distance/vectors_2/window_size_51/10steps_5walks/data4_150.csv'
    simple_model(path)


def simple_model(path):
    train_data, train_labels = read_datasets.read_data(path)
    print(np.unique(train_labels))
    model = Sequential([
        keras.layers.Dense(768, input_shape=(150,), activation="relu"),
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
