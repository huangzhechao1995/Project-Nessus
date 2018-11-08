
"""
Created on Thu Nov  8 14:42:34 2018
@author: Zhechao Huang

"""

import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
from scipy import stats
from sklearn.model_selection import train_test_split


def KNN(df, df_test, step,K=10):
    """
    The KNN method of prediction
    Input:
        df: The columns used to calculate the KNN, for example 4000 test data, df is 
    Output:
    
    """
    
    #initiate the NearestNeighbour Classifier
    #notice that in our case the metric is "Manthattan"
    nbrs = NearestNeighbors(n_neighbors=K, algorithm='ball_tree',metric="manhattan")
    
    #fit data
    distances, indices = nbrs.kneighbors(pd.get_dummies(df_test.iloc[:, :step]))
    
    return None

def Frequency(df, df_test, step,K=10):
    """
    The Frequency Method of prediction
    """
    df_selector=np.ones(len(df)).astype(bool)
    