import time
import pandas as pd
from evaluation.classification.classification_utils import read_feature_vectors, bayesian_optimization

if __name__ == '__main__':
    start = time.time()

    accuracy_dict = {}
    # for distance_type in ['center_distance']:
    for distance_type in ['polygon_distance']:
        # for w in ['10', '30', '50', '70']:
        for w in ['10']:
            # for num_of_steps, num_of_walks in [('5', '10'), ('10', '5'), ('15', '3')]:
            for num_of_steps, num_of_walks in [('5', '10')]:
                # for emb in ['skip_gram', 'cbow']:
                for emb in ['skip_gram']:
                    # for size in ['50', '100', '150']:
                    for size in ['150']:
                        file = '../../datasets/' + distance_type + '/window_size_' + w + '/' + num_of_steps + 'steps_' \
                               + num_of_walks + 'walks/' + emb + '/' + size + '/feature_vectors_0.csv'
                        try:
                            f = open(file)
                            print("exists\t\t", file)
                            f.close()

                            X_train, y_train, input_shape_x = read_feature_vectors.get_vectors(file)
                            result, best_accuracy = bayesian_optimization.optimize(X_train, y_train, input_shape_x)

                            accuracy_dict[file] = best_accuracy
                        except IOError:
                            print("DOESN'T EXISTS\t", file)

                        print(file)

    df = pd.DataFrame.from_dict(accuracy_dict)
    df.to_csv('../../evaluation/classification/best_hyperparameters.csv', index=False)

    end = time.time()
    print("Processor time (in seconds):", end)
    print("Time elapsed:", end - start)
    total = end - start
    minutes, secs = divmod(total, 60)
    hours, minutes = divmod(minutes, 60)
    print(hours, ' : ', minutes, ' : ', secs)

    exit(0)
