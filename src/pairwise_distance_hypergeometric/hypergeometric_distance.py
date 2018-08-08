import pandas 
from scipy import stats
import numpy as np
import statsmodels.sandbox.stats.multicomp as multicomp
import math
import sklearn.metrics.pairwise as sklp
import argparse

def binBinTest(x,y):
  M = x.shape[0]
  n = x.sum()
  N = y.sum()
  if n<N:
    n = y.sum()
    N = x.sum()
  k = (x*y).sum()

  hpd = stats.hypergeom(M, n, N)
  p=hpd.sf(k)

  print (p)
  return p

def run_pairwise(binary_matrix, output_name):
  binary_gene_by_event_matrix = pandas.read_csv(binary_matrix, index_col = 0, sep = "\t")
  #smaller = binary_gene_by_event_matrix.ix[1:50,1:100]
  transposed_matrix = binary_gene_by_event_matrix.transpose()
  biXbi = sklp.pairwise_distances(transposed_matrix,metric=binBinTest,n_jobs=-1)
  p_value_matrix = pandas.DataFrame(biXbi, index = transposed_matrix.index, columns = transposed_matrix.index)
  p_value_matrix.to_csv(path_or_buf = output_name,sep = '\t') 

def main():
  parser = argparse.ArgumentParser(description='Get File')
  parser.add_argument('file', type = str)
  parser.add_argument('output_name', type = str)
  args = parser.parse_args()
  run_pairwise(args.file,args.output_name)

if __name__ == '__main__':
  main() 