#####################################
#   https://towardsdatascience.com/a-beginners-guide-to-word-embedding-with-gensim-word2vec-model-5970fa56cc92
#   https://radimrehurek.com/gensim/models/word2vec.html
#
####################################
import os

import pandas
from gensim.models import Word2Vec
from gensim.test.utils import get_tmpfile

from location.KGraph import get_locations_from_csv

import time
import utils


def skip_gram(path1, list_of_walks, embeddings_size, window_size, min_c, noise_words):
    # path4 = get_tmpfile("word2vec.model")
    # print("path4 ", path4)
    # print("folder_path ", path1)

    # size: The number of dimensions of the embeddings and the default is 100.
    # window: The maximum distance between a target word and words around the target word.
    #           The default window is 5.
    # min_count: The minimum count of words to consider when training the model; words with occurrence
    #     less than this count will be ignored.The default for min_count is 5.
    # workers: The number of partitions during training and the default workers is 3.
    # sg: The training algorithm, either CBOW(0) or skip gram(1). The default training algorithm is CBOW.
    # hs ({0, 1}, optional) – If 1, hierarchical softmax will be used for model training.
    #     If 0, and negative is non-zero, negative sampling will be used.
    # negative (int, optional) – If > 0, negative sampling will be used,
    #     the int for negative specifies how many “noise words” should be drawn (usually between 5-20).
    #     If set to 0, no negative sampling is used.
    model = Word2Vec(list_of_walks, size=embeddings_size, window=window_size, min_count=min_c, workers=4, sg=1,
                     hs=0, negative=noise_words)
    model.save(path1 + str(embeddings_size) + "/"
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
    model = Word2Vec(list_of_walks, size=embeddings_size, window=5, min_count=5, workers=4, sg=0)
    model.save(folder_path + str(embeddings_size) + "/"
               + "word2vec.model")  # model = Word2Vec.load(path + "word2vec.model")

    word_vectors = model.wv
    # print(str(type(word_vectors)))
    locs = word_vectors.index2entity
    # print(str(type(locs)))
    # print(len(locs))

    return locs, word_vectors


###################
# for every location
#   save the embedding
#   save 10 closests neighbors
#
###################
def save_neighbors_and_vectors(locations, name_vectors, embeddings_size):
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


if __name__ == "__main__":
    start = time.time()

    count = 0
    # for distance_type in ['center_distance', 'polygon_distance']:
    # for distance_type in ['center_distance']:
    for distance_type in ['polygon_distance']:
        # for w in ['10', '30', '50', '70']:
        for w in ['30']:
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
                    locs, word_vectors = skip_gram(folder_path, walks_list, size, 20, 5, 5)
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

        #         break
        #     break
        # break
    utils.show_exec_time(start)
    exit(0)
