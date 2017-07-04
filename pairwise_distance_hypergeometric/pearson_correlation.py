#Import Packages
import pandas
import numpy as np
import sklearn.metrics.pairwise as sklp
from scipy import stats
import statsmodels.sandbox.stats.multicomp as multicomp
import math

#Read in file and drop the na's
input_file = pandas.read_csv("full_t_test_statistic_matrix", index_col = 0, sep = "\t")
na_free = input_file.dropna(axis=1, how='all')

#Transpose the na free matrix and the regular matrix in order to get list of na columns
transposed_matrix_na_free = na_free.transpose()
transposed_matrix = input_file.transpose()

#Get List of na columns
only_na = transposed_matrix[~transposed_matrix.index.isin(transposed_matrix_na_free.index)]
list_of_events_removed = list(only_na.index)

#Run Pearson pairwise distances and transform into similarity matrix
biXbi = sklp.pairwise_distances(transposed_matrix,metric="correlation", n_jobs = 8)
pearson_correlation = 1-biXbi

pearson_correlation_df = pandas.DataFrame(pearson_correlation, index = na_free.columns.values, columns = na_free.columns.values)

#Make Test Dataframe
df = pandas.DataFrame(np.random.random_sample(size=(3320,3320)),index = input_file.columns.values, columns = input_file.columns.values)
df = df.drop(list_of_events_removed)
df = df.drop(list_of_events_removed, axis = 1)

combined_matrix = pearson_correlation_df * df

