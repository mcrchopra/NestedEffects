import pandas
import csv
import argparse
import numpy as np 
import sklearn.metrics.pairwise as sklp
from scipy import stats
import statsmodels.sandbox.stats.multicomp as multicomp
import math
import pdb

def make_tissue_similarity_attribute(t_test_df, full_tissue_list, output_name):
    #Read in t_test_df and tissue_list
    t_test_df_with_tissues = pandas.read_csv(t_test_df, index_col = 0, sep = "\t")
    t_test_df_with_tissues = t_test_df_with_tissues.dropna(axis=1, how='all')

    tissue_list = pandas.read_csv(full_tissue_list, index_col = 0, sep = "\t")
    tissue_list = list(tissue_list.index)

    #Get columns for pairwise test
    t_test_df_subset_w_tissues = t_test_df_with_tissues[tissue_list]
    events_not_tissues = list(set(t_test_df_with_tissues.columns.values).symmetric_difference(set(tissue_list)))
    t_test_df_subset_without_tissues = t_test_df_with_tissues[events_not_tissues]


    #Tranpsose these dataframes for similarity matrix calculation
    t_test_df_subset_w_tissues = t_test_df_subset_w_tissues.transpose()
    t_test_df_subset_without_tissues = t_test_df_subset_without_tissues.transpose()

    #Create Simlarity Matrix
    similarity_matrix = sklp.pairwise_distances(t_test_df_subset_w_tissues, t_test_df_subset_without_tissues,
    metric='correlation', n_jobs = -1)

    similarity_matrix = 1 - similarity_matrix

    similarity_matrix_df = pandas.DataFrame(similarity_matrix, index = t_test_df_subset_w_tissues.index, 
    columns = t_test_df_subset_without_tissues.index)


    similarity_matrix_df.to_csv(output_name, sep = "\t")

def main():
    parser = argparse.ArgumentParser(description='Get File')
    parser.add_argument('t_test_df', type = str)
    parser.add_argument('tissue_list', type = str)
    parser.add_argument('output_name', type = str)
    args = parser.parse_args()
    make_tissue_similarity_attribute(args.t_test_df, args.tissue_list, args.output_name)

if __name__ == '__main__':
    main()