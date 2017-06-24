import pandas
import numpy as np
import csv

gene_expression_matrix = pandas.read_csv("mRNA_pancan12.nopipe.nodups.tab", index_col = 0, sep = "\t")
transposed_matrix = gene_expression_matrix.transpose()
transposed_matrix.shape

#Test
smaller = transposed_matrix.ix[1:50,1:100]
sample_names = smaller.index

continuous_cov = pandas.read_csv("cell_cycle.attr.tab", index_col = 0 , sep = "\t")
continuous_cov_names = continuous_cov.index

binary_cov = pandas.read_csv("one_mutation.csv", index_col = 0, sep = "\t")
binary_cov = binary_cov.astype(float)
binary_cov_names = binary_cov.index

overlapping_samples = set(binary_cov_names).intersection(set(sample_names))
overlapping_samples = list(overlapping_samples.intersection(continuous_cov_names))

continuous_cov_subset = continuous_cov.loc[overlapping_samples].sort_index()
binary_cov_subset = binary_cov.loc[overlapping_samples].sort_index()
smaller_subset = smaller.loc[overlapping_samples].sort_index()

continuous_cov_subset.to_csv(path_or_buf = "continuous_cov_subset.tab",sep = '\t')
binary_cov_subset.to_csv(path_or_buf = "binary_cov_subset.tab",sep = '\t')
smaller_subset.to_csv(path_or_buf = "smaller_subset.tab",sep = '\t')

print continuous_cov_subset