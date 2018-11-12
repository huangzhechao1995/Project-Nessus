
"""
Created on Fri Nov  2 01:29:28 2018

@author: Zhechao (Andrew) Huang
"""

from argparse import ArgumentParser


def get_args():
    argparser = ArgumentParser()
    argparser.add_argument('--filename', type=str, default="Featureset01_revised.xlsx")
    argparser.add_argument('--root', type=str, default="C:\\Users\\huang\\Dropbox (MIT)\\A Lab\\bayesian_inference\\")
    argparser.add_argument('--method',type=str, default="KNN")
    argparser.add_argument('--test_split',type=int, default=4000)
    argparser.add_argument('--update_step',type=int, default=5)
    argparser.add_argument('--pred_length',type=int, default=5)
    argparser.add_argument('--instant_update',type=bool, default=False)
    args = argparser.parse_args()
    return args