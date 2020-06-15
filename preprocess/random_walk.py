from numpy.random import choice
import pandas
from preprocess.utils import get_value_of_type
import preprocess.utils as utils

# recommended values of paper
# NUM_OF_STEPS = 10
# NUM_OF_WALKS = 5

NUM_OF_STEPS = 4  # recommended values of paper
NUM_OF_WALKS = 4


###################################################
# random walk function when data is separated in
# train and test sets
# creates : ../datasets/window_size_W/Ksteps_Pwalks/train_set_vectors.csv
#           ../datasets/window_size_W/Ksteps_Pwalks/train_set_vectors.json
#           ../datasets/window_size_W/Ksteps_Pwalks/train_set_labels.csv
#           ../datasets/window_size_W/Ksteps_Pwalks/train_set_labels.json
#      and  ../datasets/window_size_W/Ksteps_Pwalks/test_set_vectors.csv
#           ../datasets/window_size_W/Ksteps_Pwalks/test_set_vectors.json
#           ../datasets/window_size_W/Ksteps_Pwalks/test_set_labels.csv
#           ../datasets/window_size_W/Ksteps_Pwalks/test_set_labels.json
###################################################
def store_random_walks(weighted_graph):
    #########################################################################################
    #   TRAIN FILES                                                                          #
    #   train_vectors  : key = name of location                                             #
    #          value = list of OS_type and area of locations visited by random walk         #
    #   train_type_vec : key = name of location                                             #
    #          value = OS_type of key location                                              #
    #########################################################################################
    train_vectors = {}
    train_type_vec = {}
    for loc in weighted_graph.training_set:
        temp = []
        for walk in range(NUM_OF_WALKS):
            cur_node = loc
            for step in range(NUM_OF_STEPS):
                neighbors = weighted_graph.find_neighbors_2(cur_node)
                next_node, os_id, center, os_type, os_area = find_next(neighbors)
                cur_node = next_node

                temp.append(os_area)
                temp.append(get_value_of_type(os_type))

        train_type_vec[loc] = get_value_of_type(weighted_graph.get_os_type(loc))
        train_vectors[loc] = temp

    # create csv and json train files
    # files are saved in datasets folder under the current window size, number of steps
    # and number of walks folders
    df = pandas.DataFrame.from_dict(train_vectors, orient='index')
    df.to_csv(
        '../datasets/window_size_' + str(utils.WINDOW_SIZE) + '/' + str(NUM_OF_STEPS) + 'steps_' + str(NUM_OF_WALKS) \
        + 'walks/train_set_vectors.csv')
    df.to_json(
        '../datasets/window_size_' + str(utils.WINDOW_SIZE) + '/' + str(NUM_OF_STEPS) + 'steps_' + str(NUM_OF_WALKS) \
        + 'walks/train_set_vectors.json', orient='index')
    df = pandas.DataFrame.from_dict(train_type_vec, orient='index', columns=['OS_type'])
    df.to_csv('../datasets/window_size_' + str(utils.WINDOW_SIZE) + '/' + str(NUM_OF_STEPS) + 'steps_' + \
              str(NUM_OF_WALKS) + 'walks/train_set_labels.csv')
    df.to_json('../datasets/window_size_' + str(utils.WINDOW_SIZE) + '/' + str(NUM_OF_STEPS) + 'steps_' + \
               str(NUM_OF_WALKS) + 'walks/train_set_labels.json', orient='index')

    #########################################################################################
    #   TEST FILES                                                                          #
    #   test_vectors  : key = name of location                                              #
    #          value = list of OS_type and area of locations visited by random walk         #
    #   test_type_vec : key = name of location                                              #
    #          value = OS_type of key location                                              #
    #########################################################################################
    test_vectors = {}
    test_type_vec = {}
    for loc in weighted_graph.test_set:
        temp = []  # temp vector of current location
        for walk in range(NUM_OF_WALKS):
            cur_node = loc
            for step in range(NUM_OF_STEPS):
                # get _neighbors
                neighbors = weighted_graph.find_neighbors_2(cur_node)
                # choose one randomly
                next_node, os_id, center, os_type, os_area = find_next(neighbors)
                cur_node = next_node

                # add os_area and os_type to vector
                temp.append(os_area)
                temp.append(get_value_of_type(os_type))

        test_vectors[loc] = temp
        test_type_vec[loc] = get_value_of_type(weighted_graph.get_os_type(loc))

    # create csv and json test files
    # files are saved in datasets folder under the current window size, number of steps
    # and number of walks folders
    df = pandas.DataFrame.from_dict(test_vectors, orient='index')
    df.to_csv('../datasets/window_size_' + str(utils.WINDOW_SIZE) + '/' + str(NUM_OF_STEPS) + 'steps_' + \
              str(NUM_OF_WALKS) + 'walks/test_set_vectors.csv')
    df.to_json('../datasets/window_size_' + str(utils.WINDOW_SIZE) + '/' + str(NUM_OF_STEPS) + 'steps_' + \
               str(NUM_OF_WALKS) + 'walks/test_set_vectors.json', orient='index')
    df = pandas.DataFrame.from_dict(test_type_vec, orient='index', columns=['OS_type'])
    df.to_csv('../datasets/window_size_' + str(utils.WINDOW_SIZE) + '/' + str(NUM_OF_STEPS) + 'steps_' + \
              str(NUM_OF_WALKS) + 'walks/test_set_labels.csv')
    df.to_json('../datasets/window_size_' + str(utils.WINDOW_SIZE) + '/' + str(NUM_OF_STEPS) + 'steps_' + \
               str(NUM_OF_WALKS) + 'walks/test_set_labels.json', orient='index')


