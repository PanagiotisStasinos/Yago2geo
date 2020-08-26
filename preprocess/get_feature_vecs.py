import time
import pandas
import utils
from location.KGraph import get_locations_from_csv

if __name__ == "__main__":
    start = time.time()

    weighted_graph = get_locations_from_csv("../datasets/locations_csv/locations.csv")

    file = "../datasets/center_distance/window_size_11/3steps_3walks/vectors/neighbors.csv"
    df = pandas.read_csv(file)
    print(df.shape)
    neighbors_list = df.values.tolist()
    neighbors_dict = {}
    count = 0
    for temp_list in neighbors_list:
        # print(temp_list[0], "-", temp_list[1:])
        # print(len(temp_list[0]), " - ", len(temp_list[1:]))
        neighbors_dict[temp_list[0]] = temp_list[1:]
        count += 1
        # if count == 10:
        #     break

    feature_vectors_dict_0 = {}
    feature_vectors_dict_1 = {}
    count = 0
    for key, value in neighbors_dict.items():
        feature_vectors_dict_0[key] = []
        feature_vectors_dict_1[key] = []
        for neighbor in value:
            info = weighted_graph.get_location_info(neighbor)

            feature_vectors_dict_0[key].append(info['area'])
            feature_vectors_dict_0[key].append(utils.get_value_of_type(info['type']))
            feature_vectors_dict_0[key].append(info['OS_ID'])
            feature_vectors_dict_0[key].append(info['center'].x)
            feature_vectors_dict_0[key].append(info['center'].y)
            # feature_vectors_dict_0[key].append(neighbor)

            feature_vectors_dict_1[key].append(info['area'])
            feature_vectors_dict_1[key].append(info['center'].x)
            feature_vectors_dict_1[key].append(info['center'].y)

        feature_vectors_dict_0[key].append(utils.get_value_of_type(weighted_graph.get_os_type(key)))
        feature_vectors_dict_1[key].append(utils.get_value_of_type(weighted_graph.get_os_type(key)))
        count += 1
        # if count == 10:
        #     break
    print(len(feature_vectors_dict_0))
    print(len(feature_vectors_dict_1))
    path = "../datasets/center_distance/window_size_11/3steps_3walks/vectors/"
    df0 = pandas.DataFrame.from_dict(feature_vectors_dict_0, orient='index')
    df0.to_csv(path + 'feature_vectors_0.csv', index=True)

    df1 = pandas.DataFrame.from_dict(feature_vectors_dict_1, orient='index')
    df1.to_csv(path + 'feature_vectors_1.csv', index=True)

    utils.show_exec_time(start)
    exit(0)
