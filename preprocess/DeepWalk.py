import os
from numpy.random import choice
import pandas


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
    # temp = []
    # vectors_len = len(vectors_set[next(iter(vectors_set))])
    # for j in range(1, vectors_len):
    #     temp.append('feature' + str(j))
    # temp.append('label')
    # df.columns = temp
    # df.rows = None
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
