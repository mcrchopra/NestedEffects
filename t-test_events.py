#Import Packages
import pandas
import csv
import scipy.stats
import statsmodels.sandbox.stats.multicomp as correct

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

	# Create an empty gene by event matrix
	gene_names = list(gene_expression_matrix.index)
	event_names = event_matrix.columns.values
	gene_by_event_matrix = pandas.DataFrame(index = gene_names, columns = event_names)


	# Set p value cutoff
	pValCutoff = .01
	lowestcomputedpValue = 1
	highestcomputedpValue = 0


	sample_names = gene_expression_matrix.columns.values
	num_samples = len(sample_names)

	event_index = 0

	for index, event_column in event_matrix.iteritems():

		gene_index = 0

		print "Event_index = ", event_index

		for index_2, gene_row in gene_expression_matrix.iterrows():
			sample_index = 0

			group_0 = list()
			group_1 = list()

			for sample in sample_names:
				#print "Sample = ", sample

				# Protect against Key Error
				try:
					if event_column[sample] == 0:
						group_0.append(gene_row[sample])
					else:
						group_1.append(gene_row[sample])
			
				except KeyError:
					pass

				sample_index = sample_index +1

				#print "Sample Index = " , sample_index

			# Grouping for a single gene is done
			# T-test is performed

			#print "group_0 =", group_0
			#print "group_1 = ", group_1

			ttests = scipy.stats.ttest_ind(group_0, group_1)
			# print ttests

			_,corrected_results,_,_ = correct.multipletests(ttests.pvalue, method = "bonferroni")

			#print "corrected_results before pValCutoff = ", corrected_results

			correctedP = corrected_results[0]
			#print "corrected_P before pValCutoff = ", correctedP

			# Finding range of p Values
			if correctedP < lowestcomputedpValue:
				lowestcomputedpValue = correctedP

			if correctedP > highestcomputedpValue:
				highestcomputedpValue = correctedP

			# Converting it to values for matrix
			if correctedP < pValCutoff:
				correctedP = 1
			else:
				correctedP = 0

			#print "correctedP after pValCutoff = ", correctedP

   			# Populate gene by event matrix
   			gene_by_event_matrix.ix[gene_index, event_index] = correctedP

   			# print "Gene Index =", gene_index

   			# Increment gene index
   			gene_index = gene_index + 1


   		# Increment Event Index
   		event_index = event_index + 1


	print "lowestcomputedpValue = ", lowestcomputedpValue
	print "highestcomputedpValue = ", highestcomputedpValue

	gene_by_event_matrix.to_csv(path_or_buf = "gene_by_event_matrix.tab",sep = '\t')

def main():
	run_t_test()

if __name__ == '__main__':
	main()

		
