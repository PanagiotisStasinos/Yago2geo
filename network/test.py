import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.layers import Dense
import time
import matplotlib.pyplot as plt
from network import simple_nn, compare, bayesian_opt, read_datasets


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

    # simple_nn.scikit_cla()
    # simple_nn.simple_nn_10()
    history = simple_nn.simple_nn_8()
    plots(history)

    # history = simple_nn.simple_nn_9()
    # plots(history)

    # file = '../datasets/balanced_classes/center_distance/vectors_1/window_size_31/10steps_5walks/data2_200.csv'
    # X_train, y_train, input_shape_x = read_datasets.read_data(file)
    # result, best_accuracy = bayesian_opt.optimize(X_train, y_train, input_shape_x)

    end = time.time()
    print("Processor time (in seconds):", end)
    print("Time elapsed:", end - start)
    total = end - start
    minutes, secs = divmod(total, 60)
    hours, minutes = divmod(minutes, 60)
    print(hours, ' : ', minutes, ' : ', secs)
