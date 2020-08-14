import os
from sys import getsizeof

from numpy.random import choice
import pandas
import numpy as np
from numpy import array, argmax
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder

# for skip_gram
from tensorflow.keras.models import Sequential
from tensorflow.keras import layers
from tensorflow.keras.optimizers import Adam
from sklearn.preprocessing import Normalizer


# keeps only the name of each location visited
def deep_walk(weighted_graph, distance_type, num_of_steps, num_of_walks, window_size):
    path = '../datasets/' + distance_type + '/window_size_' + str(window_size) + '/' + str(
        num_of_steps) + 'steps_' + str(
        num_of_walks) + 'walks' + '/'
    if not os.path.exists(path):
        os.makedirs(path)
        print("CREATE ", path)
    else:
        print("\tvectors exist (num_of_steps=", num_of_steps, " num_of_walks=", num_of_walks, " window_size=",
              window_size, ")")
        return

    ############################
    #
    #
    #
    ############################
    vectors_set = {}
    count = 0
    for loc in weighted_graph.Locations:
        for walk in range(num_of_walks):
            temp_walk = random_walk(loc, num_of_steps, weighted_graph)
            vectors_set[count] = temp_walk
            count = count + 1

    df = pandas.DataFrame.from_dict(vectors_set, orient='index')
    df.to_csv(path + 'random_walks.csv', index=False)
    # df.to_json(path + 'random_walks.json', orient='index')


def random_walk(current_location, num_of_steps, weighted_graph):
    temp_walk = []
    cur_node = current_location
    for step in range(num_of_steps):
        neighbors = weighted_graph.find_neighbors_2(cur_node)
        next_node, os_id, center, os_type, os_area = find_next(neighbors)
        cur_node = next_node

        temp_walk.append(next_node)

    return temp_walk


def find_next(neighbors):
    name, weight, os_id, os_center, os_t, os_area = zip(*neighbors)
    draw = choice(name, 1, weight)
    for na, we, osID, center, os_type, area in neighbors:
        if draw.item(0) == na:
            break
    return draw.item(0), osID, center, os_type, area


# same as integer_encoded
def get_index_of_one(one_hot):
    print(one_hot)
    for i in range(len(one_hot)):
        if one_hot[i] == 1:
            return i


def get_name(one_hot, Vocabulary, Inverse_Vocabulary, label_encoder, onehot_encoder):
    int_val = onehot_encoder.inverse_transform([one_hot])
    name = label_encoder.inverse_transform(int_val[0])
    return name[0]


def get_one_hot(name, Vocabulary):
    return Vocabulary[name]


# ###############################################################
def get_vectors_from_row(row, num_of_steps, Vocabulary, input_vecs, output, skip_gram_window):
    for i in range(0, num_of_steps):
        half_window = int(skip_gram_window / 2)
        for j in range(i - half_window, i + half_window + 1):
            if i != j and 0 <= j < num_of_steps:
                input_vecs.append(Vocabulary[row[str(i)]])
                output.append(Vocabulary[row[str(j)]])



def get_train_set(file, Vocabulary, Inverse_Vocabulary, label_encoder, onehot_encoder, num_of_steps,
                  num_of_walks, skip_gram_window):
    # file = '../datasets/[(]distance_type]/window_size_[window_size]/' \
    #        '[num_of_steps]steps_[num_of_walks]walks/random_walks.csv'
    df = pandas.read_csv(file)
    print(df.shape)

    input_vecs = []
    output = []

    for index, row in df.iterrows():
        get_vectors_from_row(row, num_of_steps, Vocabulary, input_vecs, output, skip_gram_window)

    # for i in range(0, df['0'].count(), 1000):
    #     print(output[i][0], ",", output[i][1], ",", input_vecs[i], ",", output[i][2], ",", output[i][3])
    #
    # print('total : ', df['0'].count())

    X = array(input_vecs)
    Y = array(output)

    print("X", X.shape, "Y", Y.shape)
    print("X ", getsizeof(X), "Y", getsizeof(Y))
    print("X ", getsizeof(X)/(1024 ** 3), "Y", getsizeof(Y)/(1024 ** 3))

    # exit(-2)

    return X, Y


