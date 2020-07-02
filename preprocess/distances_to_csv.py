from location.KGraph import get_locations_from_csv
from location.KGraph import sort_Locations
from location.KGraph import find_distances
from location.KGraph import store_distances
from preprocess.read_OS_topological import get_topological_info
import time

################################
# - reads locations.csv file
# - sorts the neighbors by latitude and longitude
# - gets the neighbors from the topological file
# - computes the distances for each location's closest neighbors
# - stores the distances of each location with its neighbors in
#   datasets/window_size_W/distances where W is the size of sliding window
################################
# from preprocess import get_csv
if __name__ == "__main__":
    start = time.time()

##################
#   find and store distances for all locations
#    vectors_type = 1
##################
    # weighted_graph = get_locations_from_csv("../datasets/locations_csv/locations.csv")
    # # weighted_graph.print_statistics()
    #
    # print("sort locations_csv")
    # sort_Locations(weighted_graph)
    # # weighted_graph.print_statistics()
    #
    # print("read topological")
    # get_topological_info(weighted_graph)
    # weighted_graph.print_statistics()
    #
    # print("find distances")
    # find_distances(weighted_graph)
    # weighted_graph.print_statistics()
    #
    # print("store distances")
    # vectors_type = 1
    # store_distances(weighted_graph, vectors_type)
    # weighted_graph.print_statistics()

##################
#   find and store distances for smaller location dataset
#   vectors_type = 2
##################
    weighted_graph = get_locations_from_csv("../datasets/locations_csv/locations_2.csv")
    # weighted_graph.print_statistics()

    print("sort locations_csv")
    sort_Locations(weighted_graph)
    # weighted_graph.print_statistics()

    print("read topological")
    get_topological_info(weighted_graph)
    weighted_graph.print_statistics()

    print("find distances")
    find_distances(weighted_graph)
    weighted_graph.print_statistics()

    print("store distances")
    vectors_type = 2
    store_distances(weighted_graph, vectors_type, "center_distance")
    weighted_graph.print_statistics()

    end = time.time()
    print("Processor time (in seconds):", end)
    print("Time elapsed:", end - start)
