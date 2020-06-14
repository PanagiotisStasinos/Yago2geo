import numpy as np
import pandas as pd

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Activation
# from tensorflow.keras.layers. import Dense
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.optimizers import SGD
from tensorflow.keras.metrics import categorical_crossentropy

from tensorflow import feature_column
from tensorflow.keras import layers
from sklearn.model_selection import train_test_split
from network.read_datasets import df_to_dataset

#imports we know we'll need
import skopt
# !pip install scikit-optimize if  necessary
from skopt import gbrt_minimize, gp_minimize
from skopt.utils import use_named_args
from skopt.space import Real, Categorical, Integer

from tensorflow.python.keras import backend as K

import h5py
import matplotlib.pyplot as plt
import math
import time

# from network import bayesian_opt
from network import simple_nn

start = time.time()

# simple_nn.simple_nn_1()     # .62
simple_nn.simple_nn_2()     # .83
# simple_nn.simple_nn_3()     # 0.87
# simple_nn.simple_nn_4()     # 0.8276
# simple_nn.simple_nn_5()     # 0.91
# simple_nn.simple_nn_6()
# simple_nn.simple_nn_7()     # 0.98

# bayesian_opt.optimize()

end = time.time()
print("Processor time (in seconds):", end)
print("Time elapsed:", end - start)

exit(0)
