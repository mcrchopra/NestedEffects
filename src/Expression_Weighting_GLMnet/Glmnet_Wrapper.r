library(glmnet)
library(PRROC)
expression_file <- read.csv(file.choose(), sep = "\t", row.names = 1)
event_file <- read.csv(file.choose(), sep = "\t", row.names = 1)
expression_file_column_names <- colnames(expression_file)
colnames(expression_file) <- gsub('.', '-', expression_file_column_names, fixed = T)
event_file_row_names <- row.names(event_file)

intersected_names <- intersect(colnames(expression_file), event_file_row_names)

expression_test_subset <- expression_file[1:2000, intersected_names[1:2000]]

event_test_subset <- event_file[intersected_names[1:2000], 1:2000]
the_event_test_subset <- event_test_subset[3]

runClassifier<- function(X, Y, nfolds_input, iterations, alpha) {
  # The elastic-net penalty is controlled by alpha, and bridges the gap between lasso (α=1, the default) and ridge (α=0).
  # lasso results in sparse coefficients
  # ridge regression results in more coefficients

  # calculate number of folds
  # to guarantee that at least one positive/negative label is in eachfold, otherwise at least 10 samples per fold
  # first check if 10 observations exist per fold if 10 folds ischosen, if not set to min number of folds to keep at least 10 observations in each fold
  if (nrow(Y)/nfolds_input < 10) {
    nfolds_input<-floor(nrow(Y)/10)
  }

  nfolds<-min(max(3,nfolds_input),sum(Y==1),sum(Y==0))
  print(paste("Performing cross-validation using",nfolds,"folds"))
  print(paste("Alpha set to:",alpha,"(1=LASSO; fast; less
coefficients, 0=Ridge Regression; slow; all coefficients)"))
  # create weights, weights are a fraction of the pos/neg over the total number of labels
  fraction_0<-rep(1-sum(Y==0)/nrow(Y),sum(Y==0))
  fraction_1<-rep(1-sum(Y==1)/nrow(Y),sum(Y==1))
  # assign 1 - that value to a "weights" vector
  weights<-numeric(nrow(Y))
  weights[Y==0]<-fraction_0
  weights[Y==1]<-fraction_1

  # begin iterations
  pr_score_list<-as.numeric(list())
  lambda_list<-as.numeric(list())
  score_list<-as.numeric(list())
  precision_list<-as.numeric(list())
  recall_list<-as.numeric(list())
  pr<-c()
  for (i in 1:iterations) {
    print(paste("Iteration:",i,"of",iterations))

    # assign folds evenly using the mod operator
    fold0 <- sample.int(sum(Y==0)) %% nfolds
    fold1 <- sample.int(sum(Y==1)) %% nfolds
    foldid <- numeric(nrow(Y))
    foldid[Y==0] <- fold0
    foldid[Y==1] <- fold1
    foldid <- foldid + 1

    cv<-cv.glmnet(as.matrix(X), as.factor(Y[,1]), alpha=alpha, foldid
= foldid, family = "binomial", type.measure='auc', parallel=TRUE,
weights = weights)


    # PR AUC calculation
    resp<-data.frame(predict(cv, s=cv$lambda.min, data.matrix(X),
type="response"))
    resp$binary[resp$X1>.5]<-1
    resp$binary[resp$X1<.5]<-0



    #pos_resp<-(pos_resp-.5) * 2
    ## Precision - P = TP/(TP+FP) how many idd actually success/failure
    ## Recall - R = TP/(TP+FN) how many of the successes correctly idd
    TP<-length(which(resp$binary==1 & Y[,1]==1))
    FP<-length(which(resp$binary==1 & Y[,1]==0))
    FN<-length(which(resp$binary==0 & Y[,1]==1))
    if ((TP+FP) > 0) { precision<-TP/(TP+FP) } else { precision<-0 }
    if ((TP+FN) > 0) { recall<-TP/(TP+FN) } else { recall <- 0 }
    #print(paste("Precision:",precision))
    #print(paste("Recall:",recall))

    #pos_resp
    if (abs(max(as.numeric(resp$X1)) - min(as.numeric(resp$X1))) == 0) {
      pr$auc.integral<-0
      pr$auc.davis.goadrich<-0
      pr_auc<-0
    }
    else {
      pr <- pr.curve(
scores.class0=as.numeric(resp$binary),weights.class0=as.numeric(Y[,1]),curve=FALSE)
      pr_auc<-pr$auc.integral
      #print(paste("PR AUC:",pr_auc))
    }


    precision_list<-c(precision_list,precision)
    recall_list<-c(recall_list,recall)

    pr_score_list<-c(pr_score_list, pr_auc)
    score_list<-c(score_list, max(cv$cvm))
    lambda_list<-c(lambda_list, cv$lambda.min)
  }
  return(list("cv" = cv,
              "lambda.min" = mean(lambda_list),
              "score_list" = (score_list),
              "score.var" = var(score_list),
              "pr_auc" = (pr_score_list),
              "recall_list" = (recall_list),
              "precision_list" = (precision_list)))
}

val <- runClassifier(expression_test_subset, the_event_test_subset, 2, 10, 1)

