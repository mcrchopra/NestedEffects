#Import packages
import peer
import pandas
import scipy
import csv
import argparse



def run_PEER(gene_expression_file, num_confounders,covariates_2, covariates_3):

	#Load in data
	gene_expression_matrix = pandas.read_csv(gene_expression_file, index_col = 0, sep = "\t")
	#transposed_matrix = gene_expression_matrix.transpose()
	#transposed_matrix.shape

	#Test
	#smaller = transposed_matrix.ix[1:50,1:100]


	#Create PEER object
	model = peer.PEER()

	#Set number of Confounders
	model.setNk(num_confounders)
	print (model.getNk())

	#Set data
	#model.setPhenoMean(transposed_matrix)
	model.setPhenoMean(gene_expression_matrix)
	print (model.getPhenoMean().shape)

	#Set priors
	model.setPriorAlpha(0.001,0.1);
	model.setPriorEps(0.1,10.);

	#Read in and set the covariates in the model object that you want to use
	#tissue_cov = pandas.read_csv(covariates_1, index_col = 0, sep = "\t")
	#model.setCovariates(tissue_cov)

	
	continuous_cov = pandas.read_csv(covariates_2, index_col = 0 , sep = "\t")
	#continuous_cov2 = continuous_cov.ix[1:50,1:100]
	model.setCovariates(continuous_cov)

	binary_cov = pandas.read_csv(covariates_3, index_col = 0, sep = "\t")
	#binary_cov = binary_cov.astype(float)
	#binary_cov2 = binary_cov.ix[1:50,1:100]
	model.setCovariates(binary_cov)

    #Run inference
	model.update()

	#investigate results
    #factors:
	factors = model.getX()
    #weights:
	weights = model.getW()
    #ARD parameters
	precision_w = model.getAlpha()
    #get corrected dataset:
	residual_data = model.getResiduals()
	print(residual_data)

	#corrected_data = pandas.DataFrame(residual_data, index = transposed_matrix.index, columns = transposed_matrix.columns.values)
	corrected_data = pandas.DataFrame(residual_data, index = gene_expression_matrix.index, columns = gene_expression_matrix.columns.values)
	corrected_data.to_csv(path_or_buf = "peer_covariates_results.tab",sep = '\t')

def main():
	parser = argparse.ArgumentParser(description='Get Parameters')
	parser.add_argument('file', type = str)
	parser.add_argument('num_counfounders', type = int)
	#parser.add_argument('covariates_1', type = str)
	parser.add_argument('covariates_2', type = str)
	parser.add_argument('covariates_3', type = str)
	args = parser.parse_args()
	#run_PEER(args.file,args.num_counfounders, args.covariates_1, args.covariates_2, args.covariates_3)
	run_PEER(args.file,args.num_counfounders,args.covariates_2, args.covariates_3)
	
if __name__ == '__main__':
	main()