###################################################
# random walk function when data is not separated
# in train and test sets
# creates : ../datasets/window_size_W/Ksteps_Pwalks/dataX_S.csv / .json , X = [0,1,2,3,4] and S = [20,40,60,80,100]
###################################################
def store_random_walks2(weighted_graph):
    #############################################################################
    #   vectors : list of dicts  (each of these dicts has key value the name
    #               of current location and value the feature vector created
    #               by random walk
    #   temp* : feature vector
    #           1 : only os_area
    #           2 : os_area, os_type
    #           3 : os_area, os_type, center
    #           4 : os_area, os_type, center, os_id
    #           5 : os_area, center
    #############################################################################

    vectors = [dict() for x in range(5)]
    for loc in weighted_graph.Locations:
        temp1 = []  # os_area
        temp2 = []  # os_area, os_type
        temp3 = []  # os_area, os_type, center
        temp4 = []  # os_area, os_type, center, os_id
        temp5 = []  # os_area, center
        for walk in range(NUM_OF_WALKS):
            cur_node = loc
            for step in range(NUM_OF_STEPS):
                neighbors = weighted_graph.find_neighbors_2(cur_node)
                next_node, os_id, center, os_type, os_area = find_next(neighbors)
                cur_node = next_node

                temp1.append(os_area)

                temp2.append(os_area)
                temp2.append(get_value_of_type(os_type))

                temp3.append(os_area)
                temp3.append(get_value_of_type(os_type))
                temp3.append(center.x)
                temp3.append(center.y)

                temp4.append(os_area)
                temp4.append(get_value_of_type(os_type))
                temp4.append(center.x)
                temp4.append(center.y)
                temp4.append(os_id)

                temp5.append(os_area)
                temp5.append(center.x)
                temp5.append(center.y)

        temp1.append(get_value_of_type(weighted_graph.get_os_type(loc)))
        temp2.append(get_value_of_type(weighted_graph.get_os_type(loc)))
        temp3.append(get_value_of_type(weighted_graph.get_os_type(loc)))
        temp4.append(get_value_of_type(weighted_graph.get_os_type(loc)))
        temp5.append(get_value_of_type(weighted_graph.get_os_type(loc)))

        vectors[0][loc] = temp1
        vectors[1][loc] = temp2
        vectors[2][loc] = temp3
        vectors[3][loc] = temp4
        vectors[4][loc] = temp5

    # create csv and json data files
    # files are saved in datasets folder under the current window size, number of steps
    # and number of walks folders
    for i in range(5):
        df = pandas.DataFrame.from_dict(vectors[i], orient='index')
        temp = []
        vectors_len = len(vectors[i][next(iter(vectors[i]))])
        for j in range(1, vectors_len):
            temp.append('feature' + str(j))
        temp.append('label')
        df.columns = temp
        df.rows = None
        df.to_csv('../datasets/window_size_' + str(utils.WINDOW_SIZE) + '/' + str(NUM_OF_STEPS) + 'steps_' + str(
            NUM_OF_WALKS) + 'walks' + '/data' + str(i) + '_' + str(vectors_len - 1) + '.csv', index=False)
        df.to_json('../datasets/window_size_' + str(utils.WINDOW_SIZE) + '/' + str(NUM_OF_STEPS) + 'steps_' + str(
            NUM_OF_WALKS) + 'walks' + '/data' + str(i) + '_' + str(vectors_len - 1) + '.json', orient='index')


def find_next(neighbors):
    name, weight, os_id, os_center, os_t, os_area = zip(*neighbors)
    draw = choice(name, 1, weight)
    for na, we, osID, center, os_type, area in neighbors:
        if draw.item(0) == na:
            break
    return draw.item(0), osID, center, os_type, area
