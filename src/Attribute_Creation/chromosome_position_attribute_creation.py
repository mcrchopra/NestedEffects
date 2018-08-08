#!/usr/bin/env python

import pandas
import csv
import numpy as np
import argparse
import pdb

def create_chromosome_attribute(event_file):
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

    full_chromosome_position_df.to_csv("full_chromosome_position_df.tab", sep = "\t")

def main():
    parser = argparse.ArgumentParser(description='Get File')
    parser.add_argument('event_names_file', type = str)
    #parser.add_argument('chromosome_file', type = str)
    #parser.add_argument("output_names", type = str)
    args = parser.parse_args()
    create_chromosome_attribute(args.event_names_file)
if __name__ == '__main__':
    main() 