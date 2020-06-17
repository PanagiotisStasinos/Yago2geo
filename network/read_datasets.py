import json
import pandas as pd
from pandas import read_csv
from sklearn.preprocessing import Normalizer
import tensorflow as tf
from collections import Counter


def read_from_csv():
    #   train data
    path = '../datasets/train_set_vectors.csv'

    # names = ['0', '1', '2', '3', '4', '5', '6', '7']
    # data_frame = read_csv(path, names=names)
    # array = data_frame.values
    # array = np.delete(array, 0, 0)

    data_frame = read_csv(path)
    data_frame = data_frame.reset_index(drop=True)
    array = data_frame.values
    array = array[:, 1:]

    # print(array.shape)
    # print(array[0])

    data_normalizer = Normalizer(norm='l2').fit(array)
    train_data_normalized = data_normalizer.transform(array)

    #   train labels
    path = '../datasets/train_set_labels.csv'

    # names = ["OS_type"]
    # data_frame = read_csv(path, names=names)
    # array = data_frame.values
    # array = np.delete(array, 0, 0)

    data_frame = read_csv(path)
    data_frame = data_frame.reset_index(drop=True)
    array = data_frame.values
    array = array[:, 1:]

    # print(array.shape)
    # print(array[0])
    data_normalizer = Normalizer(norm='l2').fit(array)
    train_labels_normalized = data_normalizer.transform(array)

    #    test data
    path = '../datasets/test_set_vectors.csv'

    # names = ['0', '1', '2', '3', '4', '5', '6', '7']
    # data_frame = read_csv(path, names=names)
    # array = data_frame.values
    # array = np.delete(array, 0, 0)

    data_frame = read_csv(path)
    data_frame = data_frame.reset_index(drop=True)
    array = data_frame.values
    array = array[:, 1:]

    # print(array.shape)
    # print(array[0])
    data_normalizer = Normalizer(norm='l2').fit(array)
    test_data_normalized = data_normalizer.transform(array)

    #   test labels
    path = '../datasets/test_set_labels.csv'

    # names = ['OS_types']
    # data_frame = read_csv(path, names=names)
    # array = data_frame.values
    # array = np.delete(array, 0, 0)

    data_frame = read_csv(path)
    data_frame = data_frame.reset_index(drop=True)
    array = data_frame.values
    array = array[:, 1:]

    # print(array.shape)
    # print(array[0])
    data_normalizer = Normalizer(norm='l2').fit(array)
    test_labels_normalized = data_normalizer.transform(array)

    # set_printoptions(precision=2)
    # print("\nNormalized data:\n", Data_normalized[0:3])

    return train_data_normalized, train_labels_normalized, test_data_normalized, test_labels_normalized


def read_from_json():
#   train data
    path = '../datasets/train_set_vectors.json'

    input_file = open(path)
    content = json.load(input_file)
    df = pd.DataFrame.from_dict(content, orient='index')
    array = df.values

    # print(array.shape)
    # print(array[0])
    data_normalizer = Normalizer(norm='l2').fit(array)
    train_data_normalized = data_normalizer.transform(array)


#   train labels
    path = '../datasets/train_set_labels.json'

    input_file = open(path)
    content = json.load(input_file)
    df = pd.DataFrame.from_dict(content, orient='index')
    array = df.values
    # array = array.transpose()

    # print(array.shape)
    # print(array[0])
    # data_normalizer = Normalizer(norm='l2').fit(array)
    # train_labels_normalized = data_normalizer.transform(array)
    train_labels_normalized = array

#    test data
    path = '../datasets/test_set_vectors.json'

    input_file = open(path)
    content = json.load(input_file)
    df = pd.DataFrame.from_dict(content, orient='index')
    array = df.values

    # print(array.shape)
    # print(array[0])
    data_normalizer = Normalizer(norm='l2').fit(array)
    test_data_normalized = data_normalizer.transform(array)


#   test labels
    path = '../datasets/test_set_labels.json'

    input_file = open(path)
    content = json.load(input_file)
    df = pd.DataFrame.from_dict(content, orient='index')
    array = df.values
    # array = array.transpose()

    # print(array.shape)
    # print(array[0])
    # data_normalizer = Normalizer(norm='l2').fit(array)
    # test_labels_normalized = data_normalizer.transform(array)
    test_labels_normalized = array

    return train_data_normalized, train_labels_normalized, test_data_normalized, test_labels_normalized


# A utility method to create a tf.data dataset from a Pandas Dataframe
def df_to_dataset(df, shuffle=True, batch_size=32):
    df = df.copy()
    labels = df.pop('label')
    ds = tf.data.Dataset.from_tensor_slices((dict(df), labels))
    if shuffle:
        ds = ds.shuffle(buffer_size=len(df))
    ds = ds.batch(batch_size)
    return ds


def get_classWeight(train_labels):
    ll = [i[0] for i in train_labels.tolist()]
    print(ll)
    w_dict = Counter(ll)
    print(w_dict)
    print(len(w_dict))
    return w_dict


def read_data(path):
    #   train data

    data_frame = read_csv(path)
    data_frame = data_frame.reset_index(drop=True)
    array = data_frame.values
    print(array.shape)
    labels = array[:, -1]
    sh = labels.shape
    print(labels.shape)
    labels = labels.reshape(sh[0],1)
    print(labels.shape)
    array = array[:, 1:]

    print(str(type(array)))

    print(array.shape)
    print(array[0])

    data_normalizer = Normalizer(norm='l2').fit(array)
    train_data_normalized = data_normalizer.transform(array)

    print(str(type(train_data_normalized)))
    # temp = np.hsplit(train_data_normalized, np.array([3, 6]))

    return train_data_normalized, labels

