# meGA
## Overview
This project seeks to determine associations between mutually exclusive genomic alterations. In order to accomplish this, I developed the Mutually Exclusive Genomic Association (meGA) Computational Pipeline, a new methodology that couples a data- driven analysis of genomic alterations with an interactive visualization of these associations. 

Down below is a diagram that displays all the processes that the Computational Pipeline performs.

![Alt text](img/overview.png?raw=True "Overview")

The Mutually Exclusive Genomic Association (meGA) Computational Pipeline generally consists of five stages in order to produce the final map:
1) Computation of Correlations amongst Gene Expression Profiles
2) Computation of Correlations amongst Sample Profiles
3) Computation of the meGA Matrix
4) Development of the Initial Genomic Events Map
5) Refinement of this map to produce the meGA Visualization Map

This pipeline currently has been applied to TCGA’s PANCAN12 Dataset and this refined map is “sparse pearson by cosine map missing nodes put on the map”.

## Getting Started
If you want to build your own map, follow the steps below.

### Prerequisites
You will need the following Python Packages. 
1.) Pandas
2.) Numpy
3.) Scipy
4.) StatsModels
5.) Sklearn
6.) Networkx

You can use pip to install all of these packages.

Clone the repo with:
`git clone  https://github.com/mcrchopra/NestedEffects`

### Preprocessing
Input Data 
In order to use the computational pipeline, you will need a genomic events (samples by genomic alteration) dataset and a mRNA-seq dataset (consisting of samples by gene expression).
Event Creation/Attribute Creation
Your genomic alterations dataset (genomic events) needs to be formatted in the following way: samples (rows) by genomic alterations (columns). The samples indicate whether a certain patient had a genomic alteration. Refer to the following image of an example dataset if you need further clarification:


![Alt text](img/tab-sep-mutation.png?raw=True "Tab separated binary format.")

 There needs to be an overlap between the samples in your genomic alterations file and your mRNA seq dataset in order to use this pipeline. 
The event clusters that will be output by the map are analyzed in part by adding “attributes”, i.e. clinical data, to the map. Attributes provide the ability to visually segment the events on the map into meaningful categories with coloration. They allow us to visually inspect the roles of the clusters of genomic events in pathway enrichment and pathway disruption. The attributes used in maps generated with this pipeline were taken from genomic events in pathway enrichment and pathway disruption. These attributes can be grouped into the following categories: Gene Pathway Lists, Chromosome Number, Chromosome Position, Type of Event, Known Oncogenes, and Tissue Similarity Attributes.  
It is recommended that you consider using these types of attributes when generating your map. These attributes were taken from several public databases including the BROAD Institute’s Molecular Signature Database (msigDb) and then assigned to the events on the map.
In order to access the scripts used to format different types of attributes in the correct format for use in the creation of the map, do the following:

`cd Nested_Effects/src/Attribute_Creation/`

When there access the full\_attribute\_creation.py file. The following image shows a subset of the full\_attribute file created by this script.


![Alt text](img/attr-created.png?raw=True "Attribute File")

As you can see each genomic alterations has a value whether it be either 0 or 1 for binary attributes, between 1-n for categorical attributes, or any value for continuous attributes. Each row is a different genomic alterations and each column is a different attribute.
Running the Pipeline and Generating Initial Map

## T-tests
The first task is to quantify how much each gene is differentially expressed for each event in the dataset. The script that performs this action is called t\_test\_redux.py and can be located by doing the following:
`cd Nested_Effects/src/T_tests`

The two inputs to the script are the mRNA seq data matrix and genomic events matrix as stated above. The output of this script will be a Gene by Event matrix consists of t-statistics, which indicate whether genes are upregulated or downregulated for patients with a specific event.


