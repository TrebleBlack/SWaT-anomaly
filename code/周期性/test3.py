#-*-coding:utf-8-*-
import numpy as np
import math
from pandas import read_csv
from pandas import DataFrame
from matplotlib import pyplot

ogdata = "D:\SWaT-anomaly\data\Normal2.csv"
midtxt = "mid3.txt"

dataset = read_csv(ogdata, header=0, index_col=0)
name = list(dataset.columns.values)[:-1]
values = dataset.values
values = values[:,:-1]
values = values.astype('float64')

def update_diff_mean(a):
	sum = 0.0
	for i in range(1,len(a)):
		sum = sum + a[i] - a[i-1]
	return sum/(len(a)-1)


sensor_list = []
actuator_list = []
for i in range(0,len(name)):
	name[i] = name[i].replace(' ','')
	if name[i][2] == 'T' or name[i][3] == 'T':
		sensor_list.append(i)
	else:
		actuator_list.append(i)

mdt = open(midtxt,"w+")
for i in sensor_list:
	if name[i] == "LIT301":
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
		
		time = []
		ans = []
		c = 0.25
		istart = 0
		iend = 1
		diff_seg_mean = sen[iend]-sen[iend-1]
		while iend < len(sen):
			while iend < len(sen) and abs(sen[iend]-sen[iend-1] - diff_seg_mean) < c:
				iend += 1
				diff_seg_mean = update_diff_mean(sen[istart:iend])
			if iend < len(sen):
				ans.append([iend-istart-1, diff_seg_mean])
				istart = iend-1
				diff_seg_mean = sen[iend]-sen[iend-1]
				time.append(istart)
		'''
		print len(ans)
		xy = np.array(ans)
		pyplot.scatter(xy[:,0],xy[:,1],s=10)
		'''
		
		pyplot.plot(values[:,i], 'g-',linewidth=1)
		for ii in range(0,len(time)):
			pyplot.axvline(time[ii])
		
		pyplot.show()
		
		ans_str = []
		for ii in range(0,len(ans)):
			if ans[ii][1] > 0.2:
				ans_str.append(1)
			elif ans[ii][1] < -0.2:
				ans_str.append(4)
			else:
				if ans[ii][1] > 0.04:
					ans_str.append(2)
				else:
					ans_str.append(3)
		print len(ans_str)
		for ii in range(0,len(ans_str)):
			print >> mdt, ans_str[ii],
		



