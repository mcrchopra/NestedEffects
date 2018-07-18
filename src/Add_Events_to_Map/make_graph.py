import pandas
import csv
import numpy as np 
import networkx as nx
import pdb
import argparse

def make_graph(fixed_xy_file, missing_nodes_xy_file, missing_nodes_edge_file, fixed_nodes_edge_file, full_xy_file_output_name):
    #Read in xy files and edge file
    fixed_nodes_xy = pandas.read_csv(fixed_xy_file, index_col = 0, sep = "\t")
    missing_nodes_xy = pandas.read_csv(missing_nodes_xy_file, index_col = 0, sep = "\t")
    missing_nodes_edge_file = pandas.read_csv(missing_nodes_edge_file, index_col = 0, sep = "\t")
    fixed_nodes_edge_file = pandas.read_csv(fixed_nodes_edge_file, index_col = 0, sep = "\t")

    #Get edge file values that meet final heurestic and combine to make full nodes edge file
    missing_nodes_edge_file_pearson_subset = missing_nodes_edge_file[missing_nodes_edge_file["Value"] > 0.2]
    full_nodes_edge_file = pandas.concat([missing_nodes_edge_file_pearson_subset, fixed_nodes_edge_file])

    #Get subset of xy coordinate for missing nodes
    intersected_names = list(set(missing_nodes_edge_file_pearson_subset.index).intersection(set(missing_nodes_xy.index)))
    missing_nodes_subset = missing_nodes_xy.loc[intersected_names]

    one_value_list = []

    for i in intersected_names:
        try:
            if (len(missing_nodes_edge_file_pearson_subset.loc[i]['Value'])):
                pass
        except TypeError:
            one_value_list.append(i)

    one_value_df = pandas.DataFrame(one_value_list)
    one_value_df.to_csv("one_value_event_similarity_names.tab", sep = "\t")


    #Make one large xy file by combining them
    combined_xy_files = fixed_nodes_xy.append(missing_nodes_subset)

    #Make a column of tuples of  the x,y columns and convert to dictionary (index: Name of Event, value: (x,y) coordinate)
    combined_xy_files['coordinates'] = zip(combined_xy_files['x'], combined_xy_files['y'])
    del combined_xy_files["x"]
    del combined_xy_files["y"]
    combined_xy_dict = combined_xy_files.to_dict()

    #pdb.set_trace()
    #Make Tuple of name combinations from full edge file (first two columns of edge file -> one column)  
    full_nodes_edge_file_tuple_combinations = zip(full_nodes_edge_file.index, full_nodes_edge_file['Event_Name_For_Similarity'])
    full_nodes_edge_file_values_list = list(full_nodes_edge_file['Value'])

    #Creation of full lists
    full_nodes_edge_file_list = []

    for index, value in enumerate(full_nodes_edge_file_tuple_combinations):
        temp_dict = {"my_weight": full_nodes_edge_file_values_list[index]}
        temp_tuple = (value[0], value[1], temp_dict)
        full_nodes_edge_file_list.append(temp_tuple)


    pdb.set_trace()

    #Get name of nodes to keep as final placement
    fixed_nodes_names = list(fixed_nodes_xy.index)
    #Get list of all nodes
    node_names = list(combined_xy_files.index)

    G = nx.Graph()
    G.add_nodes_from(node_names)
    G.add_edges_from(full_nodes_edge_file_list)
    full_pos = nx.spring_layout(G,pos = combined_xy_dict['coordinates'], fixed = fixed_nodes_names, weight = "my_weight")

    full_pos_df = pandas.DataFrame()
    full_pos_df = full_pos_df.from_dict(full_pos, orient = 'index')
    full_pos_df.to_csv(full_xy_file_output_name, sep = "\t")

def main():
    parser = argparse.ArgumentParser(description='Get File')
    parser.add_argument('fixed_xy_file', type = str)
    parser.add_argument('missing_nodes_xy_file', type = str)
    parser.add_argument('missing_nodes_edge_file', type = str)
    parser.add_argument('fixed_nodes_edge_file', type = str)
    parser.add_argument('full_xy_file_output_name', type = str)

    args = parser.parse_args()
    make_graph(args.fixed_xy_file, args.missing_nodes_xy_file, args.missing_nodes_edge_file,
    args.fixed_nodes_edge_file, args.full_xy_file_output_name)

if __name__ == '__main__':
    main() 