## Distance Metrics
In order to calculate the correlations between genomic alterations, call pearson\_correlation.py using the resultant dataframe from calling t\_test\_redux.py. The resultant matrix received by calling pearson\_correlation.py will be an Event by Event Matrix where a pearson correlation score is calculated between each pair of genomic events to measure the association between the events on a scale of [-1, 1].
In order to quantify sample overlap, now calculate cosine distance. If your event dataset contains NaN’s call cosine\_distance\_with\_nans.py, and if your event dataset doesn’t contains NaN’s call cosine\_distance\_without\_nans.py. The output will by an event by event matrix with values between 0 and 1. 
In order to create the comprehensive similarity metric for creating the map, cutoffs will be applied (top 15% for the pearson correlation matrix and only keeping 1’s in the Cosine matrix) and then multiply these two matrices together. This results in the Final Similarity Matrix. In order to get the most accurate similarity matrix possible for clustering and creating a map, create a sparse similarity matrix, which leaves only the top six nearest neighbors in the file. All of this is done by sparse\_matrix.py and can be found by doing the following:

Use the pearson correlation matrix and cosine similarity matrix as input.

## Creating the First Map

    To create your First Map go to tumormap.ucsc.edu and press Create a Map. It will open a prompt that will ask you for a similarity file and an attribute file. So upload your sparse similarity file and the attribute file that you have created. A Force Directed Graph Algorithm will now be applied to cluster the genomic alterations based off the similarity matrix provided. 


![Alt text](img/tumor-map.png?raw=True "Tumor Map.")

## Creating the Refined Map
### Network X
As you can probably see from the map you initially made, all the genomic alterations you used as input did not make it on the map. This is because some frequently mutated genes, which include many known oncogenes, cannot be mutually exclusive with many (if any) events. Thus, we needed a way for connecting the FMGs into the map to help identify associations between known and novel events.
So we decided to lower the cosine threshold (not exactly mutually exclusive). Use the get\_top\_values\_for\_missing\_nodes.py script in order to get a sparse similarity matrix and initial xy placements for all the missing genomic alterations on the initial map. Use the full similarity matrix, a list of all genomic alterations, the cosine distance matrix, the pearson correlation matrix, and the xy placements of all the nodes on the initial map (get this by downloading it from the map) as input.
Then use make\_graph.py to run a different force directed graph algorithm that fixes the initial nodes in place (so it does not alter the initial map) and places these missing nodes back on top of the initial map. It uses the xy placements of the already placed nodes, the initial placements of the missing nodes which was just calculated, the sparse similarity matrix for the missing nodes, and the sparse similarity matrix for the nodes on the existing map as input. It outputs a final xy file which can be used as input along with the attributes file to create your refined map.

![Alt text](img/tumor-map2.png?raw=True "Tumor Map.")

## Conclusion
    Now you are free to inspect the map as you choose. Hopefully, you will find some interesting by investigating the clusters on your map.

## TLDR: A shorthand description of each of the steps.
1.) Event Matrix(s) -> get\_events\_pre\_processing.py -> Final Event Matrix
2.) mRNA Matrix, Final Event Matrix -> t\_test\_redux.py -> Tstats Matrix
3.) Tstats Matrix -> pearson\_correlation.py -> Pearson Correlation Matrix
4.) Final Event Matrix -> cosine\_distance\_with\_nans.py -> Cosine Distance Matrix
5.) Cosine Distance Matrix, Pearson Correlation Matrix -> sparse\_matrix.py -> Combined Matrix, Sparse Matrix
6.) Sparse Matrix, Attributes -> TumorMap
7.) Nodes From Map, Full Similarity Matrix, Cosine Distance Matrix, Pearson Correlation Matrix, Nodes From Map XY Coordinates -> get\_top\_values\_for\_missing\_nodes.py -> Edge File for Missing Nodes, Initial XY Placements for Missing Nodes
8.) Edge File for Missing Nodes, Initial XY Placements for Missing Nodes, Original Sparse Matrix, Fixed Nodes XY -> make\_graph.py -> Final XY Placements
