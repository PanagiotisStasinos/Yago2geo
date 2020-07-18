import time
from statistics import mean

import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np


def auto_label(rects):
    for idx, rect in enumerate(bar_plot):
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width() / 2., 0.5 * height,
                bar_label[idx],
                ha='center', va='bottom', rotation=90)


# https://matplotlib.org/3.2.2/gallery/lines_bars_and_markers/barchart.html#sphx-glr-gallery-lines-bars-and-markers-barchart-py
def autolabel(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')


def plot_by_window(average_accuracy_by_window_size):
    labels = ['11', '21', '31', '41', '51', '61', '71', '81']
    max_acc = []
    average = []
    for w in [11, 21, 31, 41, 51, 61, 71, 81]:
        average.append(mean(average_accuracy_by_window_size[w]))
        max_acc.append(max(average_accuracy_by_window_size[w]))
    x = np.arange(len(labels))  # the label locations
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width / 2, max_acc, width, label='Max')
    rects2 = ax.bar(x + width / 2, average, width, label='Average')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Accuracy')
    plt.ylim(70.0, 100.0)
    ax.set_xlabel('Window size \n max accuracy ' + str(max(max_acc)) + ", window size " + str(labels[max_acc.index(max(max_acc))]))
    ax.set_title('Max and Average accuracy for each window size')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()

    autolabel(rects1)
    autolabel(rects2)
    fig.tight_layout()
    path = '../plots/win_plt.png'
    plt.savefig(path)
    plt.show()


def plot_by_distance_type(p_max, p_average, c_max, c_average):
    labels = ['polygon_distance', 'center_distance']
    max_acc = []
    average = []

    max_acc.append(p_max)
    max_acc.append(c_max)
    average.append(p_average)
    average.append(c_average)

    x = np.arange(len(labels))  # the label locations
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width / 2, max_acc, width, label='Max')
    rects2 = ax.bar(x + width / 2, average, width, label='Average')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Accuracy')
    plt.ylim(70.0, 100.0)
    ax.set_xlabel('Distance type \n max accuracy ' + str(max(max_acc)) + ", distance type : " + str(
        labels[max_acc.index(max(max_acc))]))
    ax.set_title('Max and Average accuracy for each distance type \n vectors_2 and window size 11')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()

    auto_label(rects1)
    auto_label(rects2)
    fig.tight_layout()
    path = '../plots/distance_plt.png'
    plt.savefig(path)
    plt.show()


def plot_by_location(vec_1, vec_2):
    labels = ['vectors_1', 'vectors_2']
    max_acc = []
    average = []

    temp_1 = [max(vec_1[w]) for w in [11, 21, 31, 41, 51, 61, 71, 81]]
    max_acc.append(max(temp_1))
    temp_2 = [max(vec_2[w]) for w in [11, 21, 31, 41, 51, 61, 71, 81]]
    max_acc.append(max(temp_2))

    m_1 = [mean(vec_1[w]) for w in [11, 21, 31, 41, 51, 61, 71, 81]]
    average.append(mean(m_1))
    m_2 = [mean(vec_2[w]) for w in [11, 21, 31, 41, 51, 61, 71, 81]]
    average.append(mean(m_2))

    x = np.arange(len(labels))  # the label locations
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width / 2, max_acc, width, label='Max')
    rects2 = ax.bar(x + width / 2, average, width, label='Average')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Accuracy')
    plt.ylim(70.0, 100.0)
    ax.set_xlabel('Vectors type \n max accuracy ' + str(max(max_acc)) + ", vectors type : " + str(
        labels[max_acc.index(max(max_acc))]))
    ax.set_title('Max and Average accuracy for each vector type ')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()

    auto_label(rects1)
    auto_label(rects2)
    fig.tight_layout()
    path = '../plots/vectors_plt.png'
    plt.savefig(path)
    plt.show()


