
"""
Created on Thu Nov  8 14:20:51 2018

@author: huang
"""


import pandas as pd
import numpy as np

from helper import *
from models import *
import util



if __name__=="__main__":
    
    """------------------------Parameters---------------------"""
    args=util.get_args()
    print("The Hyper-Parameters are:", args)
    
    """--------------------------Data-------------------------"""
    df, df_test=read_data(args)
    n_train, p = df.shape
    n_test, p = df_test.shape
    #p=p-3  #the last three columns are identification code for
    
    """--------------------------Model------------------------"""
    if args.method=="KNN":
        model=KNN
    if args.method=="Frequency":
        model=Frequency
    
    """--------------------------Test-------------------------"""
    step_list=list(range(args.update_step, p, args.update_step))
    for step in step_list: 
        ##!!!!!
        pred_length=min(args.pred_length, p-step) ####need to test !!!!!
        number_mistake=np.zeros(len(df_test))
        print("current step:{}  //".format(step),"predicting columns {} to {}".format(df.columns[step],df.columns[step+pred_length-1]))
        model(df, df_test, step, pred_length)
        
        

        
    
    