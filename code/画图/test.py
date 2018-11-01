#-*-coding:utf-8-*-
import numpy as np
import math
from pandas import read_csv
from pandas import DataFrame
from matplotlib import pyplot

ogdata = "D:\SWaT-anomaly\data\Normal1.csv"

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
#for i in range(0,1):
	fig = pyplot.figure(i+1)
	pyplot.title(name[i])
	pyplot.plot(values[:,i], 'b-',linewidth=1)
pyplot.show()