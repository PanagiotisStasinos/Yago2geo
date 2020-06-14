from numpy.random import choice
import json
import numpy as np
from sklearn import preprocessing
import pandas
from preprocess.utils import get_value_of_type
import preprocess.utils as utils

# import sys
# sys.setrecursionlimit(15000)     # this number can be any limit
###########################################
#
#
#
###########################################
NUM_OF_STEPS = 2  # recommended values of paper
NUM_OF_WALKS = 10


def store_random_walks(weighted_graph):
    #############################################################################
    #   dict : key = name of locations                                          #
    #          value = list of OS_IDs of locations visited by random walk       #
    #############################################################################
    train_vectors = {}
    train_type_vec = {}
    # type_vector = []
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

    df = pandas.DataFrame.from_dict(train_vectors, orient='index')
    df.to_csv('../datasets/train_set_vectors.csv')
    df.to_json('../datasets/train_set_vectors.json', orient='index')
    df = pandas.DataFrame.from_dict(train_type_vec, orient='index', columns=['OS_type'])
    df.to_csv('../datasets/train_set_labels.csv')
    df.to_json('../datasets/train_set_labels.json', orient='index')


    test_vectors = {}
    test_type_vec = {}
    for loc in weighted_graph.test_set:
        temp = []
        for walk in range(NUM_OF_WALKS):
            cur_node = loc
            for step in range(NUM_OF_STEPS):
                neighbors = weighted_graph.find_neighbors_2(cur_node)
                next_node, os_id, center, os_type, os_area = find_next(neighbors)
                cur_node = next_node

                temp.append(os_area)
                temp.append(get_value_of_type(os_type))

        test_type_vec[loc] = get_value_of_type(weighted_graph.get_os_type(loc))
        test_vectors[loc] = temp

    df = pandas.DataFrame.from_dict(test_vectors, orient='index')
    df.to_csv('../datasets/test_set_vectors.csv')
    df.to_json("../datasets/test_set_vectors.json", orient='index')
    df = pandas.DataFrame.from_dict(test_type_vec, orient='index', columns=['OS_type'])
    df.to_csv('../datasets/test_set_labels.csv')
    df.to_json("../datasets/test_set_labels.json", orient='index')

    vectors = {}
    for loc in weighted_graph.Locations:
        temp = []
        for walk in range(NUM_OF_WALKS):
            cur_node = loc
            for step in range(NUM_OF_STEPS):
                neighbors = weighted_graph.find_neighbors_2(cur_node)
                next_node, os_id, center, os_type, os_area = find_next(neighbors)
                cur_node = next_node

                temp.append(os_area)
                temp.append(get_value_of_type(os_type))

        temp.append(get_value_of_type(weighted_graph.get_os_type(loc)))
        vectors[loc] = temp

    df = pandas.DataFrame.from_dict(vectors, orient='index')
    df.columns = ['area1', 'type1', 'area2', 'type2', 'area3', 'type3', 'area4', 'type4', 'area5', 'type5',
                  'area6', 'type6', 'area7', 'type7', 'area8', 'type8', 'area9', 'type9', 'area10', 'type10',
                  'area11', 'type11', 'area12', 'type12', 'area13', 'type13', 'area14', 'type14', 'area15', 'type15',
                  'area16', 'type16', 'area17', 'type17', 'area18', 'type18', 'area19', 'type19', 'area20', 'type20',
                  'label']
    df.rows = None
    df.to_csv('../datasets/data.csv', index=False)
    df.to_json("../datasets/data.json", orient='index')


def store_random_walks2(weighted_graph):
    #############################################################################
    #   dict : key = name of locations                                          #
    #          value = list of OS_IDs of locations visited by random walk       #
    #############################################################################

    vectors = [dict() for x in range(5)]
    for loc in weighted_graph.Locations:
        temp1 = []      # only os_area
        temp2 = []      # os_area, os_type
        temp3 = []      # os_area, os_type, center
        temp4 = []      # os_area, os_type, center, os_id
        temp5 = []      # os_area, center
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

    for i in range(5):
        df = pandas.DataFrame.from_dict(vectors[i], orient='index')
        # df.columns = ['area1', 'type1', 'area2', 'type2', 'area3', 'type3', 'area4', 'type4', 'area5', 'type5',
        #               'area6', 'type6', 'area7', 'type7', 'area8', 'type8', 'area9', 'type9', 'area10', 'type10',
        #               'area11', 'type11', 'area12', 'type12', 'area13', 'type13', 'area14', 'type14', 'area15', 'type15',
        #               'area16', 'type16', 'area17', 'type17', 'area18', 'type18', 'area19', 'type19', 'area20', 'type20',
        #               'label']
        temp = []
        vectors_len = len(vectors[i][next(iter(vectors[i]))])
        for j in range(1, vectors_len):
            temp.append('feature'+str(j))
        temp.append('label')
        df.columns = temp
        df.rows = None
        df.to_csv('../datasets/window_size_'+str(utils.WINDOW_SIZE)+'/'+str(NUM_OF_STEPS)+'steps_'+str(NUM_OF_WALKS)+'walks'+'/data'+str(i)+'_'+str(vectors_len-1)+'.csv', index=False)
        df.to_json('../datasets/window_size_'+str(utils.WINDOW_SIZE)+'/'+str(NUM_OF_STEPS)+'steps_'+str(NUM_OF_WALKS)+'walks'+'/data'+str(i)+'_'+str(vectors_len-1)+'.json', orient='index')


def find_next(neighbors):
    name, weight, os_id, os_center, os_t, os_area = zip(*neighbors)
    draw = choice(name, 1, weight)
    for na, we, osID, center, os_type, area in neighbors:
        if draw.item(0) == na:
            break
    return draw.item(0), osID, center, os_type, area
