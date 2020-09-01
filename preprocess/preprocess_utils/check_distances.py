import os
import time
import utils
import pandas as pd

if __name__ == "__main__":
    start = time.time()

    print("\n AVERAGE LENGTH: CURRENT_NAME + 2*( WINDOW_SIZE*(NEIGHBOR_NAME + DIST + DAMPENED_WEIGHT))  ")
    print("\t2*() , one for longitude and one for latitude  \n")

    # for distance_type in ["center_distance", "polygon_distance"]:
    # for distance_type in ["polygon_distance"]:
    for distance_type in ["center_distance"]:
        print("check distances")
        # for window_size in [10]:
        for window_size in [10, 30, 50, 70]:
            path = '../../datasets/' + distance_type + '/window_size_' + str(window_size) + '/distances/'
            print(path)
            if not os.path.exists(path):
                exit(-1)

            df = pd.read_csv(path + 'distances.csv')
            t_sum = 0
            count = 0
            for index, row in df.iterrows():
                t_sum += len(row)
                count += 1
            print(path + 'distances.csv')
            print("\t", count, " - average len ", t_sum/count)

            # break
    utils.show_exec_time(start)
