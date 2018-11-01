#-*-coding:utf-8-*-
import numpy as np


midtxt = "mid3.txt"
midtxt1 = "midd3.txt"

def eq_list(a,b):
	lena = len(a)
	lenb = len(b)
	if lena == lenb:
		for i in range(0,lena):
			if a[i] != b[i]:
				return False
		return True
	return False

fr = open(midtxt)
mdt = fr.readlines()
time = mdt[0].split()

mdt1 = open(midtxt1,"w+")

for w in range(4,8):
	print >> mdt1, w
	i = 0
	sum_list = []
	num_list = []
	while i+w <= len(time):
		temp = time[i:i+w]
		flag = False
		for ii in range(0,len(sum_list)):
			if eq_list(temp,sum_list[ii]):
				flag = True
				break
		if flag:
			i+=1
			continue
		else:
			num = 1
			for ii in range(i+w,len(time)):
				temp1 = time[ii:ii+w]
				if eq_list(temp,temp1):
					num+=1
			num_list.append(num)
			sum_list.append(temp)
		i+=1
	for j in range(0,len(sum_list)):
		print >> mdt1, sum_list[j], num_list[j]
	print >> mdt1, ""