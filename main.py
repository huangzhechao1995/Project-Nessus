
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

from para_models import *

IS_PARAMETERMODEL={
        "CART":True,
        "LASSO":True,
        "KNN":False,
        "Frequency": False}

if __name__=="__main__":
    
    """------------------------Parameters---------------------"""
    args=util.get_args()
    
    
    args.method="CART"
    args.train_flag=True
    args.test_flag=False
    args.update_step=5
    args.pred_length=5
    """
    args.test_split=100
    args.update_step=60
    args.pred_length=33
    args.print_prediction=True
    args.print_truth=True
    """
    
    print("The Hyper-Parameters are:", args)
    
    """--------------------------Data-------------------------"""
    df_alldata, df, df_test=read_data(args)    #The process to get dummies need to be revised for better performance
    n_train, p = df.shape
    n_test, p = df_test.shape
    #p=p-3  #the last three columns are identification code for
    
    df_alldata.fillna("blank")
    df=df.fillna("blank")
    df_test=df_test.fillna("blank")
    
    df_alldata=df_alldata.applymap(lambda x: str(x))
    df=df.applymap(lambda x: str(x))
    df_test=df_test.applymap(lambda x: str(x))
    
    
    
    """--------------------------Model------------------------"""
    
    if args.method=="KNN":
        model=KNN
    if args.method=="Frequency":
        model=Frequency
    if args.method=="CART":
        model=CART
    
    metric=NumberofErrors
    
    predict_error_record=[]
    
    
    step_list=list(range(args.update_step, p, args.update_step))
    
    
    if not IS_PARAMETERMODEL[args.method]:
        args.train_flag=False
    """-------------------------Train-------------------------"""
    if args.train_flag:
        time_point=time.time()
        for step in step_list:
            #if step!=60:
            #    continue
            pred_length=min(args.pred_length, p-step)
            pred_length=min(args.pred_length, p-step) ####need to test !!!!!
            number_mistake=np.zeros(len(df_test))
            print("-------------------Training----------------------------")
            print("current step:{}  //".format(step),"predicting columns {} to {}".format(df.columns[step],df.columns[step+pred_length-1]))
            predict=model(df, df_test, step, pred_length, train_flag=True)    
            print("Training time for this stage:", time_since(time_point))
            
            if pred_length==p-step:
                break
    
    """--------------------------Test-------------------------"""
    if args.test_flag:
        time_point=time.time()
        for step in step_list: 
            pred_length=min(args.pred_length, p-step) ####need to test !!!!!
            number_mistake=np.zeros(len(df_test))
            print("------------------Testing-----------------------------")
            print("current step:{}  //".format(step),"predicting columns {} to {}".format(df.columns[step],df.columns[step+pred_length-1]))
            if  not IS_PARAMETERMODEL[args.method]:
                predict=model(df, df_test, step, pred_length)
            else:
                predict=model(df, df_test, step, pred_length, train_flag=False)  #predict is a list of prediction results
            
            truth=df_test.iloc[:,step:step+pred_length]
            #print(truth.iloc[0,:])
            #print(predict.iloc[0,:])
            errorcount=metric(predict, truth)
            
            if args.print_prediction:
                predict.to_csv("current step{}".format(step)+"_predict_length{}".format(pred_length)+'_errorcount{}'.format(errorcount)+'_predict.csv')
            if args.print_truth:
                truth.to_csv("current step{}".format(step)+"_predict_length{}".format(pred_length)+'_errorcount{}'.format(errorcount)+'_truth.csv')
    
            
            print('Number of Difference of {} columns and {} testing data is'.format(pred_length, df_test.shape[0]), errorcount)
            print("Testing time for this stage:", time_since(time_point))
            time_point=time.time()
            predict_error_record.append((step, errorcount))
            
            if pred_length==p-step:
                break
            
        
    
        print(predict_error_record)


        
        
        

        
    
    