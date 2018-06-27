#Import Packages
import pandas
import numpy as np
import sklearn.metrics.pairwise as sklp
from scipy import stats
import statsmodels.sandbox.stats.multicomp as multicomp
import math
import argparse
import pdb

def compute_pearson(t_stat_matrix, pearson_correlation_output_name, cosine_matrix, output_name, sparse_matrix_output_name, top):

    #Read in file and drop the na's
    #pdb.set_trace()
    input_file = pandas.read_csv(t_stat_matrix, index_col = 0, sep = "\t")
    na_free = input_file.dropna(axis=1, how='all')

    #Transpose the na free matrix and the regular matrix in order to get list of na columns
    transposed_matrix_na_free = na_free.transpose()
    transposed_matrix = input_file.transpose()

    #Get List of na columns
    only_na = transposed_matrix[~transposed_matrix.index.isin(transposed_matrix_na_free.index)]
    list_of_events_removed = list(only_na.index)
    print "List of Events Removed = {}".format(list_of_events_removed)

    columns_with_nas = transposed_matrix_na_free.columns[transposed_matrix_na_free.isnull().sum() > 0]

    #Run Pearson pairwise distances and transform into similarity matrix
    biXbi = sklp.pairwise_distances(transposed_matrix_na_free,metric="correlation", n_jobs = -1)
    pearson_correlation = 1-biXbi

    pearson_correlation_df = pandas.DataFrame(pearson_correlation, index = na_free.columns.values, columns = na_free.columns.values)

    pearson_correlation_df.to_csv(pearson_correlation_output_name, index_col = 0, sep = "\t")

    #Make Test Dataframe
    #df = pandas.DataFrame(np.random.random_sample(size=(3320,3320)),index = input_file.columns.values, columns = input_file.columns.values)
    
    '''
    #Read in cosine_distance dataframe and remove rows and columns which have NA's in t-stat matrix
    cosine_distance_df = pandas.read_csv(cosine_matrix, index_col = 0, sep = "\t")
    cosine_distance_df = cosine_distance_df.drop(list_of_events_removed)
    cosine_distance_df = cosine_distance_df.drop(list_of_events_removed, axis = 1)

    event_names = pearson_correlation_df.index

    #pdb.set_trace()

    #Handle Na's
    for i in event_names:
        pearson_correlation_df.ix[i,i] = 0
        cosine_distance_df.ix[i,i] = 0

    cosine_distance_df[cosine_distance_df < 1] = 0
    pearson_cutoff = np.percentile(np.array(pearson_correlation_df), 85)
    pearson_correlation_df[pearson_correlation_df < pearson_cutoff] = 0
    #pearson_correlation_df[pearson_correlation_df >= pearson_cutoff] = 1

    combined_matrix = pearson_correlation_df * cosine_distance_df
    combined_matrix.to_csv(output_name, sep = "\t")

    
    returns a sparsified version of simdf in edge format, keeping only the
    highest top * simdf.shape[0] edges in the matrix
    @param simdf: a simlarity matrix (or otherwise)
    @param top: used to determine cutoff, top * number of columns in simdf values will be kept
    @return: edge format dataframe: column 1 is the row name, column 2 is the col name,
             and column 3 is the value of simdf[row name, col name]

    output = pd.DataFrame()


    ncols = len(simdf.index)
    #automatically determine percentile cutoff
    cutoff = 100 - 100*( (float(top)*ncols) / ncols**2)
    #set all diagonal values to 0, so they are not included in percentile
    simdf.values[[numpy.arange(ncols)]*2] = 0

    cut = numpy.percentile(combined_matrix.values, cutoff)

    for row_name in simdf.index:
        row = simdf.loc[row_name][numpy.array(simdf.loc[row_name] > cut)]

        #the index is now the column name of the original similairty matrix
        for col_name in row.index:
            output = output.append(pd.Series([row_name,col_name,row.loc[col_name]]), ignore_index=True)

    return output
    ''' 

def main():
    parser = argparse.ArgumentParser(description='Get File')
    parser.add_argument('t_stat_matrix', type = str)
    parser.add_argument('pearson_correlation_output_name', type = str)
    parser.add_argument('cosine_distance_matrix', type = str)
    parser.add_argument('combined_matrix_output_name', type = str)
    parser.add_argument('sparse_matrix_output_name', type = str)
    args = parser.parse_args()
    compute_pearson(args.t_stat_matrix, args.pearson_correlation_output_name, args.cosine_distance_matrix, 
    args.combined_matrix_output_name, args.sparse_matrix_output_name)

if __name__ == '__main__':
    main()    