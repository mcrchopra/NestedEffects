#!/usr/bin/env python

import pandas
import csv

def make_tissue_list_attribute_file():
   attribute_file = pandas.read_csv("attribute_file_combination.csv", index_col = 0, sep = "\t")
    full_event_names = attribute_file.index
    event_names = []

    for index, value in enumerate(full_event_names):
        marker = value.index('_')
        event_names.append(value[0:marker])
        
    gene_list_file = pandas.read_csv("allOnco_Feb2017.tsv", index_col = 0, sep = "\t")
    gene_list_file_names = gene_list_file.index

    overlapping_genes = list(set(event_names).intersection(set(gene_list_file_names)))

    alt_names = list(gene_list_file.ix[0:2057,2])
    alt_name_intersection = list(set(alt_names).intersection(set(event_names)))

    full_alt_names = []
    for value in alt_names:
        value = str(value)
        indices_for_events = [i for i, x in enumerate(value) if x == ',']
        [0] + indices_for_events
        indices_for_events.append(len(value))
        other_alt_names = [value[indices_for_events[i]:indices_for_events[i+1]] for i,x in enumerate(indices_for_events) if i+1 < len(indices_for_events)]
        if len(other_alt_names) > 0:
            full_alt_names.append(other_alt_names)

    full_alt_names = sum(full_alt_names, [])
    full_alt_names = [s.replace(',', '') for s in full_alt_names]
    other_intersect = list(set(full_alt_names).intersection(set(event_names)))
    alt_name_intersection.extend(other_intersect)
    overlapping_genes.extend(alt_name_intersection)

    zeros_list = [0]*full_event_names
    attribute_df = pandas.DataFrame(zeros_list, index = full_event_names)

    for index, name in enumerate(full_event_names):
        if event_names[index] in overlapping_genes:
            attribute_df.loc[name] = 1

    attribute_df.to_csv("cancer_gene_list_attribute.tab", sep = "\t")

def main():
    make_tissue_list_attribute_file()

if __name__ == '__main__':
    main()      

