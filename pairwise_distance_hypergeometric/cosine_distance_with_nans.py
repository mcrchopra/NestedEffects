import pandas
import numpy as np
import sklearn.metrics.pairwise as sklp
from scipy import stats
import statsmodels.sandbox.stats.multicomp as multicomp
import math
import itertools

sample_by_event_matrix = pandas.read_csv("all_events.tab", index_col = 0, sep = "\t")
sample_by_event_matrix = sample_by_event_matrix.dropna(axis=0, how='all')

transposed_matrix = sample_by_event_matrix.transpose()

#Empty Event by event matrix
event_by_event_matrix = pandas.DataFrame(index = transposed_matrix.index, columns = transposed_matrix.index)

event_names = transposed_matrix.index
#Get List of combinations
combination_list = list(itertools.combinations(event_names, 2))

'''
Pseudocode:
    Get List of all possible combinations of names
    Create a function which applies to a list of all combinations of names and returns a list which all vectors without nans
        Use List values to index into full sample by event matrix
            Use .loc function to index matrix by row names
                Use python slicing to get part of list value needed for this operation
                    string_test[2:(string_test.index(',')-1)]
                    string_test[(string_test.index(',')+3):(len(string_test)-2)]
                    str(combination_list[1])[(str(combination_list[1]).index(',')+3):(len(str(combination_list[1]))-2)]
                   #Second one x1 = new_transposed_matrix.loc[str(combination_list[1])[(str(combination_list[1]).index(',')+3):(len(str(combination_list[1]))-2)]]
                   #First one y1 = new_transposed_matrix.loc[str(combination_list[1])[2:(str(combination_list[1]).index(',')-1)]
                   x1 = np.array(x)[np.where(np.logical_and(np.array(x)>=0, np.array(y)>=0))]
'''
def get_rid_of_nans(x):
    
    #First of Combinations
    first_one = new_transposed_matrix.loc[str(x)[2:(str(x).index(',')-1)]]
    #Second name in the combinations
    second_one = new_transposed_matrix.loc[str(x)[(str(x).index(',')+3):(len(str(x))-2)]]
    #Get rid of Nans
    x1 = np.array(first_one)[np.where(np.logical_and(np.array(first_one)>=0, np.array(second_one)>=0))]
    y1 = np.array(second_one)[np.where(np.logical_and(np.array(first_one)>=0, np.array(second_one)>=0))]
    cosine_distance = sklp.pairwise_distances(x1,y1,metric="cosine")
    event_by_event_matrix.ix[str(x)[2:(str(x).index(',')-1)],str(x)[(str(x).index(',')+3):(len(str(x))-2)]] = cosine_distance
    global count
    count += 1
    if count % 100000 == 0:
        print count
    return cosine_distance


map(get_rid_of_nans, combination_list)


#First of Combinations
first_one = new_transposed_matrix.loc[str(combination_list[1])[2:(str(combination_list[1]).index(',')-1)]
#Second name in the combinations
second_one = new_transposed_matrix.loc[str(combination_list[1])[(str(combination_list[1]).index(',')+3):(len(str(combination_list[1]))-2)]]