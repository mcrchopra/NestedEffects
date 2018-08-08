import pandas
import csv

#Read in the two attribute files
large_file = pandas.read_csv("all_events.tab", index_col = 0, sep = "\t")
smaller_file = pandas.read_csv("attributes.mutations.hc.tab", index_col = 0, sep = "\t")

#Get the sample names
more_sample_names = large_file.index
less_sample_names = smaller_file.index

#Find the intersection of the sample names
overlapping_samples = set(more_sample_names).intersection(set(less_sample_names))
overlapping_samples = list(overlapping_samples)

#Index into the larger file with the list of interesecting sample names
large_file_subset = large_file.loc[overlapping_samples]

#Get the subset of this matrix whose columns have exactly 570 nans
fiveseventy_nans_subset = large_file_subset[large_file_subset.columns[large_file_subset.isnull().sum() == 570]]
fiveseventy_nans_subset = fiveseventy_nans_subset.dropna(axis = 0, how = "all")

#Get their sample names
new_sample_names_to_index = fiveseventy_nans_subset.index

#Get the subset of the matrix whose columns have 0 nans
no_nas_columns = large_file_subset.columns[large_file_subset.isnull().sum() == 0]
no_nas_subset = large_file_subset[no_nas_columns]

#Get full combined dataframe
no_nans_reduced_sample_subset = no_nas_subset.loc[new_sample_names_to_index]
full_event_dataframe = pandas.concat([fiveseventy_nans_subset,no_nans_reduced_sample_subset], axis = 1)

columns_with_nas = full_event_dataframe.columns[full_event_dataframe.isnull().sum() > 0]
print "Columns with nas = {}".format(columns_with_nas)

#Write to file
full_event_dataframe.to_csv("full_event_dataframe_nonans.tab", sep = "\t")

#Get Event names
event_names = full_event_dataframe.columns.values

d = {}

num_mutations= 0
num_amplifications = 0
num_deletions = 0
num_mutations_signature = 0
num_other = 0

for i in event_names:
    if "MUTATION" in i:
        d[i] = "Mutation"
        num_mutations += 1
    elif "AMPLIFICATION" in i:
        d[i] = "Copy Number Gain"
        num_amplifications += 1
    elif "DELETION" in i:
        d[i] = "Copy Number Loss"
        num_deletions += 1
    elif "Mutation" in i:
        d[i] = "Mutation Signature"
        num_mutations_signature += 1
    else:
        d[i] = "Other"
        num_other += 1

print "Number of mutations = {}".format(num_mutations)
print "num_amplifications = {}".format(num_amplifications)
print "num_deletions = {}".format(num_deletions)
print "num_mutations_signature = {}".format(num_mutations_signature)
print "num_other = {}".format(num_other)
print "Total Number of Events = {}".format(num_mutations+ num_amplifications + num_deletions + num_mutations_signature + num_other)

attribute_matrix = pandas.DataFrame(event_names)
duplicated_matrix = attribute_matrix
duplicated_matrix = duplicated_matrix.replace({0:d})
full_matrix = pandas.concat([attribute_matrix,duplicated_matrix], axis = 1)
full_matrix.to_csv("attribute_file", sep = "\t")