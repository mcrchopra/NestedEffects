import pandas
import csv
import numpy as np
import argparse
import pdb

def first_attribute(attribute_output_name):
    #Read in Data Types File and get the names of the binary events
    #pdb.set_trace()
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
    full_matrix.to_csv(attribute_output_name, sep = "\t")
    print full_matrix
    return full_matrix

def create_chromosome_position_attribute(event_file, output_name):
    event_attribute_file = pandas.read_csv(event_file, index_col = 0 , sep = "\t")
    event_names = list(event_attribute_file.index)

    full_chromosome_position_df = pandas.DataFrame(index = event_attribute_file.index)


    file_list = ['chromosome_1_KiloBasePos.continuos.attribute.tab', 'chromosome_2_KiloBasePos.continuos.attribute.tab', 
    'chromosome_3_KiloBasePos.continuos.attribute.tab', 'chromosome_4_KiloBasePos.continuos.attribute.tab',
    'chromosome_5_KiloBasePos.continuos.attribute.tab', 'chromosome_6_KiloBasePos.continuos.attribute.tab',
    'chromosome_7_KiloBasePos.continuos.attribute.tab', 'chromosome_8_KiloBasePos.continuos.attribute.tab',
    'chromosome_9_KiloBasePos.continuos.attribute.tab', 'chromosome_10_KiloBasePos.continuos.attribute.tab',
    'chromosome_11_KiloBasePos.continuos.attribute.tab', 'chromosome_12_KiloBasePos.continuos.attribute.tab',
    'chromosome_13_KiloBasePos.continuos.attribute.tab', 'chromosome_14_KiloBasePos.continuos.attribute.tab',
    'chromosome_15_KiloBasePos.continuos.attribute.tab', 'chromosome_16_KiloBasePos.continuos.attribute.tab',
    'chromosome_17_KiloBasePos.continuos.attribute.tab', 'chromosome_18_KiloBasePos.continuos.attribute.tab',
    'chromosome_19_KiloBasePos.continuos.attribute.tab', 'chromosome_20_KiloBasePos.continuos.attribute.tab',
    'chromosome_21_KiloBasePos.continuos.attribute.tab', 'chromosome_22_KiloBasePos.continuos.attribute.tab',
    'chromosome_X_KiloBasePos.continuos.attribute.tab', 'chromosome_Y_KiloBasePos.continuos.attribute.tab']

    for i in file_list:
        print i
        chromosome_file = pandas.read_csv(i,index_col = 0, sep = "\t")


        d = {}
        for val in event_names:
            marker = val.index('_')
            value_gene = val[0:marker]
            try:
                temp_set = chromosome_file.loc[value_gene]
                d[val] = temp_set.ix[0,]
            except KeyError:
                d[val] = np.NaN

        #pdb.set_trace()
        new_chromosome_number_attribute_file = pandas.DataFrame(event_attribute_file.index, index = event_attribute_file.index)
        replacement_df = new_chromosome_number_attribute_file.replace({"Event":d})
        replacement_df.columns = [i[0:13]]
        full_chromosome_position_df = pandas.concat([full_chromosome_position_df, replacement_df], axis = 1)

    full_chromosome_position_df.to_csv(output_name, sep = "\t")
    return full_chromosome_position_df

def create_chromosome_number_attribute(event_file, chromosome_file, output_name):
    event_attribute_file = pandas.read_csv(event_file, index_col = 0 , sep = "\t")
    event_names = list(event_attribute_file.index)

    chromosome_file = pandas.read_csv(chromosome_file, index_col = 0, sep = "\t")

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
    new_chromosome_number_attribute_file.to_csv(output_name, sep = "\t")
    return new_chromosome_number_attribute_file

def make_gene_pathways_attribute_file(event_file,pathway_file, maximum_column_length, output_name):

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

    full_df.to_csv(output_name, sep = "\t")
    return full_df

def make_tissue_list_attribute_file(event_file, cancer_gene_list_file, output_name):
    attribute_file = pandas.read_csv(event_file, index_col = 0, sep = "\t")
    full_event_names = attribute_file.index
    event_names = []

    for index, value in enumerate(full_event_names):
        marker = value.index('_')
        event_names.append(value[0:marker])
        
    gene_list_file = pandas.read_csv(cancer_gene_list_file, index_col = 0, sep = "\t")
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
        other_alt_names = [value[indices_for_events[i]:indices_for_events[i+1]] for i,x in enumerate(indices_for_events) 
        if i+1 < len(indices_for_events)]
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

    attribute_df.to_csv(output_name, sep = "\t")
    return attribute_df

def num_positives(combined_matrix, output_name):
    binary_matrix = pandas.read_csv(combined_matrix, index_col = 0, sep = "\t")
    num_positives = binary_matrix.sum()
    num_positives.to_csv(output_name, index_col = 0, sep = "\t")
    return num_positives

def combine_attribute_file(basic_attribute_file, chromosome_position, chromosome_number, gene_pathways, cancer_gene_list, num_positives, output_name):
    output = pandas.DataFrame(index = attribute_file.index)
    output.concat([basic_attribute_file, chromosome_position, chromosome_number, gene_pathways, cancer_gene_list, num_positives], 
    axis = 1, ignore_index = True)
    output.to_csv(output_name, sep = "\t")

def main():
    parser = argparse.ArgumentParser(description='Get File')

    #Read in all inputs and names of output for each method
    parser.add_argument('basic_attribute_file_output_name', type = str)
    parser.add_argument('chromosome_position_output_name', type = str)
    parser.add_argument('chromosome_number_file', type = str)
    parser.add_argument('chromosome_number_output_name', type = str)
    parser.add_argument('gene_pathway_file', type = str)
    parser.add_argument('maximum_column_length_gene_pathway_file', type = int)
    parser.add_argument('gene_pathways_file_output_name', type = str)
    parser.add_argument('cancer_gene_list_file', type = str)
    parser.add_argument('cancer_gene_list_output_name', type = str)
    parser.add_argument('combined_matrix_full_similarity', type = str)
    parser.add_argument('num_positives_output_name', type = str)
    parser.add_argument('full_atribute_output_name', type = str)

    args = parser.parse_args()

    #Create Basic Attribute File which is used as input to all other methods
    full_matrix = first_attribute(args.basic_attribute_file_output_name)
    #Create Chromosome Position Attribute File
    chromosome_position_df = create_chromosome_position_attribute(full_matrix, args.chromosome_position_output_name)
    #Create Chromosome Number Attribute File
    chromosome_number_df = create_chromosome_number_attribute(full_matrix, args.chromosome_number_file, 
    args.chromosome_number_output_name)
    #Create Gene Pathways Attribute File
    gene_pathways_attribute_df = make_gene_pathways_attribute_file(full_matrix, args.gene_pathway_file, 
    args.maximum_column_length_gene_pathway_file, args.gene_pathways_file_output_name)
    #Create Cancer Gene List Attribute File
    cancer_gene_list_df = make_tissue_list_attribute_file(full_matrix, args.cancer_gene_list_file, 
    args.cancer_gene_list_output_name)
    #Create an Attribute listing the Number of Positives in each event in the full similarity matrix
    num_positives_df = num_positives(args.combined_matrix_full_similarity, args.num_positives_output_name)
    #Combine all of these attribute files into one large attribute file
    combine_attribute_file(full_matrix,chromosome_position_df, chromosome_number_df, gene_pathways_attribute_df, 
    cancer_gene_list_df, num_positives_df, args.full_atribute_output_name)


if __name__ == '__main__':
    main()