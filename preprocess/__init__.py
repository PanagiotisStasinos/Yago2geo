from locations_graph.KGraph import sort_Locations
from locations_graph.KGraph import find_distances
from preprocess.random_walk import store_random_walks
from preprocess.random_walk import store_random_walks2
from preprocess.read_OS_topological import get_statistics_of_topological_and_matches_files
from preprocess.read_OS_topological import get_topological_info
from locations_graph.KGraph import get_locations_from_csv
import time

########################################################
#   1)  get_locations_from_csv()
#       reads locations from /datasets/locations_csv/locations.csv
#       locations.csv has the locations from OS_extended and OS_new files
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

    weighted_graph = get_locations_from_csv("../datasets/locations_csv/locations.csv")
    # weighted_graph.print_statistics()

    # print("sort locations_csv")
    # sort_Locations(weighted_graph)
    # weighted_graph.print_statistics()

    print("read topological")
    get_topological_info(weighted_graph)
    weighted_graph.print_statistics()
    get_statistics_of_topological_and_matches_files(weighted_graph)
    exit(1)
    print("find distances")
    find_distances(weighted_graph)
    weighted_graph.print_statistics()

    #########################################################################################
    print("separate data")
    weighted_graph.separate_data()
    weighted_graph.print_statistics()
    ##########################################################################################

    print("random walk")
    # store_random_walks(weighted_graph)
    store_random_walks2(weighted_graph)
    weighted_graph.print_statistics()

    weighted_graph.clear()

    end = time.time()
    print("Processor time (in seconds):", end)
    print("Time elapsed:", end - start)
