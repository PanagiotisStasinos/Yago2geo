#####################################
#   https://towardsdatascience.com/a-beginners-guide-to-word-embedding-with-gensim-word2vec-model-5970fa56cc92
#
#
####################################
import os

import pandas
from gensim.models import Word2Vec
from gensim.test.utils import get_tmpfile

from location.KGraph import get_locations_from_csv

import time
import utils


def skip_gram(list_of_walks, embeddings_size):
    # path4 = get_tmpfile("word2vec.model")
    # print("path4 ", path4)
    # print("folder_path ", folder_path)

    # size: The number of dimensions of the embeddings and the default is 100.
    # window: The maximum distance between a target word and words around the target word.
    #           The default window is 5.
    # min_count: The minimum count of words to consider when training the model; words with occurrence
    #     less than this count will be ignored.The default for min_count is 5.
    # workers: The number of partitions during training and the default workers is 3.
    # sg: The training algorithm, either CBOW(0) or skip gram(1). The default training algorithm is CBOW.
    model = Word2Vec(list_of_walks, size=embeddings_size, window=5, min_count=5, workers=3, sg=1)
    model.save(folder_path + str(embeddings_size)
               + "/word2vec.model")  # model = Word2Vec.load(path + "word2vec.model")

    word_vectors = model.wv
    # print(str(type(word_vectors)))
    locs = word_vectors.index2entity
    # print(str(type(locs)))
    # print(len(locs))

    return locs, word_vectors


def cbow(list_of_walks, embeddings_size):
    # path4 = get_tmpfile("word2vec.model")
    # print("path4 ", path4)
    # print("folder_path ", folder_path)

    # size: The number of dimensions of the embeddings and the default is 100.
    # window: The maximum distance between a target word and words around the target word.
    #           The default window is 5.
    # min_count: The minimum count of words to consider when training the model; words with occurrence
    #     less than this count will be ignored.The default for min_count is 5.
    # workers: The number of partitions during training and the default workers is 3.
    # sg: The training algorithm, either CBOW(0) or skip gram(1). The default training algorithm is CBOW.
    model = Word2Vec(list_of_walks, size=embeddings_size, window=5, min_count=5, workers=3, sg=0)
    model.save(folder_path + str(embeddings_size)
               + "word2vec.model")  # model = Word2Vec.load(path + "word2vec.model")

    word_vectors = model.wv
    # print(str(type(word_vectors)))
    locs = word_vectors.index2entity
    # print(str(type(locs)))
    # print(len(locs))

    return locs, word_vectors


def save_neighbors_and_vectors(locations, rename_vectors, embeddings_size):
    neighbors = {}
    vectors = {}
    for curr_loc in locations:
        vectors[curr_loc] = rename_vectors.get_vector(curr_loc)

        neighbors[curr_loc] = []
        result = rename_vectors.similar_by_word(curr_loc)
        # print("Most similar to geoentity_Benington_7295471 :\n", result[:3])

        # weighted_graph.print_loc_info(curr_loc)
        for n in result:
            neighbors[curr_loc].append(n[0])
            # weighted_graph.print_loc_info(n[0])

    # folder_path = "../../datasets/center_distance/window_size_w/ksteps_pwalks/.../"
    df1 = pandas.DataFrame.from_dict(neighbors, orient='index')
    df1.to_csv(folder_path + "/" + str(embeddings_size) + '/neighbors.csv', index=True)

    df2 = pandas.DataFrame.from_dict(vectors, orient='index')
    df2.to_csv(folder_path + "/" + str(embeddings_size) + '/vectors.csv', index=True)


if __name__ == "__main__":
    start = time.time()

    # weighted graph used for debug
    # weighted_graph = get_locations_from_csv("../../datasets/locations_csv/locations.csv")

    count = 0
    # for distance_type in ['center_distance', 'polygon_distance']:
    for distance_type in ['center_distance']:
        for w in ['10', '30', '50', '70']:
            for num_of_steps, num_of_walks in [('5', '10'), ('10', '5'), ('15', '3')]:
                path = "../../datasets/" + distance_type + "/window_size_" + w + "/" + num_of_steps + "steps_" \
                       + num_of_walks + "walks/"

                print(count, path)
                count += 1
                walks_file = path + "random_walks.csv"

                df = pandas.read_csv(walks_file)
                # print(df.shape)
                walks_list = df.values.tolist()
                # print(len(walks_list))

                folder_path = path + "skip_gram/"
                if not os.path.exists(folder_path):
                    os.mkdir(folder_path)
                print(folder_path)
                print(walks_file)

                # skip_gram
                # dimensions of the embeddings
                for size in [50, 100, 150]:
                    if not os.path.exists(folder_path + str(size) + "/"):
                        os.mkdir(folder_path + str(size) + "/")
                    locs, word_vectors = skip_gram(walks_list, size)
                    save_neighbors_and_vectors(locs, word_vectors, size)

                folder_path = path + "cbow/"
                if not os.path.exists(folder_path):
                    os.mkdir(folder_path)
                print(folder_path)
                print(walks_file)

                # CBOW
                # dimensions of the embeddings
                for size in [50, 100, 150]:
                    if not os.path.exists(folder_path + str(size) + "/"):
                        os.mkdir(folder_path + str(size) + "/")
                    locs, word_vectors = cbow(walks_list, size)
                    save_neighbors_and_vectors(locs, word_vectors, size)

                break
            break
        break
    utils.show_exec_time(start)
    exit(0)