def plot_by_nuf_of_steps_n_walks(average_accuracy_by_window_size):
    labels = ['(2,10)', '(10,5)']
    max_acc = []
    average = []

    k_2_p_10 = []
    k_10_p_5 = []
    for w in [11, 21, 31, 41, 51, 61, 71, 81]:
        k_2_p_10 = k_2_p_10 + average_accuracy_by_window_size[w][0:5]
        k_2_p_10 = k_2_p_10 + average_accuracy_by_window_size[w][10:15]
        k_10_p_5 = k_10_p_5 + average_accuracy_by_window_size[w][5:10]
        k_10_p_5 = k_10_p_5 + average_accuracy_by_window_size[w][15:20]

        print(average_accuracy_by_window_size[w])
        print("(2,10) : ", k_2_p_10)
        print("(10,5) : ", k_10_p_5)

    max_acc.append(max(k_2_p_10))
    max_acc.append((max(k_10_p_5)))

    average.append(mean(k_2_p_10))
    average.append((mean(k_10_p_5)))

    x = np.arange(len(labels))  # the label locations
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width / 2, max_acc, width, label='Max')
    rects2 = ax.bar(x + width / 2, average, width, label='Average')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Accuracy')
    plt.ylim(70.0, 100.0)
    ax.set_xlabel('Num of steps and walks \n max accuracy ' + str(max(max_acc)) + ", vectors type : " + str(
        labels[max_acc.index(max(max_acc))]))
    ax.set_title('Max and Average accuracy for each set of (num of steps, num of walks) ')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()

    auto_label(rects1)
    auto_label(rects2)
    fig.tight_layout()
    path = '../plots/steps_walks_plt.png'
    plt.savefig(path)
    plt.show()


def plot_by_feature(feature):
    labels = [0, 1, 2, 3, 4]
    max_acc = []
    average = []
    for f in [0, 1, 2, 3, 4]:
        average.append(mean(feature[f]))
        max_acc.append(max(feature[f]))
    x = np.arange(len(labels))  # the label locations
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width / 2, max_acc, width, label='Max')
    rects2 = ax.bar(x + width / 2, average, width, label='Average')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Accuracy')
    plt.ylim(50.0, 100.0)
    ax.set_xlabel('feature combination \n max accuracy ' + str(max(max_acc)) + ", feature combination " + str(labels[max_acc.index(max(max_acc))]))
    ax.set_title('Max and Average accuracy for each feature combination')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()

    autolabel(rects1)
    autolabel(rects2)
    fig.tight_layout()
    path = '../plots/feature_plt.png'
    plt.savefig(path)
    plt.show()

