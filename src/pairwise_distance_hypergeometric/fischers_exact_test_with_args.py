#!/usr/bin/env python

#Import needed packages 
import pandas
import numpy as np
import sklearn.metrics.pairwise as sklp
from scipy import stats
import statsmodels.sandbox.stats.multicomp as multicomp
import math
import datetime
import argparse
 
count = 0
count_limit = 10

# contingency table construction
def contingencyTable(x,y):

 x_n = len(set(x))
 y_n = len(set(y))
 
 # a dict of combinations present and the indecies for which they occur
 groupDict = pandas.DataFrame([x,y],index=[0,1]).transpose().groupby([0,1]).groups

 #intialize matrix that represents all all prosible combinations of the two discrete vars
 table = np.repeat(0,x_n*y_n).reshape(x_n,y_n)

 #fill in each combo that we have data for
 for key in groupDict.keys():
   #must modify the key to prevent off by one error when
   # accessing matrix
   modkey = tuple(map(lambda x: int(x)-1,key))

   table[modkey] = len(groupDict[key])

 return table
 
#fisher exact test
 
def binBinTest(x,y):
 #filter out bad values
 #x,y = filterBinCat(x,y)

 global count
 count += 1
 
 global count_limit
 if count % count_limit == 0:
  print count
  print datetime.datetime.now().time()
  if count_limit < 10000:
   count_limit = count_limit*10

 x1 = x[np.where(np.logical_and(x>=0, y>=0))]
 y1 = y[np.where(np.logical_and(x>=0, y>=0))]

 #build contingency table
 table = contingencyTable(x,y)
 #if contingency table for binaries doesn't have this shape,
 # then there are no observations for one of the binary variables values
 # e.g. after Na's are filtered there are only 1's present in one of the attributes,
 # statistics can not accurately be computed
 if table.shape != (2,2):
  return np.NAN
 oddsratio, pValue = stats.fisher_exact(table)
 
 return pValue

def run_fischers(events_file):
  sample_by_event_matrix = pandas.read_csv(events_file, index_col = 0, sep = "\t")
  sample_by_event_matrix = sample_by_event_matrix.transpose()
  
  sample_by_event_matrix = sample_by_event_matrix.dropna(axis=0, how='all')
  sample_by_event_matrix = sample_by_event_matrix.fillna(-1)
  biXbi = sklp.pairwise_distances(sample_by_event_matrix,metric=binBinTest, n_jobs = 8)
  results = pandas.DataFrame(biXbi)
  results.to_csv("sample_profile_similarity_with_nans.tab", sep = "\t")

def main():
  parser = argparse.ArgumentParser(description='Get File')
  parser.add_argument('events_file', type = str)
  args = parser.parse_args()
  run_fischers(args.file)

if __name__ == '__main__':
  main() 