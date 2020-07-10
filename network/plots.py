import time
import pandas as pd
import matplotlib.pyplot as plt

start = time.time()

# for distance_type in ["polygon_distance"]:
# for distance_type in ["center_distance"]:
for distance_type in ["center_distance", "polygon_distance"]:
    for vec in ["vectors_1", "vectors_2"]:
        for w_size in [11, 21, 31, 41, 51, 61, 71, 81]:
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

                if '../datasets/' + distance_type + '/' + vec + '/window_size_' + str(w_size) + '/' in current_file:
                    current_file = current_file.replace('../datasets/' + distance_type + '/' + vec + '/window_size_' +
                                                        str(w_size) + '/', '')
                    print(current_file)
                X.append(current_file)
                # X.append(str(current_number_of_file) + str(current_number_of_features))
                accuracy.append(current_best_accuracy)

            fig = plt.figure(figsize=(10, 5))

            # creating the bar plot
            plt.bar(X, accuracy, color='maroon',
                    width=0.4)

            plt.xlabel("files")
            plt.ylabel("accuracy")
            plt.title("Accuracy Bar plot")
            plt.xticks(rotation=90)
            fig.text = X

            plt.savefig(png_path)
            plt.show()
            # plt.bar(X, accuracy, width = 0.6)
            # plt.show()
            break
        break
    break

end = time.time()
print("Processor time (in seconds):", end)
print("Time elapsed:", end - start)
total = end - start
minutes, secs = divmod(total, 60)
hours, minutes = divmod(minutes, 60)
print(hours, ' : ', minutes, ' : ', secs)

exit(0)
