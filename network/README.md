**\__init\__.py**  
> used to either call a single nn for testing or to do bayesian optimize on a NN anf find the best hyperpameters

 **bayesian_opt.py**  
>   returns the best hyperparameters for the current dataset 
> todo

**read_datasets.py**  
> * read_from_csv() :  
>>>    reads the vector and label csv files for both training and testing data, normalizes the vectors , converts them in 
    dataframes and returns them  
> * read_from_json() :  
>>>    does the same with read_from_csv() but reads the .json files instead
> * df_to_dataset() :  
>>>    to do, not used currently
> * get_classWeight() :
>>>   finds the number of records for each OS_type/class.  
    It is used because some classes have significantly more records compared to some others that have scarce records
> * read_data() :  
>>>    used in case that one dataset is used to train and test the nn, so it reads the file, normalizes the vectors and returns in dataframe form
    
    
    
**simple_nn.py**  
> used for mainly for testing, uses the best hyperparameters given from the optimizer for the certain dataset

