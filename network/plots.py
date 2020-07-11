import time
import pandas as pd
import matplotlib.pyplot as plt
import os


def auto_label(rects):
    for idx, rect in enumerate(bar_plot):
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width() / 2., 0.5 * height,
                bar_label[idx],
                ha='center', va='bottom', rotation=90)


start = time.time()

average_accuracy_by_window_size = {}
for w_size in [11, 21, 31, 41, 51, 61, 71, 81]:
    average_accuracy_by_window_size[w_size] = 0.0
count = 0

average_accuracy_by_vector_len = {}
for vector_len in range(0, 10):
    average_accuracy_by_vector_len[vector_len] = 0.0
count1 = 0

# for distance_type in ["polygon_distance"]:
# for distance_type in ["center_distance", "polygon_distance"]:
for distance_type in ["center_distance"]:
    for vec in ["vectors_1", "vectors_2"]:
        count = count + 1
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

                    if '../datasets/' + distance_type + '/' + vec + '/window_size_' + str(w_size) + '/' in current_file:
                        current_file = current_file.replace('../datasets/' + distance_type + '/' + vec +
                                                            '/window_size_' + str(w_size) + '/', '')
                    X.append(current_file)
                    # X.append(str(current_number_of_file) + str(current_number_of_features))
                    accuracy.append(current_best_accuracy)

                average_accuracy_by_window_size[w_size] = average_accuracy_by_window_size[w_size] + max(accuracy)
                print(max(accuracy))
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

print(count)
for w_size in [11, 21, 31, 41, 51, 61, 71, 81]:
    print("Window_Size ", w_size, " average accuracy ", average_accuracy_by_window_size[w_size] / count)

print(count1)
for vector_len in range(0, 10):
    print("vector length ", vector_len, " average accuracy ", average_accuracy_by_vector_len[vector_len] / count1)


end = time.time()
print("Processor time (in seconds):", end)
print("Time elapsed:", end - start)
total = end - start
minutes, secs = divmod(total, 60)
hours, minutes = divmod(minutes, 60)
print(hours, ' : ', minutes, ' : ', secs)

exit(0)
