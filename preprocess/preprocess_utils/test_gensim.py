import pandas
from gensim.models import Word2Vec
from gensim.test.utils import get_tmpfile

from location.KGraph import get_locations_from_csv


weighted_graph = get_locations_from_csv("../../datasets/locations_csv/locations.csv")

file = "../../datasets/center_distance/window_size_11/3steps_3walks/random_walks.csv"
df = pandas.read_csv(file)
print(df.shape)

walks = df.values.tolist()
print(len(walks))

path1 = get_tmpfile("word2vec.model")
model = Word2Vec(walks, size=100, window=5, min_count=1, workers=4)
path = "../../datasets/center_distance/window_size_11/3steps_3walks/gensim/"
model.save(path + "word2vec.model")
# model = Word2Vec.load(path + "word2vec.model")

word_vectors = model.wv
print(str(type(word_vectors)))
locs = word_vectors.index2entity
print(str(type(locs)))
print(len(locs))

neighbors = {}
vectors = {}
for curr_loc in locs:
    # vectors[curr_loc] =  ################################

    neighbors[curr_loc] = []
    result = word_vectors.similar_by_word(curr_loc)
    # print("Most similar to geoentity_Benington_7295471 :\n", result[:3])

    weighted_graph.print_loc_info(curr_loc)
    for n in result:
        neighbors[curr_loc].append(n[0])
        weighted_graph.print_loc_info(n[0])

# path = "../../datasets/center_distance/window_size_11/3steps_3walks/"
df1 = pandas.DataFrame.from_dict(neighbors, orient='index')
df1.to_csv(path + 'gensim_neighbors.csv', index=True)
