#-*-coding:utf-8-*-
import numpy as np
import math
from pandas import read_csv
from pandas import DataFrame

ogdata = "D:\SWaT-anomaly\data\Normal2.csv"

dataset = read_csv(ogdata, header=0, index_col=0)
name = list(dataset.columns.values)[:-1]
values = dataset.values
values = values[:,:-1]

values = values.astype('float64')
midtxt = "mid.txt"

sensor_list = []
actuator_list = []
for i in range(0,len(name)):
	name[i] = name[i].replace(' ','')
	if name[i][2] == 'T' or name[i][3] == 'T':
		sensor_list.append(i)
	else:
		actuator_list.append(i)

mdt = open(midtxt,"w+")
for i in actuator_list:
	print i
	temp1 = []
	temp2 = []
	for ii in range(0,len(sensor_list)):
		temp1.append([])
	for ii in range(0,len(sensor_list)):
		temp2.append([])
	for index in range(1,len(values)):
		if values[index][i] != values[index-1][i] and values[index-1][i] != 0:
			if values[index-1][i] == 1:
				for j in range(0,len(sensor_list)):
					temp1[j].append(values[index-1][sensor_list[j]])
			else:
				for j in range(0,len(sensor_list)):
					temp2[j].append(values[index-1][sensor_list[j]])
	print >> mdt, name[i]
	print >> mdt, "1->2"
	for j in range(0,len(sensor_list)):
		if temp1[j] == []:
			print >> mdt, name[sensor_list[j]],temp1[j]
		else:
			print >> mdt, name[sensor_list[j]],np.array(temp1[j]).mean(),np.array(temp1[j]).var(),np.array(values[:,sensor_list[j]]).var()
			#print >> mdt, name[sensor_list[j]],temp2[j]
	print >> mdt, "2->1"
	for j in range(0,len(sensor_list)):
		if temp2[j] == []:
			print >> mdt, name[sensor_list[j]],temp2[j]
		else:
			print >> mdt, name[sensor_list[j]],np.array(temp2[j]).mean(),np.array(temp2[j]).var(),np.array(values[:,sensor_list[j]]).var()
			#print >> mdt, name[sensor_list[j]],temp2[j]