if __name__ == '__main__':
    start = time.time()

    # ###### 1
    # compare accuracy for vectors_1 and vectors_2
    # vec_1 contains all locations
    # 2 locations less, 2 os_categories less
    vec_1 = {}
    vec_2 = {}
    for w_size in [11, 21, 31, 41, 51, 61, 71, 81]:
        vec_1[w_size] = []
        vec_2[w_size] = []

    # ###### 2
    # check average max accuracy per window size
    average_accuracy_by_window_size = {}
    for w_size in [11, 21, 31, 41, 51, 61, 71, 81]:
        average_accuracy_by_window_size[w_size] = []

    # ###### 3
    # check average for different   num_of_walks
    #                               num_of_steps
    #                               features
    average_accuracy_by_vector_len = {}
    for vector_len in range(0, 10):
        average_accuracy_by_vector_len[vector_len] = 0.0
    count1 = 0

    # ###### 4
    # compare accuracy for vectors_1 and vectors_2
    feature = {}
    for feature_type in [0, 1, 2, 3, 4]:
        feature[feature_type] = []

    for distance_type in ["center_distance"]:
        for vec in ["vectors_1", "vectors_2"]:
            # count = count + 1
            for w_size in [11, 21, 31, 41, 51, 61, 71, 81]:
                count1 = count1 + 1
                if os.path.exists('../datasets/' + distance_type + '/' + vec + '/window_size_' + str(w_size) + '/'):
                    file = '../datasets/' + distance_type + '/' + vec + '/window_size_' + str(w_size) + \
                           '/best_hyperparameters.csv'
                    df = pd.read_csv(file)

                    accuracy = []
                    X = []
                    png_path = '../datasets/' + distance_type + '/' + vec + '/window_size_' + str(w_size) + '/plot.png'
                    for index, row in df.iterrows():
                        current_file = row['file']
                        current_distance_type = row['distance_type']
                        current_OS_type_category = row['OS_type category']
                        current_window_size = row['window size']
                        current_num_of_steps = row['num_of_steps']
                        current_num_of_walks = row['num_of_walks']
                        current_number_of_features = row['number_of_features']
                        current_vector_len = row['vector_len']
                        current_number_of_file = row['number_of_file']
                        current_dim_learning_rate = row['dim_learning_rate']
                        current_dim_num_dense_layers = row['dim_num_dense_layers']
                        current_dim_num_input_nodes = row['dim_num_input_nodes']
                        current_dim_num_dense_nodes = row['dim_num_dense_nodes']
                        current_dim_activation = row['dim_activation']
                        current_dim_batch_size = row['dim_batch_size']
                        current_dim_adam_decay = row['dim_adam_decay']
                        current_best_accuracy = row['best_accuracy']

                        average_accuracy_by_vector_len[index] = average_accuracy_by_vector_len[index] + \
                                                                current_best_accuracy
                        feature[index % 5].append(current_best_accuracy)
                        average_accuracy_by_window_size[w_size].append(current_best_accuracy)

                        if vec == 'vectors_1':
                            vec_1[w_size].append(current_best_accuracy)
                        else:
                            vec_2[w_size].append(current_best_accuracy)

                        if '../datasets/' + distance_type + '/' + vec + '/window_size_' + str(w_size) + '/' in current_file:
                            current_file = current_file.replace('../datasets/' + distance_type + '/' + vec +
                                                                '/window_size_' + str(w_size) + '/', '')
                        X.append(current_file)
                        # X.append(str(current_number_of_file) + str(current_number_of_features))
                        accuracy.append(current_best_accuracy)

                    # fig = plt.figure(figsize=(10, 5))
                    # # creating the bar plot
                    # plt.bar(X, accuracy, color='maroon',
                    #         width=0.4)
                    # plt.xlabel("files")
                    # plt.ylabel("accuracy")
                    # plt.title("Accuracy Bar plot")
                    # plt.xticks(rotation=90)
                    # fig.text = X
                    # plt.savefig(png_path)
                    # plt.show()

                    fig, ax = plt.subplots()

                    bar_x = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
                    bar_height = accuracy
                    bar_tick_label = ['C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9']
                    bar_label = accuracy

                    bar_plot = plt.bar(bar_x, bar_height, tick_label=bar_tick_label)
                    auto_label(bar_plot)

                    plt.ylim(0.0, 100.0)

                    plt.title('Add text for each bar with matplotlib')

                    plt.savefig(png_path, bbox_inches='tight')
                    plt.show()

                    # plt.bar(X, accuracy, width = 0.6)
                    # plt.show()
                    # break     # w_size
                # if dir exists
            # break   # vector_type
        # break     # distance_type

    plot_by_window(average_accuracy_by_window_size)
    print("ACCURACY PER WINDOW SIZE")
    for w_size in [11, 21, 31, 41, 51, 61, 71, 81]:
        print(average_accuracy_by_window_size[w_size])
        print(average_accuracy_by_window_size[w_size][:5])
        print(average_accuracy_by_window_size[w_size][5:10])
        print(average_accuracy_by_window_size[w_size][10:15])
        print(average_accuracy_by_window_size[w_size][15:20])
        print("Window_Size ", w_size, " average accuracy ", mean(average_accuracy_by_window_size[w_size]))
        print("\t\t\t\tmax accuracy ", max(average_accuracy_by_window_size[w_size]), "(",
              average_accuracy_by_window_size[w_size].index(max(average_accuracy_by_window_size[w_size])), ")")
        print()


    print("ACCURACY BY VECTOR LENGTH")
    print(count1)
    for vector_len in range(0, 10):
        print("vector length ", vector_len, " average accuracy ", average_accuracy_by_vector_len[vector_len] / count1)
    print()

    plot_by_location(vec_1, vec_2)
    print("ACCURACY BY locations")
    c1 = 0
    c2 = 0
    sum1 = 0
    sum2 = 0
    for w_size in [11, 21, 31, 41, 51, 61, 71, 81]:
        print("WINDOW_SIZE ", w_size)
        print(vec_1[w_size])
        print(vec_2[w_size])
        c1 = 0
        c2 = 0
        sum1 = 0
        sum2 = 0
        for i in range(0, len(vec_1)):
            if vec_1[w_size][i] > vec_2[w_size][i]:
                print("vec_1 :", vec_1[w_size][i] - vec_2[w_size][i])
                c1 = c1 + 1
                sum1 = sum1 + vec_1[w_size][i] - vec_2[w_size][i]
            elif vec_1[w_size][i] < vec_2[w_size][i]:
                print("vec_2 :", vec_2[w_size][i] - vec_1[w_size][i])
                c2 = c2 + 1
                sum2 = sum2 + vec_2[w_size][i] - vec_1[w_size][i]
            else:
                print("equal")
        print("vec_1 ", c1, " - vec_2 ", c2)
        print("sum1 ", sum1, " - sum2 ", sum2)
        print()


    plot_by_feature(feature)
    print("\nACCURACY BY FEATURE")
    for feature_type in [0, 1, 2, 3, 4]:
        print(feature[feature_type])
        print(feature_type, " ", mean(feature[feature_type]), " - ", max(feature[feature_type]))
        print()

    plot_by_nuf_of_steps_n_walks(average_accuracy_by_window_size)


