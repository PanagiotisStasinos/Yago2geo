import json
import pandas as pd
from pandas import read_csv
from sklearn.preprocessing import Normalizer
import tensorflow as tf
from collections import Counter
import numpy as np


def get_vectors(path):
    df = read_csv(path)
    lines = df.values
    print("lines ", lines.shape)

    names = lines[:, 0]
    vectors = lines[:, 1:-1]
    labels = lines[:, -1]

    labels2 = np.zeros(labels.shape[0], dtype=int)
    for i in range(labels.shape[0]):
        labels2[i] = labels[i]

    # sh = labels.shape
    # print(labels.shape)
    # labels = labels.reshape(sh[0], 1)
    # print(labels.shape)

    # for i in range(lines.shape[0]):
    #     print(lines[i])
    #     print(names[i], "\n - ", vectors[i], "\n - ", labels2[i])

    print("names ", names.shape)
    print("vectors ", vectors.shape)
    print("labs", labels2.shape)

    data_normalizer = Normalizer(norm='l2').fit(vectors)
    train_data_normalized = data_normalizer.transform(vectors)
    return train_data_normalized, labels2, vectors.shape[1]


def get_classWeight(train_labels):
    ll = [i for i in train_labels.tolist()]
    print(ll)
    w_dict = Counter(ll)
    print(w_dict)
    print(len(w_dict))
    return w_dict
