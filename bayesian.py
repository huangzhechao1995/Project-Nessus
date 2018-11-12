#!/usr/bin/env python
# coding: utf-8

#upload libraries
import pandas as pd
import numpy as np
import csv
from operator import eq

df = pd.read_excel('Featureset01_revised.xlsx',sheet_name='Sheet1',header=0)

print("dataset size : ", df.shape)

####split training and testing sets
msk = np.random.rand(len(df)) < 0.80
dftrain = df[msk]
dftest = df[~msk]
dftrain.index=range(len(dftrain))
dftest.index=range(len(dftest))
print("trainning dataset size : ", dftrain.shape)
print("testing dataset size : ", dftest.shape)


def match_df(dftrain, dftest, n, p): #n is the number of question answered 
#initialize dfselector with True
	dfselector=np.full((dftrain.shape[0]), True, dtype=bool)
	for colname in dftrain.columns[:n]:
		dfselector=dfselector & (dftrain[colname]==dftest[colname][p])

	result =  dftrain[dfselector]
	return result 
###it can be the case that we have empthy data frame 

def countcase(result, n):
	count_target = result.iloc[:, n:] #the subset that we want to count
	#dfcount = count_target.groupby(count_target.columns.tolist()).size().reset_index().rename(columns={0:'count'})
	#count_target.groupby(count_target.columns.tolist(),as_index=False).size()
	#count_target.groupby(count_target.columns.tolist()).size()
	#dfcount = count_target.groupby(cols).size().reset_index(name='count')
	#key = []
	#unique = count_target.drop_duplicates()
	#unique.iloc[0,:].tolist()

	master = []
	for i in range(len(count_target)):
		strlist = []
		temp = count_target.iloc[i,:].tolist()
		for element in temp:
			element = str(element)
			strlist.append(element)
		strlist = ";".join(strlist)
		master.append(strlist)
	casedic = {i:master.count(i) for i in set(master)}
	return casedic


def prediton(dftrain, dftest, n, p, result):  
	result = match_df(dftrain, dftest, n, p)
	casedic = countcase(result, n)
	casedic_sorted_keys = sorted(casedic, key=casedic.get, reverse=True)
	if len(casedic_sorted_keys) > 0:
		casechosen = casedic_sorted_keys[0]
		#print("highest frequncy case is : ", casechosen, "frequency is : ", casedic[casechosen])
		predict = casechosen.split(';')
	else: 
		keys = []
		values = []
		benchmark = dftest.iloc[p,:n]
		for i in range(len(dftrain)):
			temp = dftrain.iloc[i,:n] 
			temp2 = dftrain.iloc[i,n:] 
			onekey =[]
			for element in temp2:
				element = str(element)
				onekey.append(element)
			onekey = ";".join(onekey)
			keys.append(onekey)
			check = list(map(eq, temp, benchmark))
			values.append(sum(check))
		casedic2 = dict(zip(keys, values))
		casedic2_sorted_keys = sorted(casedic2, key=casedic2.get, reverse=True)
		casechosen = casedic2_sorted_keys[0]
		predict = casechosen.split(';')


	#deal with extreme check, answered questions majority vote

	GT_raw = dftest.iloc[p,n:]
	GT = []
	for element in GT_raw:
		element = str(element)
		GT.append(element)
	check = list(map(eq, predict, GT))
	accuracy = sum(check)/len(check)
	wrongcase =  len(check) - sum(check)
	totalcase = sum(check)
	return predict, check, wrongcase, totalcase, accuracy

def performance(dftrain, dftest, n):
	wrong_whole = 0
	total_whole = 0
	for p in range(len(dftest)):
		result = match_df(dftrain, dftest, n, p)
		predict, check, wrongcase, totalcase, accuracy = prediton(dftrain, dftest, n, p, result)
		wrong_whole += wrongcase
		total_whole += totalcase
		print("----", wrong_whole)
	return wrong_whole, total_whole


n_40_wrong, n_40_total = performance(dftrain, dftest, 40)





















