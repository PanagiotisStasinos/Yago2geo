**EXECUTE ORDER** 
> get_locations_csv.py  
> distances_to_csv.py  
> get_walks_csv.py  
> gensim/word2vec.py(get_skip_gram_vectors.py custom made but slower than gensim [deleted])  
> gensim/gensim_get_feature_vectors.py

**\__init\__()**  
> calls the rest of methods, in general it reads the locations file and creates the vector files 

 **distances_to_csv()**  
>finds distances for each location with its neighbors and 
>stores them in datasets/window_size_W/distances, 
>where W is the current size of window defined in utils.py  
>creates 2 distances files, one for the closest by latitude and one for those by longitude

**get_csv()**  
>Reads the 4 OS_extended files and the OS_new and stores the locations
>in a scv file. For each location it stores its name, geometry, id, type and asWKT

**random_walk()** \ \ \ \ \ \ \ \ (todo)  
> * gstore_random_walks() :  
    creates both training and testing feature vector and label files  
> * store_random_walks2() :
    creates data files that contain feature vectors and labels for each location


 **read_OS_topological()**  
>has two functions
> * get_topological_info() :  
    reads topological.nt and stores for each location the locations  
    that it touches, includes or be within them
> * get_statistics_of_topological_and_matches_files() :  
> used only to view some stats about the RDFs of the file