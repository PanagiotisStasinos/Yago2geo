from location.KGraph import get_locations_from_csv
from location.KGraph import sort_Locations
from location.KGraph import find_center_distances, find_polygon_distances
from location.KGraph import store_distances, get_polygon_distances
from read_files.read_OS_topological import get_topological_info
import time
import utils

################################
# - reads locations.csv file
# - sorts the neighbors by latitude and longitude
# - gets the neighbors from the topological file
# - computes the distances for each location's closest neighbors
# - stores the distances of each location with its neighbors in
#   datasets/window_size_W/distances where W is the size of sliding window
################################
if __name__ == "__main__":
    start = time.time()

##################
#
##################
    weighted_graph = get_locations_from_csv("../datasets/locations_csv/locations.csv")

    print("sort locations_csv")
    sort_Locations(weighted_graph)
    # weighted_graph.print_statistics()

    print("read topological")
    get_topological_info(weighted_graph)
    weighted_graph.print_statistics()

    # for distance_type in ["center_distance", "polygon_distance"]:
    # for distance_type in ["center_distance"]:
    for distance_type in ["polygon_distance"]:
        print("find distances")
        # for window_size in [10, 30, 50, 70]:
        # for window_size in [10]:
        for window_size in [30]:

            if distance_type == "center_distance":
                find_center_distances(weighted_graph, window_size)
            else:
                # get distances from smaller window
                # less estimation to be done
                if window_size == 30:
                    smaller_window_size = 10    # window_size = 30
                    get_polygon_distances(weighted_graph, window_size, smaller_window_size)
                elif window_size == 50:
                    smaller_window_size = 30  # window_size = 50
                    get_polygon_distances(weighted_graph, window_size, smaller_window_size)
                elif window_size == 70:
                    smaller_window_size = 50  # window_size = 70
                    get_polygon_distances(weighted_graph, window_size, smaller_window_size)

                find_polygon_distances(weighted_graph, window_size)

            print("store distances")
            store_distances(weighted_graph, distance_type, window_size)
            # break
    utils.show_exec_time(start)

