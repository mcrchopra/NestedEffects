import pandas
import csv
import numpy as np 
import random
import argparse
import pdb

def make_dummy_events(sample_by_event_file, num_positives_file, output_name):
    sample_by_event_matrix = pandas.read_csv(sample_by_event_file, index_col = 0, sep = "\t")
    num_positives = pandas.read_csv(num_positives_file, index_col = 0, sep = "\t")
    dummy_sample_by_event_matrix = pandas.DataFrame()

    pdb.set_trace()
    count = 0
    for i in num_positives.iterrows():
        #Incremenate count for running purposes
        count += 1
        print count

        nums = np.zeros(len(sample_by_event_matrix))
        nums[:i[1][0]] = 1
        np.random.shuffle(nums)

        col_name_list = ["Dummy_Event_" + i[0]]
        temp_df = pandas.DataFrame(nums, index = sample_by_event_matrix.index, columns = col_name_list)
        dummy_sample_by_event_matrix = pandas.concat([dummy_sample_by_event_matrix, temp_df], axis = 1)

    dummy_sample_by_event_matrix.to_csv(output_name, sep = "\t")


def main():
    parser = argparse.ArgumentParser(description='Get File')
    parser.add_argument('sample_by_event_file', type = str)
    parser.add_argument('num_positives_file', type = str)
    parser.add_argument('output_name', type = str)
    args = parser.parse_args()
    make_dummy_events(args.sample_by_event_file, args.num_positives_file, args.output_name)

if __name__ == '__main__':
    main()