def skip_gram(file_path, num_of_steps, num_of_walks, skip_gram_window):
    file = "../datasets/locations_csv/locations.csv"
    df = pandas.read_csv(file)

    temp = []
    for index, row in df.iterrows():
        temp.append(row['name'])

    values = array(temp)
    # print("\t values , ", str(type(values)))    # numpy.ndarray
    # print(values.shape)    # (19648,)
    # print(values)

    # integer encode
    label_encoder = LabelEncoder()
    integer_encoded = label_encoder.fit_transform(values)
    # print("\t integer_encoded , ", str(type(integer_encoded)))   # numpy.ndarray
    # print(integer_encoded.shape)    # (19648, )
    # print(integer_encoded)
    # print(integer_encoded[0])

    # binary encode
    onehot_encoder = OneHotEncoder(sparse=False)
    integer_encoded = integer_encoded.reshape(len(integer_encoded), 1)
    onehot_encoded = onehot_encoder.fit_transform(integer_encoded)
    # onehot_encoded = np.float32(onehot_encoded)
    onehot_encoded = np.int8(onehot_encoded)
    # onehot_encoded = np.array(onehot_encoded, dtype=bool)     # same as int_8
    # print("\t onehot_encoded , ", str(type(onehot_encoded)))  # numpy.ndarray
    # print(onehot_encoded.shape)  # (19648, 19648)
    # print(onehot_encoded)
    # print(" onehot_encoded[0]", str(type(onehot_encoded[0])))
    # print(onehot_encoded[0], get_index_of_one(onehot_encoded[0]))

    # # invert first example
    # inverted = label_encoder.inverse_transform([argmax(onehot_encoded[0, :])])  # 0, gia to 1o location apo to csv
    # print("\t inverted , ", str(type(inverted)))  # numpy.ndarray
    # print(inverted.shape)
    # print(inverted)  # name of first location
    #
    # print(" ----- EXAMPLE -----")
    # int_val = onehot_encoder.inverse_transform([onehot_encoded[0, :]])
    # print(int_val)
    # name = label_encoder.inverse_transform([argmax(int_val)])  # to argmax() xreiazetai, den exw katalavei giati
    # print(name)
    # print("--------------------")

    Vocabulary = {}  # key: name , value: one-hot
    Inverse_Vocabulary = {}  # key: integer val , value: name
    for i in range(len(values)):
        Vocabulary[values[i]] = onehot_encoded[i]
        Inverse_Vocabulary[integer_encoded[i][0]] = values[i]

    # print(" ----- TEST -----")
    # print("VOC :", values[1000], Vocabulary[values[1000]])
    # print("I-VOC", integer_encoded[1000][0], Inverse_Vocabulary[integer_encoded[1000][0]])
    # print("test", get_index_of_one(Vocabulary[values[1000]]))
    #
    # # int_val = onehot_encoder.inverse_transform([onehot_encoded[1000, :]])
    # # print(int_val[0])
    # # name = label_encoder.inverse_transform(int_val[0])
    # # print(name[0])
    # # print(values[1000])
    # print(values[1000], get_one_hot(values[1000], Vocabulary))
    # print(Vocabulary[values[1000]],
    #       get_name(Vocabulary[values[1000]], Vocabulary, Inverse_Vocabulary, label_encoder, onehot_encoder))
    # print("-----------------")
    #
    # exit(-1)
    X, Y = get_train_set(file_path, Vocabulary, Inverse_Vocabulary, label_encoder, onehot_encoder, num_of_steps,
                         num_of_walks, skip_gram_window)
    # exit(-2)
    model = Sequential([
        layers.Dense(100, input_shape=(19648,)),
        layers.Dense(19648, activation="softmax")
    ])
    model.summary()
    opt1 = Adam(learning_rate=.00335888)
    model.compile(optimizer='adam'
                  # , loss='sparse_categorical_crossentropy'
                  , loss='categorical_crossentropy'
                  # , metrics=['loss']
                  )

    # Allocation of 78592000 exceeds 10% of system memory, when batch_size=1000
    model.fit(X, Y, batch_size=400, epochs=1, shuffle=True, verbose=0)

    weights = [layer.get_weights() for layer in model.layers]

    print(str(type(weights[0][0])))
    print(weights[0][0].shape)

    vec_dict = {}
    counter = 0
    for name in values:
        vec_dict[name] = weights[0][0][counter]
        counter += 1

    df = pandas.DataFrame.from_dict(vec_dict, orient='index')
    check_if_l1_normalized(df)

    temp_array = df.values

    print(temp_array.shape)
    print(temp_array[0])

    data_normalizer = Normalizer(norm='l2').fit(temp_array)
    temp_array = data_normalizer.transform(temp_array)
    print(temp_array.shape)
    print(temp_array[0])

    v_dict = {}
    counter = 0
    for name in values:
        v_dict[name] = temp_array[counter]
        counter += 1

    df = pandas.DataFrame.from_dict(v_dict, orient="index")
    df.to_csv("../datasets/center_distance/window_size_11/" + str(num_of_steps) + "steps_" +
              str(num_of_walks) + "walks/vectors.csv", index=True)
    # check_if_l2_normalized(df)


# in each row the sum of the squares will always be up to 1
def check_if_l2_normalized(df):
    v = df.values
    print(v.shape)
    print(v.shape[0])
    counter = 0
    flag = 0
    for row in range(0, v.shape[0]):
        print(np.sum(v[row] ** 2))
        if np.sum(v[row] ** 2) != 1.0:
            flag += 1
        counter += 1
    if flag > 1:
        print("Not l-2 Normalized", flag)


# in each row the sum of the absolute values will always be up to 1
def check_if_l1_normalized(df):
    v = df.values
    print(v.shape)
    print(v.shape[0])
    counter = 0
    flag = 0
    for row in range(0, v.shape[0]):
        print(np.sum(abs(v[row])))
        if np.sum(abs(v[row])) != 1.0:
            flag += 1
        counter += 1
    if flag > 1:
        print("Not l-1 Normalized", flag)
