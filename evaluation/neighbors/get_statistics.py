import os

import pandas
from gensim.models import Word2Vec
from gensim.test.utils import get_tmpfile

from location.KGraph import get_locations_from_csv, get_distances_from_csv

import time
import utils


def print_line(index_line):
    print(percentages_dict["distance_type"][index_line],
          percentages_dict["walk_window"][index_line],
          percentages_dict["num_of_steps"][index_line],
          percentages_dict["num_of_walks"][index_line],
          percentages_dict["embedding"][index_line],
          percentages_dict["embedding_window"][index_line],
          percentages_dict["category_percentage"][index_line],
          percentages_dict["proximity_percentage"][index_line])


def print_center_type(window_size):
    center_dist_proximity_sum = 0
    center_count = 0
    polygon_dist_proximity_sum = 0
    polygon_count = 0
    for line_index in range(len(percentages_dict["proximity_percentage"])):
        if percentages_dict["walk_window"][line_index] == window_size:
            if percentages_dict["distance_type"][line_index] == "center_distance":
                center_dist_proximity_sum += percentages_dict["proximity_percentage"][line_index]
                center_count += 1
            else:
                polygon_dist_proximity_sum += percentages_dict["proximity_percentage"][line_index]
                polygon_count += 1
            # print_line(line_index)
    print(window_size, " center ", center_dist_proximity_sum / center_count)
    print(window_size, " polygon ", polygon_dist_proximity_sum / polygon_count)


def print_walk_window(window_size, dist_type):
    proximity_sum = 0
    count = 0
    for line_index in range(len(percentages_dict["proximity_percentage"])):
        if percentages_dict["walk_window"][line_index] == window_size:
            if percentages_dict["distance_type"][line_index] == dist_type:
                proximity_sum += percentages_dict["proximity_percentage"][line_index]
                count += 1
    print(window_size, " ", dist_type, " ", proximity_sum / count)


def print_steps_walks(steps, walks, dist_type):
    proximity_sum = 0
    count = 0
    for line_index in range(len(percentages_dict["proximity_percentage"])):
        if percentages_dict["distance_type"][line_index] == dist_type:
            if percentages_dict["num_of_steps"][line_index] == steps:
                proximity_sum += percentages_dict["proximity_percentage"][line_index]
                count += 1
    print(dist_type, " (", steps, ", ", walks, ") ", proximity_sum / count)


def print_embedding_window(emb_win, dist_type):
    proximity_sum = 0
    count = 0
    for line_index in range(len(percentages_dict["proximity_percentage"])):
        if percentages_dict["distance_type"][line_index] == dist_type:
            if percentages_dict["embedding_window"][line_index] == emb_win:
                proximity_sum += percentages_dict["proximity_percentage"][line_index]
                count += 1
    print(dist_type, " ", emb_win, " ", proximity_sum / count)


if __name__ == "__main__":
    start = time.time()

    df = pandas.read_csv("percentages.csv")
    percentages_dict = df.to_dict()

    temp_cat = percentages_dict["category_percentage"]
    temp_walk_window = percentages_dict["walk_window"]

    temp_prox = percentages_dict["proximity_percentage"]
    print(str(type(temp_prox)))
    print(temp_prox)

    # max proximity
    index = max(temp_prox, key=temp_prox.get)  # get key of max proximity_percentage
    print(index, " - ", temp_cat[index], " - ", temp_prox[index])
    print_line(index)

    # max category
    index = max(temp_cat, key=temp_cat.get)  # get key of max category_percentage
    print(index, " - ", temp_cat[index], " - ", temp_prox[index])
    print_line(index)

    # best distance_type
    # check only for window sizes of 10 and 30
    win_size = 10
    print_center_type(win_size)

    win_size = 30
    print_center_type(win_size)

    # best walk window size
    # center_distance
    print_walk_window(10, "center_distance")
    print_walk_window(30, "center_distance")
    print_walk_window(50, "center_distance")
    print_walk_window(70, "center_distance")

    # best (num_of_steps, num_of_walks)
    # center_distance
    print_steps_walks(5, 10, "center_distance")
    print_steps_walks(10, 5, "center_distance")
    print_steps_walks(15, 3, "center_distance")
    # polygon_distance
    print_steps_walks(5, 10, "polygon_distance")
    print_steps_walks(10, 5, "polygon_distance")
    print_steps_walks(15, 3, "polygon_distance")

# best embedding window size
    print_embedding_window(50, "center_distance")
    print_embedding_window(100, "center_distance")
    print_embedding_window(150, "center_distance")
    print_embedding_window(50, "polygon_distance")
    print_embedding_window(100, "polygon_distance")
    print_embedding_window(150, "polygon_distance")

    utils.show_exec_time(start)
    exit(0)
