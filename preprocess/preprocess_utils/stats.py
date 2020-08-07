from location.KGraph import get_locations_from_csv

if __name__ == "__main__":

    weighted_graph = get_locations_from_csv("../../datasets/locations_csv/locations.csv")
    weighted_graph.get_statistics_csv("1")

    exit(0)
