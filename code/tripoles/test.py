#-*-coding:utf-8-*-
import numpy as np
import math
from pandas import read_csv
from pandas import DataFrame

def person(a,b):
	n = len(a)
	sum1 = sum(a[i] for i in range(n))
	sum2 = sum(b[i] for i in range(n))
	
	sum1_pow = sum([pow(a[i],2) for i in range(n)])
	sum2_pow = sum([pow(b[i],2) for i in range(n)])
	
	sum_ab = sum([a[i]*b[i] for i in range(n)])
	
	fenzi = sum_ab - (sum1*sum2/n)
	fenmu = math.sqrt((sum1_pow - pow(sum1,2)/n)*(sum2_pow - pow(sum2,2)/n))
	if fenmu == 0:
		return 0.0
	return fenzi/fenmu


ogdata = "D:\SWaT-anomaly\data\Normal.csv"
midtxt = "mid.txt"


dataset = read_csv(ogdata, header=0, index_col=0)
name = list(dataset.columns.values)[:-1]
values = dataset.values
values = values[:,:-1]

values = values.astype('float64')

name_numlist = []
delete_list = []
for i in range(0,len(name)):
	if name[i][2] == 'T' or name[i][3] == 'T':
		name_numlist.append(i)
	else:
		delete_list.append(i)
values = np.delete(values,delete_list,axis = 1)

mean = []
var = []
for i in range(len(name_numlist)):
	mean.append(values[:,i].mean())
	var.append(values[:,i].var())

for i in range(len(values)):
	for j in range(len(values[0])):
		values[i][j] = (values[i][j] - mean[j]) / var[j]


mdt = open(midtxt,"w+")
for i in range(len(name_numlist)):
	for j in range(i+1,len(name_numlist)):
		print i,j
		for m in range(len(name_numlist)):
			if m != i and m != j:
				mi = person(values[:,m], values[:,i])
				mj = person(values[:,m], values[:,j])
				mij = person(values[:,m], values[:,i] + values[:,j])
				u = pow(mij,2) - max(pow(mi,2),pow(mj,2))
				if u > 0:
					print >> mdt, name[name_numlist[m]], name[name_numlist[i]], mi
					print >> mdt, name[name_numlist[m]], name[name_numlist[j]], mj
					print >> mdt, name[name_numlist[m]], name[name_numlist[i]], '+', name[name_numlist[j]], mij
					print >> mdt, '++',u
					print >> mdt,""

