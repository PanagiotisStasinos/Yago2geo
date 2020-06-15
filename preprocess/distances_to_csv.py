from locations_graph.KGraph import get_locations_from_csv
from locations_graph.KGraph import sort_Locations
from locations_graph.KGraph import find_distances
from locations_graph.KGraph import store_distances
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

    weighted_graph = get_locations_from_csv("/datasets/locations_csv/locations.csv")
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
