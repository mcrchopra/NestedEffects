#!/usr/bin/env python

import pandas
import csv

tissue_file = pandas.read_csv("pancan12TissueStrs.tab", index_col = 0, sep = "\t")
tissue_list = ["BRCA","BLCA","KIRC","UCEC","GBM", "LUSC", "LAML", "READ", "LUAD", "COAD", "OV","HNSC"]

tissue_event_df = pandas.DataFrame(index = tissue_file.index)

for name in tissue_list:
    tissue_file_subset = tissue_file.loc[tissue_file['Tissue'] == name]
    temp_df = tissue_file.copy()
    temp_df.columns = [name]
    temp_df[name] = 0
    temp_df.loc[tissue_file_subset.index] = 1
    tissue_event_df = pandas.concat([tissue_event_df, temp_df[name]], axis = 1)

tissue_event_df.to_csv("tissue_events.tab",sep = "\t")

