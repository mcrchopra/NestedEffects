import pandas
import csv
import numpy as np
import argparse
import pdb

def get_missing_nodes_nearest_neighbors(full_similarity_matrix, all_nodes, cosine_matrix, pearson_matrix, xy_file,
    missing_nodes_xy_output_name, no_matches_output_name, edge_file_output_file):
    
    #Get list of missing nodes 
    pearson_by_cosine_full_similarity_matrix = pandas.read_csv(full_similarity_matrix, index_col = 0, sep = "\t")
    all_nodes = pandas.read_csv(all_nodes, index_col = 0, sep = "\t")
    missing_nodes = list(set(all_nodes.index).symmetric_difference(set(pearson_by_cosine_full_similarity_matrix.index)))

    #Read in cosine distance matrix and subset it to the size of the pearson matrix
    cosine_distance_matrix = pandas.read_csv(cosine_matrix, index_col = 0, sep = "\t")
    cosine_distance_matrix = cosine_distance_matrix[pearson_by_cosine_full_similarity_matrix.index]
    cosine_distance_matrix = cosine_distance_matrix.loc[pearson_by_cosine_full_similarity_matrix.index]

    #Read in Pearson Correlation Matrix
    pearson_correlation_matrix = pandas.read_csv(pearson_matrix, index_col = 0, sep = "\t")

    #Get rid of diagonal values
    for i in pearson_correlation_matrix.index:
        pearson_correlation_matrix.ix[i,i] = 0
        cosine_distance_matrix.ix[i,i] = 0

    #Subset both matrices to include only the rows which have the missing nodes
    cosine_distance_matrix_missing_nodes = cosine_distance_matrix.loc[missing_nodes]
    pearson_correlation_matrix_missing_nodes = pearson_correlation_matrix.loc[missing_nodes]

    #Read in XY file and make empty pandas dataframe for resultant missing xy file
    xy_file = pandas.read_csv(xy_file, index_col = 0, sep = "\t")
    full_xy_file_for_missing_nodes = pandas.DataFrame(columns = ['x', 'y'])

    pdb.set_trace()

    count = 0
    no_matches = pandas.DataFrame()
    edge_file = pandas.DataFrame()
    for index, row in cosine_distance_matrix_missing_nodes.iterrows():
        count += 1
        print count
        # Rank row of cosine matrix in order to get top 100 and set all the other to nans
        row = row[row > 0.95] 
        cosine_distance_matrix_missing_nodes.ix[index] = cosine_distance_matrix_missing_nodes.ix[index][row.index] 
        pearson_correlation_matrix_missing_nodes.ix[index] = pearson_correlation_matrix_missing_nodes.ix[index][row.index]

        #Rank row of pearson matrix (top 6 of the 100 that are there from cosine)
        pearson_correlation_matrix_missing_nodes.ix[index] = pearson_correlation_matrix_missing_nodes.ix[index][xy_file.index]
        number_pearson = (pearson_correlation_matrix_missing_nodes.ix[index] > -2).sum()
        pearson_row = pearson_correlation_matrix_missing_nodes.ix[index].rank(method = "max")
        missing_nodes_nearest_neighbors = pearson_correlation_matrix_missing_nodes.ix[index][pearson_row > (number_pearson-6)]

        #Get the xy coordinates
        try:
            xy_subset = xy_file.loc[missing_nodes_nearest_neighbors.index]

            #Get subset of missing_nodes_nearest neighbors and create edge file
            the_subset = missing_nodes_nearest_neighbors.loc[xy_subset.index]
            temp_list = [missing_nodes_nearest_neighbors.name for i in xrange(len(the_subset))]
            the_subset = the_subset.reset_index()
            the_subset.index = temp_list
            the_subset.columns = ['Event_Name_For_Similarity', 'Value']
            edge_file = edge_file.append(the_subset)

            x_coordinate = xy_subset['x'].mean()
            y_coordinate = xy_subset['y'].mean()

            #Create a temp_df and add to full_file
            name_temp_list = []
            name_temp_list.append(missing_nodes_nearest_neighbors.name)
            temp_xy_df = pandas.DataFrame({'x':[x_coordinate],'y': [y_coordinate]}, index = name_temp_list)
            full_xy_file_for_missing_nodes = full_xy_file_for_missing_nodes.append(temp_xy_df)

        except KeyError:
            temp_list = []
            temp_list.append(missing_nodes_nearest_neighbors.name)
            no_matches_name = pandas.DataFrame(temp_list)
            no_matches = no_matches.append(no_matches_name)

    full_xy_file_for_missing_nodes.to_csv(missing_nodes_xy_output_name, sep = "\t")
    no_matches.to_csv(no_matches_output_name, sep = "\t")
    edge_file.to_csv(edge_file_output_file, sep = "\t")

def main():
    parser = argparse.ArgumentParser(description='Get File')
    parser.add_argument('full_similarity_matrix', type = str)
    parser.add_argument('all_nodes', type = str)
    parser.add_argument('cosine_matrix', type = str)
    parser.add_argument('pearson_matrix', type = str)
    parser.add_argument('xy_file', type = str)
    parser.add_argument('missing_nodes_xy_output_name', type = str)
    parser.add_argument('no_matches_output_name', type = str)
    parser.add_argument('edge_file_output_file', type = str)

    args = parser.parse_args()
    get_missing_nodes_nearest_neighbors(args.full_similarity_matrix, args.all_nodes, args.cosine_matrix, args.pearson_matrix, 
    args.xy_file, args.missing_nodes_xy_output_name, args.no_matches_output_name, args.edge_file_output_file)

if __name__ == '__main__':
    main() 
