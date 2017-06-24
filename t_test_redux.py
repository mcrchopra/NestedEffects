#Import Packages
import pandas
import csv
import scipy.stats
import statsmodels.sandbox.stats.multicomp as correct
import numpy as np

# Create an gene by event matrix through the utliziation of t-tests on groups defined by
# the sample by event matrix and gene by sample matrix
# For each event in the sample by event matrix
# 	For each gene
# 		For each sample for that gene
#			Check if the event value for that sample is a 0 or 1
#			Accordingally append the gene expression value for that sample for that gene to group 0 or group 1
#		Perform a T-test between group 0 and group 1 (gene expression values) 
#		The result of the t-test will be a value in the gene by event matrix 

def run_t_test():
	# Read in gene_expression matrix and sample by event matrix
	gene_expression_matrix = pandas.read_csv("mRNA_pancan12.nopipe.nodups.tab", index_col = 0, sep = "\t")
	event_matrix = pandas.read_csv("attributes.mutations.hc.tab", index_col =0, sep="\t")

	# Determine overlapping samples across gene expression and event matrices
	sharedSamples = list(set(gene_expression_matrix.columns).intersection(set(event_matrix.index)))

	# Subset the matrices according to overlapping samples
	event_matrix = event_matrix.loc[sharedSamples]
	gene_expression_matrix = gene_expression_matrix[sharedSamples]

	#Create empty t_stats and p_val matrices
	gene_names = list(gene_expression_matrix.index)
	event_names = event_matrix.columns.values
	gene_by_event_t_stats = pandas.DataFrame(index = gene_names, columns = event_names)
	gene_by_event_p_value = pandas.DataFrame(index = gene_names, columns = event_names)

	# Set p value cutoff
	pValCutoff = .01
	lowestcomputedpValue = 1
	highestcomputedpValue = 0

	for event, event_samples in event_matrix.iteritems():
		print "Event = {}".format(event)
		# Seperate groups depending on binary value
		group_0 = event_matrix.index[np.array(event_samples == 0)]
		group_1 = event_matrix.index[np.array(event_samples == 1)]

		# Run the ttest
		ttests = scipy.stats.ttest_ind(gene_expression_matrix[group_0], gene_expression_matrix[group_1], axis=1)

		print "Group 0: {}".format(group_0)
		print "Group 1: {}".format(group_1)

		#Fill that Column
		gene_by_event_t_stats[event] = ttests.statistic
		print gene_by_event_t_stats
		gene_by_event_p_value[event] = ttests.pvalue

	
	#Generate two matrices
	positive_gene_by_event_matrix = np.logical_and(gene_by_event_t_stats > 0, gene_by_event_pvalues < cutoff).astype(int)
	negative_gene_by_event_matrix = np.logical_and(gene_by_event_t_stats < 0, gene_by_event_pvalues < cutoff).astype(int)
	print "lowestcomputedpValue = ", lowestcomputedpValue
	print "highestcomputedpValue = ", highestcomputedpValue

	positive_gene_by_event_matrix.to_csv(path_or_buf = "positive_gene_by_event_matrix.tab",sep = '\t')
	negative_gene_by_event_matrix.to_csv(path_or_buf = "negative_gene_by_event_matrix.tab",sep = '\t')

def main():
	run_t_test()

if __name__ == '__main__':
	main()

		
