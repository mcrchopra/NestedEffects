#!/usr/bin/env python

import pandas
import csv
import argparse
from collections import OrderedDict
import pdb

def make_attribute_file(event_file,pathway_file, maximum_column_length):

    #Read in attribute file and make two identical lists of event names
    event_attribute_file = pandas.read_csv(event_file, index_col = 0 , sep = "\t")
    full_event_names = list(event_attribute_file.index)
    event_names = list(event_attribute_file.index)

    #Create list of zeros for later
    listofzeros = [0]*len(full_event_names)

    #Make event names attribute into the gene names for those events
    for index, val in enumerate(event_names):
        marker = val.index('_')
        event_names[index] = val[0:marker]

    #Read in pathway file
    the_list = list(range(0,maximum_column_length))
    cp_gene_pathways = pandas.read_csv(pathway_file, names = the_list,index_col = 0, sep = "\t")

    full_df = pandas.DataFrame(index = full_event_names)

    #pdb.set_trace()
    percentage_cutoff = 0.01

    #Make empty list of tuples
    genes_events_mapping = []
    #Get Unique List
    unique_list = list(OrderedDict.fromkeys(event_names))

    #Make list of tuples which maps every unique gene to its events    
    for value in unique_list:
        #Get all indices for a unique gene by indexing non-unique gene list
        indices_for_events = [i for i, x in enumerate(event_names) if x == value]

        #Get the events by indexing into events list which has a one to one mapping relationship with non-unique gene list
        resultant_events = [full_event_names[i] for i in indices_for_events]
        #print resultant_events

        #Make tuple out of the events and the gene name and add to the list
        temp_tuple = (resultant_events, value)
        genes_events_mapping.append(temp_tuple)

    #Loop through each row and make attribute file if necessary
    for index, row in cp_gene_pathways.iterrows():

        temp = list(row.dropna())

        ind_dict = dict((k,i) for i,k in enumerate(unique_list))
        overlapping_genes = set(ind_dict).intersection(temp)
        indices = [ ind_dict[x] for x in overlapping_genes ]

        events_in_pathway = [genes_events_mapping[i][0] for i in indices]
        events_in_pathway = sum(events_in_pathway, [])

        print len(events_in_pathway)

        if len(events_in_pathway) > (percentage_cutoff*len(event_names)):
            #pdb.set_trace()
            attribute_df = pandas.DataFrame({row.name:listofzeros}, index = full_event_names)
            attribute_df.loc[events_in_pathway] = 1
            full_df = pandas.concat([full_df,attribute_df[row.name]])
            #string_name = "Attribute_file_{}.tab".format(row.name)
            #attribute_df.to_csv(string_name, sep = "\t")

    full_df.to_csv("full_df.tab", sep = "\t")

def main():
    parser = argparse.ArgumentParser(description='Get File')
    parser.add_argument('event_names_file', type = str)
    parser.add_argument('pathway_file', type = str)
    parser.add_argument('maximum_column_length', type = int)
    args = parser.parse_args()
    make_attribute_file(args.event_names_file,args.pathway_file, args.maximum_column_length)

if __name__ == '__main__':
    main() 

