import pandas
import numpy as np
import sklearn.metrics.pairwise as sklp
from scipy import stats
import statsmodels.sandbox.stats.multicomp as multicomp
import math
import itertools
import datetime

count = 0
count_limit = 10
sample_by_event_matrix = pandas.read_csv("./all_events.tab", index_col = 0, sep = "\t")
sample_by_event_matrix = sample_by_event_matrix.dropna(axis=0, how='all')

transposed_matrix = sample_by_event_matrix.transpose()
event_by_event_matrix = pandas.DataFrame(index = transposed_matrix.index, columns = transposed_matrix.index)

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
def get_rid_of_nans(event):
    # Extract events and respective vectors
    #pdb.set_trace()
    event1 = event[0]
    event2 = event[1]
    event1_vector = transposed_matrix.loc[event1]
    event2_vector = transposed_matrix.loc[event2]

    # Remove values at indices, where NAN exists for either vector
    overlapping_indices = np.where(np.logical_and(np.array(event1_vector)>=0, np.array(event2_vector)>=0))
    event1_vector_no_nans = np.array(event1_vector)[overlapping_indices].reshape(1, -1)
    event2_vector_no_nans = np.array(event2_vector)[overlapping_indices].reshape(1, -1)
    
    # Compute Cosine Distance
    cosine_distance = sklp.pairwise_distances(event1_vector_no_nans, event2_vector_no_nans, metric="cosine")
    event_by_event_matrix.ix[event1, event2] = cosine_distance

    # Debug Statements
    global count
    count += 1
    
    global count_limit
    if count % count_limit == 0:
        print count
        print datetime.datetime.now().time()
        if count_limit < 10000:
            count_limit = count_limit*10

    return cosine_distance


def main():
    #Empty Event by event matrix
    event_names = transposed_matrix.index

    #Get List of combinations
    combination_list = list(itertools.combinations(event_names, 2)) 
    map(get_rid_of_nans, combination_list)
    event_by_event_matrix.to_csv("event_by_event_matrix_cosine_distance.tab", sep = "\t")

if __name__ == '__main__':
    main() 

#First of Combinations
#first_one = new_transposed_matrix.loc[str(combination_list[1])[2:(str(combination_list[1]).index(',')-1)]
#Second name in the combinations
#second_one = new_transposed_matrix.loc[str(combination_list[1])[(str(combination_list[1]).index(',')+3):(len(str(combination_list[1]))-2)]]