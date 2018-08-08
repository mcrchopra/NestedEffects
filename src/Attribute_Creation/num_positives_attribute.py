import pandas
import csv

binary_matrix = pandas.read_csv("full_event_dataframe_nonans.tab", index_col = 0, sep = "\t")
num_positives = binary_matrix.sum()
num_positives.to_csv("num_positives_attribute_without_nans.tab", sep = "\t")
