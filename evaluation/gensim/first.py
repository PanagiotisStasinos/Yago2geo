import time
import utils
from evaluation.evaluation_utils.read_vectors import get_train_set


if __name__ == "__main__":
    start = time.time()

    X, Y = get_train_set("../../datasets/center_distance/window_size_11/3steps_3walks/gensim/feature_vectors_1.csv")
    print("X", X.shape)
    print("Y", Y.shape)

    utils.show_exec_time(start)
    exit(0)
