# -*- coding: utf-8 -*-
"""
Created on Fri Nov  2 01:29:28 2018

@author: huang
"""

from argparse import ArgumentParser


def get_args():
    argparser = ArgumentParser()
    argparser.add_argument('--filename', type=str, default="ground_truth_10000.csv")
	argparser.add_argument('--root', type=str, default="C:\\Users\\huang\\Dropbox (MIT)\\A Lab\\Data\\")
	argparser.add_argument('--method',type=str, default="KNN")
	argparser.add_argument('--update_step',type=int, default=5)
	argparser.add_argument('--pred_length',type=int, default=5)
	argparser.add_argument('--instant_update',type=bool, default=False)
    args = argparser.parse_args()
    return args