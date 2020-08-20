from collections import Counter

import pandas
from pandas import array
import utils
import numpy


# reads skip gram vectors and get type as label for every location
def get_vectors_n_type_labels(file):
    locs_df = pandas.read_csv("../datasets/locations_csv/locations.csv")
    type_dict = {}
    for index, row in locs_df.iterrows():
        type_dict[row['name']] = row['type']

    df = pandas.read_csv(file, index_col=0)
    temp_v = []
    temp_l = []
    for index, row in df.iterrows():
        # print(index)
        # print("--------------------------")
        temp = row.to_numpy()
        # print(temp)
        # print("\t#\t###############################################")

        temp_v.append(temp)
        temp_l.append(utils.get_value_of_type(type_dict[index]))

    X = numpy.array(temp_v)
    Y = numpy.array(temp_l)

    print("X", X.shape)     # (19648, 100)
    print("Y", Y.shape)     # (19648, )

    label_weights = [0 for i in range(15)]
    for t in temp_l:
        label_weights[t] += 1
    for i in range(15):
        print("LABEL_", i, " ", label_weights[i], "-",label_weights[i]/sum(label_weights))
    return X, Y


# reads feature vectors
def get_train_set(file):
    df = pandas.read_csv(file)
    # print(df.shape)
    feature_vectors_list = df.values.tolist()

    vectors_dict = {}
    train_set = []
    label_set = []
    for temp_list in feature_vectors_list:
        # print(temp_list)
        # print(temp_list[0], "-", temp_list[1:-1], temp_list[-1])
        train_set.append(temp_list[1:-1])
        label_set.append(temp_list[-1])
        # vectors_dict[temp_list[0]] = temp_list[1:]

    X = numpy.array(train_set)
    Y = numpy.array(label_set)

    return X, Y


def get_classWeight(train_labels):
    label_weights = [0 for i in range(15)]
    for t in train_labels:
        label_weights[t] += 1
    print(label_weights)
    w_dict = {}
    for i in range(15):
        w_dict[i] = label_weights[i]
    print(w_dict)
    print(len(w_dict))
    return w_dict
