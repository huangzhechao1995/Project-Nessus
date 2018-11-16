
"""
Created on Thu Nov  8 14:20:51 2018

@author: Zhechao (Andrew) Huang
"""


import pandas as pd
import numpy as np

import time
from helper import *
from models import *
import util



if __name__=="__main__":
    
    """------------------------Parameters---------------------"""
    args=util.get_args()
    print("The Hyper-Parameters are:", args)
    
    args.method="KNN"
    args.test_split=4000
    args.update_step=10
    args.pred_length=10
    
    
    """--------------------------Data-------------------------"""
    df, df_test=read_data(args)    #The process to get dummies need to be revised for better performance
    n_train, p = df.shape
    n_test, p = df_test.shape
    #p=p-3  #the last three columns are identification code for
    
    """--------------------------Model------------------------"""
    if args.method=="KNN":
        model=KNN
    if args.method=="Frequency":
        model=Frequency
    
    metric=NumberofErrors
    
    predict_error_record=[]
    
    time_point=time.time()
    """--------------------------Test-------------------------"""
    step_list=list(range(args.update_step, p, args.update_step))
    for step in step_list: 
        if step<=60:
            continue
        ##!!!!!
        pred_length=min(args.pred_length, p-step) ####need to test !!!!!
        number_mistake=np.zeros(len(df_test))
        print("-----------------------------------------------")
        print("current step:{}  //".format(step),"predicting columns {} to {}".format(df.columns[step],df.columns[step+pred_length-1]))
        predict=model(df, df_test, step, pred_length)  #predict is a list of prediction results
        truth=df_test.iloc[:,step:step+pred_length]
        #print(truth.iloc[0,:])
        #print(predict.iloc[0,:])
        errorcount=metric(predict, truth)
        print('Number of Difference of {} columns and {} testing data is'.format(pred_length, df_test.shape[0]), errorcount)
        print(time_since(time_point))
        time_point=time.time()
        predict_error_record.append((step, errorcount))


        
        
        

        
    
    