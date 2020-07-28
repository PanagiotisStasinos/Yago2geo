import os

from location.KGraph import sort_Locations, store_distances, get_distances_from_csv, empty_distance_dicts, \
    find_polygon_distances

from location.KGraph import find_center_distances, get_distances_from_csv
from preprocess.random_walk import store_random_walks
from preprocess.random_walk import store_random_walks3
from preprocess.read_OS_topological import get_statistics_of_topological_and_matches_files
from preprocess.read_OS_topological import get_topological_info
from location.KGraph import get_locations_from_csv
import time

if __name__ == "__main__":
    start = time.time()

    # weighted_graph = get_locations_from_csv("../datasets/locations_csv/locations_1.csv")
    # get_distances_from_csv(weighted_graph,
    #                        "../datasets/center_distance/vectors_1/window_size_31/distances/distances_lat.csv",
    #                        "../datasets/center_distance/vectors_1/window_size_31/distances/distances_lon.csv")
    # weighted_graph.print_statistics()
    #
    # vectors_type = 1
    # distance_type = "center_distance"
    # num_of_steps = 2
    # num_of_walks = 10
    # window_size = 31
    # store_random_walks3(weighted_graph, distance_type, vectors_type, num_of_steps, num_of_walks, window_size,
    #                     "../locations_stats_" + str(vectors_type) + ".csv")
    # weighted_graph.print_statistics()

    vectors_type = 1
    file = "../datasets/locations_csv/locations_1.csv"
    weighted_graph = get_locations_from_csv(file)

    # for distance_type in ['center_distance', 'polygon_distance']:
    for distance_type in ['center_distance']:
    # for distance_type in ['polygon_distance']:

        # for window_size in [11, 21, 31, 41, 51, 61, 71, 81]:
        # for window_size in [21, 31, 41, 51, 61, 71, 81]:
        # for window_size in [11, 21, 31, 41, 51]:
        # for window_size in [31]:
        for window_size in [51]:
            # check if distances exist
            path = '../datasets/' + distance_type + '/vectors_' + str(vectors_type) + '/window_size_' + \
                   str(window_size) + '/distances/'
            if not os.path.exists(path):
                if distance_type == 'center_distance':
                    print("find center distances")
                    find_center_distances(weighted_graph, window_size)
                elif distance_type == 'polygon_distance':
                    print("find polygon distances")
                    find_polygon_distances(weighted_graph, window_size)

                print("store distances")
                store_distances(weighted_graph, vectors_type, distance_type, window_size)
            else:
                print("get distances")
                get_distances_from_csv(weighted_graph, path + 'distances_lat.csv', path + 'distances_lon.csv')

            for k, p in [(10, 5), (2, 10), (4, 4)]:
                # for k, p in [(10, 5)]:
                # for k, p in [(2, 10)]:
                print("random walk")
                store_random_walks3(weighted_graph, distance_type, vectors_type, k, p, window_size,
                                    "../locations_stats_" + str(vectors_type) + ".csv")

            # empty distance dicts
            print("delete previous distances")
            empty_distance_dicts(weighted_graph)

    end = time.time()
    print("Processor time (in seconds):", end)
    print("Time elapsed:", end - start)
    total = end - start
    minutes, secs = divmod(total, 60)
    hours, minutes = divmod(minutes, 60)
    print(hours, ' : ', minutes, ' : ', secs)

    exit(0)
