import os

import pandas
from gensim.models import Word2Vec
from gensim.test.utils import get_tmpfile

from location.KGraph import get_locations_from_csv, get_distances_from_csv

import time
import utils

if __name__ == "__main__":
    start = time.time()

    w_graph = get_locations_from_csv("../../datasets/locations_csv/locations.csv")

    f = open("spatial_proximity.txt", "a")

    stats_dict = {}
    stats_dict["distance_type"] = []
    stats_dict["walk_window"] = []
    stats_dict["num_of_steps"] = []
    stats_dict["num_of_walks"] = []
    stats_dict["embedding"] = []
    stats_dict["embedding_window"] = []
    stats_dict["category_percentage"] = []
    stats_dict["proximity_percentage"] = []

    for distance_type in ['center_distance', 'polygon_distance']:
        for w in ['10', '30', '50', '70']:
            temp_path = "../../datasets/" + distance_type + "/window_size_" + w + "/distances/distances.csv"
            if not os.path.exists(temp_path):
                print("distances don't exist")
                break
            get_distances_from_csv(w_graph, temp_path)
            for num_of_steps, num_of_walks in [('5', '10'), ('10', '5'), ('15', '3')]:
                for emb in ['cbow', 'skip_gram']:
                # for emb in ['skip_gram']:
                    for size in [50, 100, 150]:
                        path = "../../datasets/" + distance_type + "/window_size_" + w + "/" + num_of_steps + "steps_" \
                           + num_of_walks + "walks/" + emb + "/" + str(size) + "/neighbors.csv"

                        stats_dict["distance_type"].append(distance_type)
                        stats_dict["walk_window"].append(w)
                        stats_dict["num_of_steps"].append(num_of_steps)
                        stats_dict["num_of_walks"].append(num_of_walks)
                        stats_dict["embedding"].append(emb)
                        stats_dict["embedding_window"].append(size)

                        if not os.path.exists(path):
                            print(path, " DOESN'T EXIST")
                            f.write(path + " DOESN'T EXIST\n")
                            stats_dict["proximity_percentage"].append(-1)
                            stats_dict["category_percentage"].append(-1)
                        else:
                            print(path, " EXISTS")
                            f.write(path + " EXISTS\n")

                            df = pandas.read_csv(path)
                            count = 0
                            count1 = 0
                            total = 0
                            for index, row in df.iterrows():
                                name = row.tolist()[0]
                                neighbors = row.tolist()[1:]
                                # print(row.tolist())
                                # print(name, weighted_graph.get_os_type(name))
                                # print(len(neighbors), neighbors)
                                # i = 0
                                for temp in neighbors:
                                    if w_graph.get_os_type(name) == w_graph.get_os_type(temp):
                                        # index = neighbors.index(temp)
                                        # print(index)
                                        count += 1

                                for temp in neighbors:
                                    if temp in w_graph.Locations[name].adjacency_list:
                                        count1 += 1

                                total += len(neighbors)

                            category_percentage = count/total
                            proximity_percentage = count1/total

                            print(category_percentage)
                            print("in adjacency list ", proximity_percentage)

                            f.write("\t category : " + str(category_percentage) + "\n")
                            f.write("\t adjacency list : " + str(proximity_percentage) + "\n")

                            stats_dict["proximity_percentage"].append(proximity_percentage)
                            stats_dict["category_percentage"].append(category_percentage)

                        # break
                    # break
                # break
            # break
        # break

    file = "percentages.csv"
    df = pandas.DataFrame.from_dict(stats_dict)
    df.to_csv(file, index=False)

    f.close()

    utils.show_exec_time(start)
    exit(0)
