import time
import pandas
import utils
from scipy.spatial import distance


def find_closest_neighbors(vec_dict):
    closest_neighbors = {}
    n_count = 0
    for key1, value1 in vec_dict.items():
        closest_neighbors[key1] = []
        temp_neighbor_dict = {}
        for key2, value2 in vec_dict.items():
            if key1 != key2:
                temp_neighbor_dict[key2] = distance.cosine(value1, value2)
        temp_neighbor_dict = {k: v for k, v in sorted(temp_neighbor_dict.items(), key=lambda item: item[1])}
        # print(len(temp_neighbor_dict))
        # print(temp_neighbor_dict)
        count = 0
        for k, v in temp_neighbor_dict.items():
            closest_neighbors[key1].append(k)
            count += 1
            if count == 10:
                break
        # print(len(closest_neighbors[key1]), closest_neighbors[key1])
        n_count += 1
        if n_count % 100 == 0:
            print(n_count)
            # break

        # exit(-1)
    return closest_neighbors


if __name__ == "__main__":
    start = time.time()

    file = "../datasets/center_distance/window_size_11/3steps_3walks/vectors/skip_gram_vectors.csv"
    df = pandas.read_csv(file)
    # print(df.shape)
    vectors_list = df.values.tolist()
    # print(len(vectors_list[0]))
    # print(vectors_list[0])
    # print(len(vectors_list[0][:0]), " - ", vectors_list[0][0])
    # print(len(vectors_list[0][1:]), " - ", vectors_list[0][1:])

    vectors_dict = {}
    for temp_list in vectors_list:
        # print(temp_list[0], "-", temp_list[1:])
        vectors_dict[temp_list[0]] = temp_list[1:]

    # cosine similarity to get neighbors
    neighbors = find_closest_neighbors(vectors_dict)
    # print(str(type(neighbors)))
    # print(len(neighbors))

    path = "../datasets/center_distance/window_size_11/3steps_3walks/vectors/"
    df1 = pandas.DataFrame.from_dict(neighbors, orient='index')
    df1.to_csv(path + 'neighbors.csv', index=True)

    utils.show_exec_time(start)
    exit(0)





