
"""
Created on Thu Nov  8 14:20:51 2018

@author: huang
"""


import pandas as pd
import numpy as np

from helper import *
import util






if __name__=="__main__":
    
    args=util.get_args()

    df, df_test=read_data(args)