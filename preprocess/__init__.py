import os

from location.KGraph import sort_Locations, store_distances, get_distances_from_csv, empty_distance_dicts, \
    find_polygon_distances
from location.KGraph import find_center_distances
from preprocess.random_walk import store_random_walks
from preprocess.random_walk import store_random_walks2
from preprocess.read_OS_topological import get_statistics_of_topological_and_matches_files
from preprocess.read_OS_topological import get_topological_info
from location.KGraph import get_locations_from_csv
import time

########################################################
#   1)  get_locations_from_csv()
#       reads locations from /datasets/locations_csv/locations_1.csv
#       locations_1.csv has the locations from OS_extended and OS_new files
#   2)  sort_locations()
#       find neighbors sorted by by longitude and latitude for each location
#   3)  get_topological_info()
#       store locations that are adjacent or within each location
#   4)  find_distances()
#       find distances for each location with its closest by longitude, latitude, adjacent and within locations
#   5)  separate_data()  (not randomly)
#       separates location to 2 sets, one for training the nn and one for testing the nn
#
########################################################
if __name__ == "__main__":
    start = time.time()

    # for vectors_type in [1, 2]:
    # for vectors_type in [1]:
    for vectors_type in [2]:
        file = "../datasets/locations_csv/locations_" + str(vectors_type) + ".csv"
        weighted_graph = get_locations_from_csv(file)

        print("sort locations_csv")
        sort_Locations(weighted_graph)

        # for distance_type in ['center_distance', 'polygon_distance']:
        # for distance_type in ['center_distance']:
        for distance_type in ['polygon_distance']:

            # for window_size in [11, 21, 31, 41, 51, 61, 71, 81]:
            # for window_size in [11, 21, 31]:
            for window_size in [11]:
            # for window_size in [21, 31, 41, 51, 61, 71, 81]:
                # # check if distances exist
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

                for k, p in [(10, 5), (2, 10)]:
                # for k, p in [(10, 5)]:
                # for k, p in [(2, 10)]:
                    print("random walk")
                    store_random_walks2(weighted_graph, distance_type, vectors_type, k, p, window_size)

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
