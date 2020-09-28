import os
from location.KGraph import store_distances, empty_distance_dicts, find_polygon_distances
import utils
from location.KGraph import find_center_distances, get_distances_from_csv
from preprocess.preprocess_utils import DeepWalk
from location.KGraph import get_locations_from_csv
import time


def load_distances(file_path, w_graph):
    if not os.path.exists(file_path):
        if distance_type == 'center_distance':
            print("find center distances")
            find_center_distances(w_graph, window_size)
        elif distance_type == 'polygon_distance':
            print("find polygon distances")
            find_polygon_distances(w_graph, window_size)

        print("store distances")
        store_distances(w_graph, distance_type, window_size)
    else:
        print("get distances")
        get_distances_from_csv(w_graph, path + 'distances.csv')


if __name__ == "__main__":
    start = time.time()

    file = "../datasets/locations_csv/locations.csv"
    weighted_graph = get_locations_from_csv(file)

    # for distance_type in ['center_distance', 'polygon_distance']:
    # for distance_type in ['center_distance']:
    for distance_type in ['polygon_distance']:
        # for window_size in [10, 30, 50, 70]:
        for window_size in [30]:
            path = '../datasets/' + distance_type + '/window_size_' + str(window_size) + '/distances/'
            # check if distances exist
            load_distances(path, weighted_graph)
            # break
            # for num_of_steps, num_of_walks in [(5, 3), (3, 3)]:
            for num_of_steps, num_of_walks in [(5, 10), (10, 5), (15, 3)]:
                print("START DeepWalk (num_of_steps=", num_of_steps, " num_of_walks=", num_of_walks,
                      " window_size=", window_size)

                DeepWalk.deep_walk(weighted_graph, distance_type, num_of_steps, num_of_walks, window_size)

            # empty distance dicts
            print("delete previous distances")
            empty_distance_dicts(weighted_graph)
            # break

    utils.show_exec_time(start)

    exit(0)
