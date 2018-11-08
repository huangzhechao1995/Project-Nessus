
"""
Created on Thu Nov  8 14:37:42 2018

@author: huang
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

def time_since(since):
    interval = time.time()-since
    m = math.floor(interval/60)
    s = interval - m*60
    return '%dm %ds' % (m, s)

def read_data(args):
    
    print(args.root,args.filename)
    
    df=pd.read_excel(args.root+args.filename,encoding="utf-8")
    print("total data size:",df.shape)
    
    df, df_test=train_test_split(df,random_state=42,test_size=args.test_split)
    print("training data size:",df.shape)
    print("testing data size:",df_test.shape)
    return df,df_test