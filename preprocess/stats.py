from location.KGraph import get_locations_from_csv
import time

if __name__ == "__main__":
    start = time.time()

    weighted_graph = get_locations_from_csv("../datasets/locations_csv/locations_1.csv")
    weighted_graph.get_statistics_csv("1")

    exit(0)
