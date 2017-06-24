import pandas 
from scipy import stats
import numpy as np
import statsmodels.sandbox.stats.multicomp as multicomp
import math
import sklearn.metrics.pairwise as sklp

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

def run_pairwise():
  binary_gene_by_event_matrix = pandas.read_csv("gene_by_event_matrix.tab", index_col = 0, sep = "\t")
  #smaller = binary_gene_by_event_matrix.ix[1:50,1:100]
  transposed_matrix = binary_gene_by_event_matrix.transpose()
  biXbi = sklp.pairwise_distances(transposed_matrix,metric=binBinTest,n_jobs=-1)
  p_value_matrix = pandas.DataFrame(biXbi, index = transposed_matrix.index, columns = transposed_matrix.index)
  p_value_matrix.to_csv(path_or_buf = "pairwise.tab",sep = '\t') 

def main():
  run_pairwise()

if __name__ == '__main__':
  main() 