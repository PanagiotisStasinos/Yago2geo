import os
import time

import pandas

import utils


def check(fold_path):
    for size in [50, 100, 150]:
        p = fold_path + str(size) + '/'
        print("\t", p)
        if not os.path.exists(p):
            print("doesn't exist")
        else:
            print("exists")

            df1 = pandas.read_csv(p + "neighbors.csv")
            print("neighbors ", len(df1.values.tolist()), len(df1.values.tolist()[0]))

            df2 = pandas.read_csv(p + "vectors.csv")
            print("vectors ", len(df2.values.tolist()), len(df2.values.tolist()[0]))


if __name__ == "__main__":
    start = time.time()

    count = 0
    # for distance_type in ['center_distance', 'polygon_distance']:
    for distance_type in ['center_distance']:
        for w in ['10', '30', '50', '70']:
            for num_of_steps, num_of_walks in [('5', '10'), ('10', '5'), ('15', '3')]:
                path = "../../datasets/" + distance_type + "/window_size_" + w + "/" + num_of_steps + "steps_" \
                       + num_of_walks + "walks/"

                folder_path = path + "skip_gram/"
                check(folder_path)

                folder_path = path + "cbow/"
                check(folder_path)

    utils.show_exec_time(start)
    exit(0)
