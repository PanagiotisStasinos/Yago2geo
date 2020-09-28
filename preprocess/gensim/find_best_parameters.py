import os

import pandas
from gensim.models import Word2Vec

import time
import utils
from location.KGraph import get_locations_from_csv, get_distances_from_csv

from preprocess.gensim.gensim_word2vec import skip_gram


###################
# for every location
#   save the embedding
#   save 10 closests neighbors
#
###################
def save_neighbors_and_vectors_1(locations, name_vectors, embeddings_size):
    neighbors = {}
    vectors = {}
    for curr_loc in locations:
        vectors[curr_loc] = name_vectors.get_vector(curr_loc)

        neighbors[curr_loc] = []
        result = name_vectors.similar_by_word(curr_loc)
        for n in result:
            neighbors[curr_loc].append(n[0])

    df1 = pandas.DataFrame.from_dict(neighbors, orient='index')
    df1.to_csv(folder_path + "/" + str(embeddings_size) + '/neighbors.csv', index=True)

    df2 = pandas.DataFrame.from_dict(vectors, orient='index')
    df2.to_csv(folder_path + "/" + str(embeddings_size) + '/vectors.csv', index=True)


def get_spatial_proximity(path1):
    df1 = pandas.read_csv(path1)
    count1 = 0
    total = 0
    for index, row in df1.iterrows():
        name = row.tolist()[0]
        neighbors = row.tolist()[1:]
        for temp in neighbors:
            if temp in w_graph.Locations[name].adjacency_list:
                count1 += 1
        total += len(neighbors)

    proximity_percentage = count1 / total
    print("in adjacency list ", proximity_percentage)
    return proximity_percentage


if __name__ == "__main__":
    start = time.time()

    w_graph = get_locations_from_csv("../../datasets/locations_csv/locations.csv")

    stats_dict = {}
    stats_dict["distance_type"] = []
    stats_dict["walk_window"] = []
    stats_dict["num_of_steps"] = []
    stats_dict["num_of_walks"] = []
    stats_dict["embedding"] = []
    stats_dict["embedding_vector_size"] = []
    stats_dict["embedding_window_size"] = []
    stats_dict["embedding_min_count"] = []
    stats_dict["embedding_noise_words"] = []
    stats_dict["proximity_percentage"] = []

    count = 0
    # for distance_type in ['center_distance', 'polygon_distance']:
    # for distance_type in ['polygon_distance']:
    for distance_type in ['center_distance']:
        # for w in ['30']:
        for w in ['10', '30', '50', '70']:
            temp_path = "../../datasets/" + distance_type + "/window_size_" + w + "/distances/distances.csv"
            if not os.path.exists(temp_path):
                print("distances don't exist")
                break
            get_distances_from_csv(w_graph, temp_path)
            for num_of_steps, num_of_walks in [('5', '10'), ('10', '5'), ('15', '3')]:
                path = "../../datasets/" + distance_type + "/window_size_" + w + "/" + num_of_steps + "steps_" \
                       + num_of_walks + "walks/"

                print(count, path)
                count += 1
                walks_file = path + "random_walks.csv"

                df = pandas.read_csv(walks_file)
                walks_list = df.values.tolist()

                folder_path = "/temp/"
                # if not os.path.exists(folder_path):
                #     os.mkdir(folder_path)
                print(folder_path)
                print(walks_file)

                # skip_gram
                # dimensions of the embeddings
                for size in [50, 100, 150]:
                    if not os.path.exists(folder_path + str(size) + "/"):
                        os.mkdir(folder_path + str(size) + "/")
                    for window_size in [5, 10, 15]:     # (min, max) sentence length (5, 15)
                        for min_count in [0, 5, 10]:    # word frequency, less than that will be ignored
                            for noise_words in [5, 10, 15, 20]:     # how many “noise words” should be drawn
                                # skip_gram(list_of_walks, embeddings_size, window_size, min_c, noise_words)
                                locs, word_vectors = skip_gram(folder_path, walks_list, size, window_size,
                                                               min_count, noise_words)
                                save_neighbors_and_vectors_1(locs, word_vectors, size)
                                prox = get_spatial_proximity(folder_path + str(size) + "/neighbors.csv")

                                stats_dict["distance_type"].append(distance_type)
                                stats_dict["walk_window"].append(w)
                                stats_dict["num_of_steps"].append(num_of_steps)
                                stats_dict["num_of_walks"].append(num_of_walks)
                                stats_dict["embedding"].append('skip_gram')
                                stats_dict["embedding_vector_size"].append(size)
                                stats_dict["embedding_window_size"].append(window_size)
                                stats_dict["embedding_min_count"].append(min_count)
                                stats_dict["embedding_noise_words"].append(noise_words)
                                stats_dict["proximity_percentage"].append(prox)
                break
            break
        break

    utils.show_exec_time(start)
    exit(0)
