from location.KGraph import find_distances, get_distances_from_csv
from preprocess.random_walk import store_random_walks
from preprocess.random_walk import store_random_walks2
from preprocess.read_OS_topological import get_statistics_of_topological_and_matches_files
from preprocess.read_OS_topological import get_topological_info
from location.KGraph import get_locations_from_csv
import time

if __name__ == "__main__":
    start = time.time()

    weighted_graph = get_locations_from_csv("../datasets/locations_csv/locations_2.csv")
    get_distances_from_csv(weighted_graph,
                           "../datasets/center_distance/vectors_2/window_size_51/distances/distances_lat.csv",
                           "../datasets/center_distance/vectors_2/window_size_51/distances/distances_lon.csv")
    weighted_graph.print_statistics()

    end = time.time()
    print("Processor time (in seconds):", end)
    print("Time elapsed:", end - start)
