#-*-coding:utf-8-*-

import time
import xlrd
import FPG as fp
import numpy as np
import multiprocessing as mp

datas = "D:\\SWaT-anomaly\\data\\pre-normal1.txt"
freqItemstxt = "freqItems.txt"
rulestxt = "rules.txt"
ms = 350000
cf = 0.98
	
#生成数据集
def loadSimpDat(dataa):
    data = []
    for i in range(0,len(dataa)):
        temp = dataa[i].split()
        data.append(temp)
    return data

def task(q,freqItems,sup,cf):
    q.put(fp.generateRules3(freqItems,sup, minConf=cf))

if __name__=="__main__":
    
    start_time = time.time()
    
    #封装算法后代码测试
    fr = open(datas)
    dataa = fr.readlines()
    fr.close()
    dataSet = loadSimpDat(dataa)
    print len(dataSet)
    print len(dataSet[0])
    #print dataSet
    print "load_end"
    load_time = time.time()

    freqItems,sup = fp.fpGrowth(dataSet, minSup=ms)

    fo = open(freqItemstxt, "w+")
    for k,it in sup.iteritems():
        for g in k:
            print >>fo,g,
        print >> fo,": ",it

    print len(sup)

    freq_time = time.time()

    d = len(freqItems) / 5
    rules = []
    '''
    q = mp.Queue()
    p1 = mp.Process(target=task, args=(q,freqItems[0*d:(0+1)*d],sup,cf))
    p2 = mp.Process(target=task, args=(q,freqItems[1*d:(1+1)*d],sup,cf))
    p3 = mp.Process(target=task, args=(q,freqItems[2*d:(2+1)*d],sup,cf))
    p4 = mp.Process(target=task, args=(q,freqItems[3*d:(3+1)*d],sup,cf))
    p5 = mp.Process(target=task, args=(q,freqItems[4*d:(4+1)*d],sup,cf))
    p6 = mp.Process(target=task, args=(q,freqItems[5*d:(5+1)*d],sup,cf))
    p7 = mp.Process(target=task, args=(q,freqItems[6*d:(6+1)*d],sup,cf))
    p8 = mp.Process(target=task, args=(q,freqItems[7*d:(7+1)*d],sup,cf))
    p9 = mp.Process(target=task, args=(q,freqItems[8*d:(8+1)*d],sup,cf))
    p10 = mp.Process(target=task, args=(q,freqItems[9*d:(9+1)*d],sup,cf))
    p1.start()
    p2.start()
    p3.start()
    p4.start()
    p5.start()
    p6.start()
    p7.start()
    p8.start()
    p9.start()
    p10.start()
    p1.join()
    p2.join()
    p3.join()
    p4.join()
    p5.join()
    p6.join()
    p7.join()
    p8.join()
    p9.join()
    p10.join()
    res1 = q.get()
    res2 = q.get()
    res3 = q.get()
    res4 = q.get()
    res5 = q.get()
    res6 = q.get()
    res7 = q.get()
    res8 = q.get()
    res9 = q.get()
    res10 = q.get()
    rules = res1 + res2 + res3 + res4 + res5 + res6 + res7 + res8 + res9 + res10
    '''
    '''
    manager = mp.Manager()
    sup = manager.dict(sup)
    pool = mp.Pool()
    results = []
    for i in range(5):
        results.append(pool.apply_async(fp.generateRules3,(freqItems[i*d:(i+1)*d],sup,cf)))
    pool.close()
    pool.join()
    for res in results:
        rules = rules + res.get()
    '''
    '''
    q = mp.Queue()
    p1 = mp.Process(target=task, args=(q,freqItems[0*d:(0+1)*d],sup,cf))
    p2 = mp.Process(target=task, args=(q,freqItems[1*d:(1+1)*d],sup,cf))
    p3 = mp.Process(target=task, args=(q,freqItems[2*d:(2+1)*d],sup,cf))
    p4 = mp.Process(target=task, args=(q,freqItems[3*d:(3+1)*d],sup,cf))
    p5 = mp.Process(target=task, args=(q,freqItems[4*d:(4+1)*d],sup,cf))
    p1.start()
    p2.start()
    p3.start()
    p4.start()
    p5.start()
    p1.join()
    p2.join()
    p3.join()
    p4.join()
    p5.join()
    res1 = q.get()
    res2 = q.get()
    res3 = q.get()
    res4 = q.get()
    res5 = q.get()
    rules = res1 + res2 + res3 + res4 + res5
    '''
    rules = fp.generateRules3(freqItems,sup, minConf=cf)
    foru = open(rulestxt, "w+")

    for ru in rules:
        for g in ru[0]:
            print >> foru,g,
        print >> foru,"-->",
        for g in ru[1]:
            print >> foru,g,
        print >> foru,"conf=%f"%(ru[2]),"lift=%f"%(ru[3]*len(dataSet))
    print len(rules)

    end_time = time.time()
	
    print "Load Time: ",load_time-start_time
    print "FreqItems Time: ",freq_time-load_time
    print "Rules Time: ",end_time-freq_time
    print "Run Time: ",end_time-start_time