from tensorflow import feature_column
from tensorflow.keras import layers
from sklearn.model_selection import train_test_split
from network.read_datasets import df_to_dataset
import time

from network import simple_nn, compare

start = time.time()

# simple_nn.simple_nn_1()     # .62
# simple_nn.simple_nn_2()     # .83
# simple_nn.simple_nn_3()     # 0.87
# simple_nn.simple_nn_4()     # 0.8276
# simple_nn.simple_nn_5()     # 0.91
# simple_nn.simple_nn_6()
# simple_nn.simple_nn_7()     # 0.

compare.compare_1()

# bayesian_opt.optimize()

end = time.time()
print("Processor time (in seconds):", end)
print("Time elapsed:", end - start)

exit(0)
