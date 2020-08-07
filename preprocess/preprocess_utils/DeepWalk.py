import os
from numpy.random import choice
import pandas
from numpy import array, argmax
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder

# for skip_gram
from tensorflow.keras.models import Sequential
from tensorflow.keras import layers
from tensorflow.keras.optimizers import Adam

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


def skip_gram(weighted_graph, distance_type, num_of_steps, num_of_walks, window_size):
    file = "../datasets/locations_csv/locations.csv"
    df = pandas.read_csv(file)

    temp = []
    for index, row in df.iterrows():
        temp.append(row['name'])

    values = array(temp)
    print(values.shape)
    print(values)

    # integer encode
    label_encoder = LabelEncoder()
    integer_encoded = label_encoder.fit_transform(values)
    print(integer_encoded.shape)
    print(integer_encoded)

    # binary encode
    onehot_encoder = OneHotEncoder(sparse=False)
    integer_encoded = integer_encoded.reshape(len(integer_encoded), 1)
    onehot_encoded = onehot_encoder.fit_transform(integer_encoded)
    print(onehot_encoded.shape)
    print(onehot_encoded)

    # invert first example
    inverted = label_encoder.inverse_transform([argmax(onehot_encoded[0, :])])
    print(inverted.shape)
    print(inverted)

    model = Sequential([
        layers.Dense(100, input_shape=(19648,)),
        layers.Dense(4, activation="softmax")
    ])
    model.summary()
    opt1 = Adam(learning_rate=.00335888)
    model.compile(optimizer=opt1
                  # , loss='sparse_categorical_crossentropy'
                  , loss='categorical_crossentropy'
                  # , metrics=['loss']
    )

    # model.fit(onehot_encoded, batch_size=78, epochs=20, shuffle=True)
