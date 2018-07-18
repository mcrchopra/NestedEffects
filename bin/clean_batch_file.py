#!/usr/bin/env python

import pdb
import pandas
import csv

gene_expression = pandas.read_csv("mRNA_pancan12.nopipe.nodups.tab", index_col = 0, sep="\t")
sample_event = pandas.read_csv("attributes.mutations.hc.tab", index_col =0, sep="\t")
expression_sample_names = list(gene_expression.columns.values)
updated_sample_event_matrix = pandas.DataFrame()

# Sorting sample-event dataframe by the list of sample names from a gene expression 
# matrix so that the rows of the sample-event matrix are in the same order as the
# sample columns in the gene expression matrix
#print "start of for loop"
j = 0
for gene_sample_name in expression_sample_names:
	#print "gene_sample_name = ", gene_sample_name
	for event_sample_name,row in sample_event.iterrows():
		#print "gene_sample_name", gene_sample_name, "event_sample =" , event_sample_name
		if event_sample_name == gene_sample_name:
			dataframe_to_append = pandas.DataFrame(row)
			updated_sample_event_matrix = updated_sample_event_matrix.append(dataframe_to_append)
			print j,"gene_sample_name = ", gene_sample_name, " | event_sample = ", event_sample_name, "********************************************FOUND MATCH **********************************", 
			#print "updated_sample_event_matrix = ", updated_sample_event_matrix.head(100).to_string()
			break
	j = j+1

with open('sorted_sample_event.tab', 'wb') as csvfile:
    sample_event_file_writer = csv.writer(csvfile, delimiter='\t')
    sample_event_file_writer.writerow(updated_sample_event_matrix)
	#csvfile.close()








