#-*-coding:utf-8-*-
import numpy as np
import math
from pandas import read_csv
from pandas import DataFrame
from matplotlib import pyplot

ogdata = "D:\SWaT-anomaly\data\Normal2.csv"

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

for i in sensor_list:
	if name[i] == "LIT401":
		sen = values[:,i]
		'''
		temp2 = []
		istart = 0
		while istart < len(sen):
			sum = 0
			ii = 0
			num = 0
			while istart + ii < len(sen) and ii < 30:
				sum = sum + sen[istart+ii]
				ii+=1
				num+=1
			temp2.append(sum/num)
			istart = istart + ii
		sen = temp2
		'''
		
		temp1 = []
		for ii in range(0,len(sen)):
			j = 0
			num = 0
			sum = 0
			while j<=20 and ii+j < len(sen):
				sum = sum + sen[ii+j]
				num+=1
				j+=1
			j = 1
			while j<=20 and ii-j >= 0:
				sum = sum + sen[ii-j]
				num+=1
				j+=1
			temp1.append(sum/num)
		sen = temp1
		
		'''
		aa = 0.05
		temp3 = []
		temp3.append(sen[0] * aa)
		for ii in range(1,len(sen)):
			temp3.append(aa*sen[ii] + (1-aa)*temp3[ii-1])
		sen = temp3
		'''
		temp = []
		for j in range(1,len(sen)):
			temp.append(sen[j]-sen[j-1] + 900)
		pyplot.plot(sen, 'b-',linewidth=1)
		pyplot.plot(temp, 'g-',linewidth=1)
	pyplot.show()