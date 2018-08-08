import pandas
import csv
import sklearn.metrics.pairwise as sklp
from scipy import stats
import statsmodels.sandbox.stats.multicomp as multicomp
import math
import argparse
import pdb

def cosine_distance_calculation(input_file, output_name):
    pdb.set_trace()

    sample_by_event_matrix = pandas.read_csv(input_file, index_col = 0, sep = "\t")
    sample_by_event_matrix = sample_by_event_matrix.transpose()
    cosine_distance = sklp.pairwise_distances(sample_by_event_matrix, metric="cosine")

    cosine_distance_df = pandas.DataFrame(cosine_distance, index = sample_by_event_matrix.index, columns = sample_by_event_matrix.index)
    cosine_distance_df.to_csv(output_name, sep = "\t")

def main():
    parser = argparse.ArgumentParser(description='Get File')
    parser.add_argument('sample_by_event_matrix', type = str)
    parser.add_argument('output_name', type = str)
    args = parser.parse_args()
    cosine_distance_calculation(args.sample_by_event_matrix, args.output_name)

if __name__ == '__main__':
    main() 

