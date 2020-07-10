from tensorflow import feature_column
from tensorflow.keras import layers
from sklearn.model_selection import train_test_split
from network.read_datasets import df_to_dataset
import time
import pandas as pd

from network import simple_nn, compare, bayesian_opt

start = time.time()
columns = {"file": [],
           "distance_type": [],
           "OS_type category": [],
           "window size": [],
           "num_of_steps": [],
           "num_of_walks": [],
           "number_of_features": [],
           "vector_len": [],
           "number_of_file": [],
           "dim_learning_rate": [],
           "dim_num_dense_layers": [],
           "dim_num_input_nodes": [],
           "dim_num_dense_nodes": [],
           "dim_activation": [],
           "dim_batch_size": [],
           "dim_adam_decay": [],
           "best_accuracy": []}

temp_window_columns = {"file": [],
                       "distance_type": [],
                       "OS_type category": [],
                       "window size": [],
                       "num_of_steps": [],
                       "num_of_walks": [],
                       "number_of_features": [],
                       "vector_len": [],
                       "number_of_file": [],
                       "dim_learning_rate": [],
                       "dim_num_dense_layers": [],
                       "dim_num_input_nodes": [],
                       "dim_num_dense_nodes": [],
                       "dim_activation": [],
                       "dim_batch_size": [],
                       "dim_adam_decay": [],
                       "best_accuracy": []}

# simple_nn.simple_nn_1()     # .62
# simple_nn.simple_nn_2()     # .83
# simple_nn.simple_nn_3()     # 0.87
# simple_nn.simple_nn_4()     # 0.8276
# simple_nn.simple_nn_5()     # 0.91
# simple_nn.simple_nn_6()
# simple_nn.simple_nn_7()     # 0.

# compare.compare_1()
for distance_type in ["polygon_distance"]:
# for distance_type in ["center_distance"]:
# for distance_type in ["center_distance", "polygon_distance"]:

    # for vec in ["vectors_1", "vectors_2"]:
    for vec in ["vectors_2"]:
        # for w_size in [11, 21, 31, 41, 51, 61, 71, 81]:
        # for w_size in [21, 31, 41, 51, 61, 71, 81]:
        # for w_size in [81]:
        for w_size in [11]:
            for k, p in [(2, 10), (10, 5)]:
                # v = number of features
                # d = number_of_file
                for d, v in [(0, 1), (1, 2), (2, 4), (3, 5), (4, 3)]:
                    ven_len = p * k * v
                    file = '../datasets/' + distance_type + '/' + vec + '/window_size_' + str(w_size) + \
                           '/' + str(k) + 'steps_' + str(p) + 'walks/data' + str(d) + '_' + str(ven_len) + '.csv'
                    try:
                        f = open(file)
                        print("exists\t\t", file)
                        f.close()

                        # columns["file"].append(file)
                        # columns["distance_type"].append(distance_type)
                        # columns["OS_type category"].append(vec)
                        # columns["window size"].append(w_size)
                        # columns["num_of_steps"].append(k)
                        # columns["num_of_walks"].append(p)
                        # columns["number_of_features"].append(v)
                        # columns["vector_len"].append(ven_len)
                        # columns["number_of_file"].append(d)

                        temp_window_columns["file"].append(file)
                        temp_window_columns["distance_type"].append(distance_type)
                        temp_window_columns["OS_type category"].append(vec)
                        temp_window_columns["window size"].append(w_size)
                        temp_window_columns["num_of_steps"].append(k)
                        temp_window_columns["num_of_walks"].append(p)
                        temp_window_columns["number_of_features"].append(v)
                        temp_window_columns["vector_len"].append(ven_len)
                        temp_window_columns["number_of_file"].append(d)

                        X_train, y_train, input_shape_x = read_datasets.read_data(file)
                        result, best_accuracy = bayesian_opt.optimize(X_train, y_train, input_shape_x)

                        # columns["dim_learning_rate"].append(result.x[0])
                        # columns["dim_num_dense_layers"].append(result.x[1])
                        # columns["dim_num_input_nodes"].append(result.x[2])
                        # columns["dim_num_dense_nodes"].append(result.x[3])
                        # columns["dim_activation"].append(result.x[4])
                        # columns["dim_batch_size"].append(result.x[5])
                        # columns["dim_adam_decay"].append(result.x[6])
                        # columns["best_accuracy"].append(best_accuracy)

                        temp_window_columns["dim_learning_rate"].append(result.x[0])
                        temp_window_columns["dim_num_dense_layers"].append(result.x[1])
                        temp_window_columns["dim_num_input_nodes"].append(result.x[2])
                        temp_window_columns["dim_num_dense_nodes"].append(result.x[3])
                        temp_window_columns["dim_activation"].append(result.x[4])
                        temp_window_columns["dim_batch_size"].append(result.x[5])
                        temp_window_columns["dim_adam_decay"].append(result.x[6])
                        temp_window_columns["best_accuracy"].append(best_accuracy)

                    except IOError:
                        print("DOESN'T EXISTS\t", file)

                    print(file)
                    # break
                # break
            # break
            file = '../datasets/' + distance_type + '/' + vec + '/window_size_' + str(w_size) + \
                   '/best_hyperparameters.csv'
            df = pd.DataFrame.from_dict(temp_window_columns)
            df.to_csv(file, index=False)

            # empty temp_window_columns dict
            for key, value in temp_window_columns.items():
                temp_window_columns[key].clear()
        # break

# df = pd.DataFrame.from_dict(columns)
# df.to_csv('../best_hyperparameters.csv', index=False)

# path = '../datasets/center_distance/vectors_1/window_size_11/2steps_10walks/data4_60.csv'
# X_train, y_train = read_datasets.read_data(path)

# result = bayesian_opt.optimize(X_train, y_train)
# print(result.x)


end = time.time()
print("Processor time (in seconds):", end)
print("Time elapsed:", end - start)
total = end - start
minutes, secs = divmod(total, 60)
hours, minutes = divmod(minutes, 60)
print(hours, ' : ', minutes, ' : ', secs)

exit(0)
