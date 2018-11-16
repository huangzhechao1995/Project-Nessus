
"""
Created on Thu Nov  8 14:42:34 2018
@author: Zhechao (Andrew) Huang

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
    #print(L)
    """try:
        result_array=np.array([x[0][0] for x in L]).reshape(1, df.shape[1])
        result=pd.DataFrame(result_array, columns=df.columns)
    except:
        print(L)
        print(dftemp)
        print(neighbourslist)
        print(df.shape)
        print(result_array)
        raise
    """
    #result_array=np.array([x[0][0] for x in L]).reshape(1, df.shape[1])
    result=df.iloc[0,:]
    for i in range(len(L)):
        df.iloc[0,i]=L[i][0][0]
    return df.iloc[:1,:]



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
    #print(indices.shape)
    
    vote_result=[]
    for i in range(indices.shape[0]):
        vote_result.append(vote(df.iloc[:,step:step+pred_length],indices[i]))   
    #print(vote_result[:100])
    
    vote_result=pd.concat(vote_result)
    return vote_result


def Frequency(df, df_test, step, pred_length):
    """
    The Frequency Method of prediction
    Input:
        df     : The columns used to look up KNN (training data)
        df_test: The columns used to calculate the frequency (testing data), for example 4000 test data. df_test size=(4000, p)
        step   : Which means we use columns [0,step] to predict [step: step+pred_length]
    Output:
        result : The prediction of Frequency Method, result size=(4000, pred_length)
    """
    vote_result=[]
    for i in range(len(df_test)):
        if i%500==0:
            print("%.2f percent completed" % (i/4000*100))
        df_test.iloc[i,:step]
        dfselector=np.zeros(df.shape[0])
        for colname in df.columns[:step]:
            dfselector=dfselector + (df[colname]==df_test[colname][i]).astype(int)
        indice=np.array(np.where(dfselector == dfselector.max())[0]).astype(int)
        #print("current step {},\t row {} in test set,\t best match has {} matches,\t {} best match set length".format(step, i, dfselector.max(), len(indice)))
        
        current_result=vote(df.iloc[:,step:step+pred_length], indice)
        vote_result.append(current_result)
    vote_result=pd.concat(vote_result)
    return vote_result
    
    
