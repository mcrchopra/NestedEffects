#!/usr/bin/env python

import pandas
import csv
import numpy as np
import argparse
import pdb



def percentile_sparsify(sim_df_pearson,sim_df_sample, pearson_cutoff, sample_cutoff):
    '''
    returns a sparsified version of simdf in edge format, keeping only the
    highest top * simdf.shape[0] edges in the matrix
    @param sim_df_pearson: a simlarity matrix (expression profile)
    @param sim_df_sample: a similarity matrix (sample profile)
    @return: edge format dataframe: column 1 is the row name, column 2 is the col name,
             and column 3 is the value of simdf[row name, col name]
    '''

    #pdb.set_trace()
    output = pandas.DataFrame()

    simdf_pearson = pandas.read_csv(sim_df_pearson, index_col = 0, sep = "\t")
    simdf_sample = pandas.read_csv(sim_df_sample, index_col = 0, sep = "\t")

    #ncols = len(simdf.index)
    #automatically determine percentile cutoff
    #cutoff = 100 - 100*( (float(top)*ncols) / ncols**2)
    #set all diagonal values to 0, so they are not included in percentile
    #simdf.values[[np.arange(ncols)]*2] = 0

    event_names = list(simdf_pearson.index)
    simdf_sample = simdf_sample.loc[event_names]
    simdf_sample = simdf_sample[event_names]
    #Handle Na's
    for i in event_names:
        simdf_pearson.ix[i,i] = 0
        simdf_sample.ix[i,i] = 0

    pdb.set_trace()
    sample_cut = np.percentile(simdf_sample.values, sample_cutoff)
    pearson_cut = np.percentile(simdf_pearson.values, pearson_cutoff)

    simdf_sample[simdf_sample >= sample_cut] = 1
    simdf_sample[simdf_sample < sample_cut] = 0
    
    simdf_pearson[simdf_pearson < pearson_cut] = 0
    simdf_pearson[simdf_pearson >= pearson_cut] = 1

    combined_matrix = simdf_pearson * simdf_sample

    for row_name in combined_matrix.index:
        row = combined_matrix.loc[row_name][np.array(combined_matrix.loc[row_name] == 1)]

        #the index is now the column name of the original similairty matrix
        for col_name in row.index:
            output = output.append(pandas.Series([row_name,col_name,row.loc[col_name]]), ignore_index=True)

    output.to_csv("sparse_combined_binary_matrix_7_15.tab", sep = "\t")        
    #return output

def main():
    parser = argparse.ArgumentParser(description='Get File')
    parser.add_argument('similairty_matrix_pearson', type = str)
    parser.add_argument('similairty_matrix_sample', type = str)
    parser.add_argument('pearson_cutoff', type = int)
    parser.add_argument('sample_cutoff',type = int)
    args = parser.parse_args()
    percentile_sparsify(args.similairty_matrix_pearson, args.similairty_matrix_sample, args.pearson_cutoff, args.sample_cutoff)

if __name__ == '__main__':
    main() 