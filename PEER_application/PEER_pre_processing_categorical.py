import pandas
import csv
import numpy

tissues = pandas.read_csv("pancan12TissueStrs.tab", index_col =0, sep = "\t")

tissue_list = []
tissue_list.append("BRCA")

for index, row in tissues.iterrows():
    new = []
    new.append(tissues.ix[index,0])
    if bool(set(new) & set(tissue_list)) == False :
        tissue_list.append(new[0])
    print tissue_list

full_tissue_list = pandas.DataFrame(tissue_list)
print full_tissue_list

dict = {"BRCA": 1,"BLCA" :2,"KIRC":3,"UCEC":4,"GBM":5, "LUSC":6, "LAML":7, "READ":8, "LUAD":9, "COAD":10, "OV":11,"HNSC":12}
tissues = tissues.replace({"Tissue":dict})

tissues.to_csv(path_or_buf = "tissues_with_numerical_categories.tab",sep = '\t')
