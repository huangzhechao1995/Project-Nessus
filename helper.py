
"""
Created on Thu Nov  8 14:37:42 2018

@author: Zhechao (Andrew) Huang 
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import time 
import math

def time_since(since):
    interval = time.time()-since
    m = math.floor(interval/60)
    s = interval - m*60
    return '%dm %ds' % (m, s)

def read_data(args):
    
    print(args.root,args.filename)
    
    df=pd.read_excel(args.root+args.filename,encoding="utf-8")
    print("total data size:",df.shape)
    
    df_train, df_test=train_test_split(df,random_state=42,test_size=args.test_split)
    df_train.index=range(df_train.shape[0])
    df_test.index=range(df_test.shape[0])
    print("training data size:",df_train.shape)
    print("testing data size:",df_test.shape)
    return df,df_train,df_test

def NumberofErrors(df1, df2):
    """
    Calculate the number of difference values in two Dataframes (here, the two dataframes are our prediction and the truth)
    """
    errorCount=(df1.values!=df2.values).sum()
    return errorCount

