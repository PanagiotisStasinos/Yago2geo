import time
import pandas
import utils


if __name__ == "__main__":
    start = time.time()

    file = "../../datasets/center_distance/window_size_11/3steps_3walks/vectors.csv"
    df = pandas.read_csv(file)
    print(df.shape)
    gensim_vectors_list = df.values.tolist()
    print(len(gensim_vectors_list[0]))
    print(gensim_vectors_list[0])
    print(len(gensim_vectors_list[0][:0]), " - ", gensim_vectors_list[0][0])
    print(len(gensim_vectors_list[0][1:]), " - ", gensim_vectors_list[0][1:])

    vectors_dict = {}
    for temp_list in gensim_vectors_list:
        # print(temp_list[0], "-", temp_list[1:])
        vectors_dict[temp_list[0]] = temp_list[1:]

    
    # cosine similarity to get neighbors

    utils.show_exec_time(start)
    exit(0)
