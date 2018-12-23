# -*- coding: utf-8 -*-
"""
Created on Wed Nov 21 21:31:32 2018

@author: Andrew Huang, Jixin Wang 
"""
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
import pickle
import pandas as pd
from sklearn.model_selection import GridSearchCV
import os


def CART(df,df_test, step, pred_length, train_flag=True):
    """
    Input a dataframe(contains all information until current step)
    Output the prediction made in the next pred_length steps
    
    If training=True, then "df" is regarded as training set, df_test is not used.
    (1) we conduct 3-fold cross-validation on the training set, to select the best parameters
    (2) we save the best model, saved as "modelname"
    (3) return model result
    
    If training=False, it means we will do Testing, "df_test" is regarded as testing set, df is not used
    (1) we load the best model saved
    (2) test the model result on the testing set.
    (3) return model result.
    """

    outputFolder = './CARTmodel'
    if not os.path.exists(outputFolder):
        os.makedirs(outputFolder)
    train_dummies_df=pd.get_dummies(df.iloc[:, :step])
    test_dummies_df=pd.get_dummies(df_test.iloc[:,:step])
    
    result_dict=dict.fromkeys(df.columns[step:step+pred_length])
    for i in range(pred_length):
        modelname = 'step{}predicting{}.sav'.format(step,step+i)
        
        #print('training', modelname)
        if len(train_dummies_df.columns)!=len(test_dummies_df.columns):   #Ensure Train_dummies_df and Test_dummies_df to be the same shape
            df_temp=pd.DataFrame(columns=sorted(list(set([x for x in train_dummies_df.columns]+[x for x in test_dummies_df.columns]))))   
            
            train_dummies_df=pd.concat([df_temp,train_dummies_df])
            train_dummies_df.fillna(0,inplace=True)
            test_dummies_df=pd.concat([df_temp,test_dummies_df])
            test_dummies_df.fillna(0,inplace=True)
        
        X=train_dummies_df
        Y=df.iloc[:,step+i]

        if train_flag:
            # Set the parameters by cross-validation
            tuned_parameters = {"criterion": ["gini", "entropy"],
                          #"min_samples_split": [2, 5, 10],
                          "max_depth": [2, 5, 10],
                          "min_samples_leaf": [1, 5, 10]
                          }
            clf = tree.DecisionTreeClassifier()
            clf = GridSearchCV(clf, tuned_parameters, cv=3)
            clf.fit(X,Y)
            pickle.dump(clf, open('model/{}'.format(modelname), 'wb'))
        else:
            clf = pickle.load(open('model/{}'.format(modelname), 'rb'))
            prediction=clf.predict(test_dummies_df)
            result_dict[df.columns[step+i]]=prediction
    return pd.DataFrame(result_dict) if not train_flag else None
        
        
    
def RF(df,df_test, step, pred_length, train_flag=True):
    """
    Input a dataframe(contains all information until current step)
    Output the prediction made in the next pred_length steps
    
    If training=True, then "df" is regarded as training set, df_test is not used.
    (1) we conduct 3-fold cross-validation on the training set, to select the best parameters
    (2) we save the best model, saved as "modelname"
    (3) return model result
    
    If training=False, it means we will do Testing, "df_test" is regarded as testing set, df is not used
    (1) we load the best model saved
    (2) test the model result on the testing set.
    (3) return model results.
    """
    outputFolder = './RFmodel'
    if not os.path.exists(outputFolder):
        os.makedirs(outputFolder)
    train_dummies_df=pd.get_dummies(df.iloc[:, :step])
    test_dummies_df=pd.get_dummies(df_test.iloc[:,:step])
    
    result_dict=dict.fromkeys(df.columns[step:step+pred_length])
    for i in range(pred_length):
        modelname = 'RF_step{}predicting{}.sav'.format(step,step+i)
        
        if len(train_dummies_df.columns)!=len(test_dummies_df.columns):   
        #Ensure Train_dummies_df and Test_dummies_df to be the same shape
            df_temp=pd.DataFrame(columns=sorted(list(set([x for x in train_dummies_df.columns]+[x for x in test_dummies_df.columns]))))   
            
            train_dummies_df=pd.concat([df_temp,train_dummies_df])
            train_dummies_df.fillna(0,inplace=True)
            test_dummies_df=pd.concat([df_temp,test_dummies_df])
            test_dummies_df.fillna(0,inplace=True)
        
        X=train_dummies_df
        Y=df.iloc[:,step+i]
        if train_flag:
            # Set the parameters by cross-validation
            tuned_parameters = {"criterion": ["gini", "entropy"],
                          "min_samples_split": [2, 5, 10],
                          "max_depth": [2, 5, 10],
                          "min_samples_leaf": [1, 5, 10]
                          }
            clf = RandomForestClassifier()
            clf = GridSearchCV(clf, tuned_parameters, cv=3)
            clf.fit(X,Y)
            pickle.dump(clf, open('RFmodel/{}'.format(modelname), 'wb'))
        else:
            clf = pickle.load(open('RFmodel/{}'.format(modelname), 'rb'))
            prediction=clf.predict(test_dummies_df)
            result_dict[df.columns[step+i]]=prediction
    return pd.DataFrame(result_dict) if not train_flag else None


