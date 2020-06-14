from preprocess.KGraph import get_locations_from_csv
from preprocess.KGraph import sort_Locations
from preprocess.KGraph import find_distances
from preprocess.KGraph import store_distances
from preprocess.random_walk import store_random_walks
from preprocess.random_walk import store_random_walks2
from preprocess.read_OS_topological import get_topological_statistics
from preprocess.read_OS_topological import get_topological_info
import time

################################
# reads extented and new files
# creates a graph with all locations_csv
#
################################
# from preprocess import get_csv
if __name__ == "__main__":
    start = time.time()

    weighted_graph = get_locations_from_csv("/datasets/locations_csv/locations_1.csv")
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
    store_distances(weighted_graph)
    weighted_graph.print_statistics()

    end = time.time()
    print("Processor time (in seconds):", end)
    print("Time elapsed:", end - start)
