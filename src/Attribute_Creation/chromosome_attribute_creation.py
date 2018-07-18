#!/usr/bin/env python

import pandas
import csv
import numpy as np

event_attribute_file = pandas.read_csv("attribute_file_combination.csv", index_col = 0 , sep = "\t")
event_names = list(event_attribute_file.index)

d = {}
for value in full_event_names:
    marker = value.index('_')
    value_gene = value[0:marker]
    try:
        temp_set = chromosome_file.loc[value_gene]
        d[value] = temp_set.ix[0,]
    except KeyError:
        d[value] = np.NaN

new_chromosome_number_attribute_file = pandas.DataFrame(event_attribute_file.index)
replacement_df = new_chromosome_number_attribute_file.replace({"Event":d})
new_chromosome_number_attribute_file = pandas.concat([new_chromosome_number_attribute_file,replacement_df], axis = 1)
new_chromosome_number_attribute_file.to_csv("chromosome_number_attribute_file.tab", sep = "\t")