# #################################
#
#   POLYGON DISTANCE
#
# #################################
    # ###### 1
    accuracy_list = []

    if os.path.exists('../datasets/polygon_distance/vectors_2/window_size_11/'):
        file = '../datasets/polygon_distance/vectors_2/window_size_11/best_hyperparameters.csv'
        df = pd.read_csv(file)

        X = []
        png_path = '../datasets/polygon_distance/vectors_2/window_size_11/plot.png'
        for index, row in df.iterrows():
            current_file = row['file']
            current_distance_type = row['distance_type']
            current_OS_type_category = row['OS_type category']
            current_window_size = row['window size']
            current_num_of_steps = row['num_of_steps']
            current_num_of_walks = row['num_of_walks']
            current_number_of_features = row['number_of_features']
            current_vector_len = row['vector_len']
            current_number_of_file = row['number_of_file']
            current_dim_learning_rate = row['dim_learning_rate']
            current_dim_num_dense_layers = row['dim_num_dense_layers']
            current_dim_num_input_nodes = row['dim_num_input_nodes']
            current_dim_num_dense_nodes = row['dim_num_dense_nodes']
            current_dim_activation = row['dim_activation']
            current_dim_batch_size = row['dim_batch_size']
            current_dim_adam_decay = row['dim_adam_decay']
            current_best_accuracy = row['best_accuracy']

            accuracy_list.append(current_best_accuracy)


            if '../datasets/polygon_distance/vectors_2/window_size_11/' in current_file:
                current_file = current_file.replace('../datasets/polygon_distance/vectors_2/window_size_11/', '')
            X.append(current_file)

        fig, ax = plt.subplots()

        bar_x = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        bar_height = accuracy_list
        bar_tick_label = ['C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9']
        bar_label = accuracy_list

        bar_plot = plt.bar(bar_x, bar_height, tick_label=bar_tick_label)
        auto_label(bar_plot)

        plt.ylim(0.0, 100.0)

        plt.title('Add text for each bar with matplotlib')

        plt.savefig(png_path, bbox_inches='tight')
        plt.show()


        p_max = max(accuracy_list)
        p_average = mean(accuracy_list)
        c_max = max(average_accuracy_by_window_size[w_size][10:20])
        c_average = mean(average_accuracy_by_window_size[w_size][10:20])
        plot_by_distance_type(p_max, p_average, c_max, c_average)

    end = time.time()
    print("Processor time (in seconds):", end)
    print("Time elapsed:", end - start)
    total = end - start
    minutes, secs = divmod(total, 60)
    hours, minutes = divmod(minutes, 60)
    print(hours, ' : ', minutes, ' : ', secs)
