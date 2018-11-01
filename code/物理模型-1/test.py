#-*-coding:utf-8-*-
import numpy as np
import math
from pandas import read_csv
from pandas import DataFrame

ogdata = "D:\SWaT-anomaly\data\Normal2.csv"
midtxt = "mid.txt"

dataset = read_csv(ogdata, header=0, index_col=0)
name = list(dataset.columns.values)[:-1]
values = dataset.values
values = values[:,:-1]
values = values.astype('float64')

sensor_list = []
actuator_list = []
for i in range(0,len(name)):
	name[i] = name[i].replace(' ','')
	if name[i][2] == 'T' or name[i][3] == 'T':
		sensor_list.append(i)
	else:
		actuator_list.append(i)

istart = 0
iend = 1
ans = []		
while iend < len(values):
	flag = True
	for i in actuator_list:
		if values[iend-1][i] != values[iend][i]:
			flag = False
			break
	if flag:
		iend+=1
	else:
		if iend - istart >= 60:
			temp = []
			stemp = []
			for j in actuator_list:
				stemp.append(name[j] + ":" + str(values[iend-1][j]))
			temp.append(stemp)
			jtemp = []
			for j in sensor_list:
				actemp = []
				actemp.append(name[j])
				
				actemp.append(values[istart][j])
				actemp.append(values[iend][j])
				'''
				for jindex in range(istart,iend):
					actemp.append(values[jindex][j])
				'''
				jtemp.append(actemp)
			temp.append(jtemp)
			ans.append(temp)
		istart = iend
		iend+=1

mdt = open(midtxt,"w+")
for i in range(0,len(ans)):
	print >> mdt, ans[i]
	print >> mdt, ""
print len(ans),len(ans[0])