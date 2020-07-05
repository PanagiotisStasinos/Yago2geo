from tensorflow import feature_column
from tensorflow.keras import layers
from sklearn.model_selection import train_test_split
from network.read_datasets import df_to_dataset
import time

from network import simple_nn, compare

start = time.time()

# simple_nn.simple_nn_1()     # .62
# simple_nn.simple_nn_2()     # .83
simple_nn.simple_nn_3()     # 0.87
# simple_nn.simple_nn_4()     # 0.8276
# simple_nn.simple_nn_5()     # 0.91
# simple_nn.simple_nn_6()
# simple_nn.simple_nn_7()     # 0.

# compare.compare_1()

# for distance_type in ["center_distance", "polygon_distance"]:
#     for vec in ["vectors_1", "vectors_2"]:
#         for w_size in range(11, 82, 10):
#             for k, p in [(2, 10), (10, 5)]:
#                 for d, v in [(0, 1), (1, 2), (2, 4), (3, 5), (4, 3)]:
#                     ven_len = p * k * v
#                     file = '../datasets/' + distance_type + '/' + vec + '/window_size_' + str(w_size) + \
#                            '/' + str(k) + 'steps_' + str(p) + 'walks/data' + str(d) + '_' + str(ven_len) + '.csv'
#                     try:
#                         f = open(file)
#                         print("exists\t\t", file)
#                         f.close()
#                     except IOError:
#                         print("DOESN'T EXISTS\t", file)


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
