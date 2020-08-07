import time
import os
from preprocess.preprocess_utils import DeepWalk


if __name__ == "__main__":
    start = time.time()

    for distance_type in ['center_distance'
                          # , 'polygon_distance'
                          ]:

        for window_size in [11
            , 31
            , 51
                            ]:

            for num_of_steps, num_of_walks in [(5, 10), (10, 5), (15, 3)]:
                file = '../datasets/' + distance_type + '/window_size_' + str(window_size) + '/' + str(
                    num_of_steps) + 'steps_' + str(num_of_walks) + 'walks/random_walks.csv'

                if os.path.exists(file):
                    print("file exists")

                    DeepWalk.skip_gram(file)
                    exit(-2)
                else:
                    print("No random walks")

    exit(0)
