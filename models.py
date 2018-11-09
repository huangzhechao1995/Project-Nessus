
"""
Created on Thu Nov  8 14:42:34 2018
@author: Zhechao Huang

"""

import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
from scipy import stats
from sklearn.model_selection import train_test_split

from collections import Counter


def vote(df,neighbourslist):
    dftemp=df.iloc[neighbourslist,:]
    L=[]
    for i in range(len(dftemp.columns)):
        b = Counter(dftemp.iloc[:,i])
        L.append(b.most_common(1))
    result=pd.DataFrame(np.array([x[0][0] for x in L]).reshape(1, df.shape[1]), columns=df.columns)
    return result

def NumberofErrors(df1, df2):
    errorCount=(df1.values==df2.values).sum()
    return errorCount

def KNN(df, df_test, step, pred_length, K=30):
    """
    The KNN method of prediction
    Input:
        df     : The columns used to look up KNN (training data)
        df_test: The columns used to calculate the KNN (testing data), for example 4000 test data. df_test size=(4000, p)
        step   : Which means we use columns [0,step] to predict KNN
    Output:
        result : The prediction of KNN, result size=(4000, pred_length)   step to step+pred_length-1
    """
    
    #initiate the NearestNeighbour Classifier
    #notice that in our case the metric is "Manthattan"
    nbrs = NearestNeighbors(n_neighbors=K, algorithm='ball_tree',metric="manhattan")

    #fit data
    train_dummies_df=pd.get_dummies(df.iloc[:, :step])
    test_dummies_df=pd.get_dummies(df_test.iloc[:,:step])
    if len(train_dummies_df.columns)!=len(test_dummies_df.columns):   #Ensure Train_dummies_df and Test_dummies_df to be the same shape
        df_temp=pd.DataFrame(columns=sorted(list(set([x for x in train_dummies_df.columns]+[x for x in test_dummies_df.columns]))))   
        
        train_dummies_df=pd.concat([df_temp,train_dummies_df])
        train_dummies_df.fillna(0,inplace=True)
        test_dummies_df=pd.concat([df_temp,test_dummies_df])
        test_dummies_df.fillna(0,inplace=True)
    nbrs.fit(train_dummies_df)


    distances, indices = nbrs.kneighbors(test_dummies_df.iloc[:,:])
    
    print(indices.shape)
    
    vote_result=[]
    for i in range(indices.shape[0]):
        vote_result.append(vote(df.iloc[:,step:step+pred_length],indices[i,step: step+pred_length]))    
    vote_result=pd.concat(vote_result)
    return vote_result

def Frequency(df, df_test, step):
    """
    The Frequency Method of prediction
    Input:
        df     : The columns used to look up KNN (training data)
        df_test: The columns used to calculate the KNN (testing data), for example 4000 test data. df_test size=(4000, p)
        step   : Which means we use columns [0,step] to predict KNN
    Output:
        result : The prediction of Frequency Method, result size=(4000, pred_length)
    """
    df_selector=np.ones(len(df)).astype(bool)
    