import os
import time
import utils
import pandas as pd

if __name__ == "__main__":
    start = time.time()

    for distance_type in ['center_distance']:
        for window_size in [10, 30, 50, 70]:
            for num_of_steps, num_of_walks in [(5, 10), (10, 5), (15, 3)]:
                file = '../../datasets/' + distance_type + '/window_size_' + str(window_size) + '/' + str(num_of_steps) \
                       + 'steps_' + str(num_of_walks) + 'walks/random_walks.csv'
                print(file)
                if not os.path.exists(file):
                    exit(-1)

                df = pd.read_csv(file)
                t_sum = 0
                count = 0
                for index, row in df.iterrows():
                    t_sum += len(row)
                    count += 1
                print("\t", count, " - average len ", t_sum / count)
            # break

    utils.show_exec_time(start)
