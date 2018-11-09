
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


def vote(neighbourslist):
    dftemp=df.iloc[neighbourslist,:]
    L=[]
    for i in range(len(dftemp.columns)):
        b = Counter(dftemp.iloc[:,i])
        L.append(b.most_common(1))
    result=pd.DataFrame(np.array([x[0][0] for x in L]))
    return result


def KNN(df, df_test, step, pred_length, K=10):
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
    nbrs.fit(pd.get_dummies(df.iloc[:, :step]))
    
    
    distances, indices = nbrs.kneighbors(
    #for i in indices.iterrows():
    #    vote(indices[i,step: step+pred_length-1])
    print(indices)
    
    
    
    return None

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
    