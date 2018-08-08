#!/usr/bin/env python

import pandas
import csv

#Read in Data Types File and get the names of the binary events
names_file = pandas.read_csv("Layer_Data_Types.tab", index_col = 0, sep = "\t")
binary_event_names = list(names_file.ix[1,])

#Read in full events matrix and get the list of all the names
event_matrix = pandas.read_csv("allAttributes.tab", index_col = 0, sep = "\t")
all_event_names = list(event_matrix.columns.values)

#Find the Overlapping set
overlapping_events = set(binary_event_names).intersection(set(all_event_names))
large_names = list(event_matrix.columns.values)

#Get all the binary event data from the event matrix
new_matrix = event_matrix.filter(items = overlapping_events)
new_matrix.to_csv("all_events.tab", sep = "\t")

d = {}
for i in binary_event_names:
    if "MUTATION" in i:
        d[i] = "Mutation"
    elif "AMPLIFICATION" in i:
        d[i] = "Copy Number Gain"
    elif "DELETION" in i:
        d[i] = "Copy Number Loss"
    elif "Mutation" in i:
        d[i] = "Mutation Signature"
    else:
        d[i] = "Other"

attribute_matrix = pandas.DataFrame(binary_event_names)
duplicated_matrix = attribute_matrix
duplicated_matrix = duplicated_matrix.replace({0:d})
full_matrix = pandas.concat([attribute_matrix,duplicated_matrix], axis = 1)
full_matrix.to_csv("attribute_file", sep = "\t")