import pandas
import csv
import numpy as np
import argparse
import pdb

def create_combined_matrix_and_sparse_matrix(full_similarity_matrix, sparse_matrix_output_name, top):
    '''
    pearson_correlation_df = pandas.read_csv(pearson_matrix, index_col = 0, sep = "\t")

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

    pdb.set_trace()

    cosine_distance_df[cosine_distance_df < 1] = 0
    pearson_cutoff = np.percentile(np.array(pearson_correlation_df), 85)
    pearson_correlation_df[pearson_correlation_df < pearson_cutoff] = 0
    #pearson_correlation_df[pearson_correlation_df >= pearson_cutoff] = 1

    combined_matrix = pearson_correlation_df * cosine_distance_df
    combined_matrix.to_csv(combined_matrix_output_name, sep = "\t")

    '''
    '''
    returns a sparsified version of simdf in edge format, keeping only the
    highest top * simdf.shape[0] edges in the matrix
    @param simdf: a simlarity matrix (or otherwise)
    @param top: used to determine cutoff, top * number of columns in simdf values will be kept
    @return: edge format dataframe: column 1 is the row name, column 2 is the col name,
             and column 3 is the value of simdf[row name, col name]
    '''
    pdb.set_trace()

    #Read in combined_matrix
    combined_matrix = pandas.read_csv(full_similarity_matrix, index_col = 0, sep = "\t")

    sparse_matrix_output = pandas.DataFrame()

    '''

    ncols = len(combined_matrix.index)
    #automatically determine percentile cutoff
    cutoff = 100 - 100*( (float(top)*ncols) / ncols**2)
    #set all diagonal values to 0, so they are not included in percentile
    combined_matrix.values[[np.arange(ncols)]*2] = 0
    '''

    #cut = np.percentile(combined_matrix.values, 85)
    cut = 0.556

    count = 0
    for row_name in combined_matrix.index:
        count += 1
        print count

        row = combined_matrix.loc[row_name][np.array(combined_matrix.loc[row_name] > 0)]
        row = row.nlargest(6)

        #the index is now the column name of the original similairty matrix
        for col_name in row.index:
            sparse_matrix_output = sparse_matrix_output.append(pandas.Series([row_name,col_name,row.loc[col_name]]), ignore_index=True)

    sparse_matrix_output.to_csv(sparse_matrix_output_name, sep = "\t") 

def main():
    parser = argparse.ArgumentParser(description='Get File')
    #parser.add_argument('pearson_matrix', type = str)
    #parser.add_argument('cosine_matrix', type = str)
    parser.add_argument('combined_matrix', type = str)
    #parser.add_argument('combined_matrix_output_name', type = str)
    parser.add_argument('sparse_matrix_output_name', type = str)
    parser.add_argument('top', type = int)
    args = parser.parse_args()
    create_combined_matrix_and_sparse_matrix(args.combined_matrix, args.sparse_matrix_output_name, args.top)

if __name__ == '__main__':
    main()