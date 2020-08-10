import time

from tensorflow import keras
from tensorflow.keras import Sequential
from tensorflow.keras.optimizers import Adam

import utils
from evaluation.evaluation_utils.read_vectors import get_vectors_n_type_labels, get_classWeight

if __name__ == '__main__':
    start = time.time()

    file = "../datasets/center_distance/window_size_11/3steps_3walks/vectors.csv"
    X, Y = get_vectors_n_type_labels(file)

    model = Sequential([
        keras.layers.Dense(768, input_shape=(100,), activation="relu"),
        keras.layers.Dense(256, activation="relu"),
        keras.layers.Dense(15, activation="softmax")
    ])
    model.summary()
    opt1 = Adam(learning_rate=.00335888)
    model.compile(optimizer=opt1, loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    classWeight = get_classWeight(Y)
    print(classWeight)
    model.fit(X, Y, batch_size=78, epochs=20, shuffle=True,
              class_weight=classWeight,
              validation_split=0.1,
              verbose=2)

    utils.show_exec_time(start)
    exit(0)
