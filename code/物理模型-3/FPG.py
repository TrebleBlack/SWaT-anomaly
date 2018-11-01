#-*-coding:utf-8-*-

#定义一个树，保存树的每一个结点
class treeNode:
    def __init__(self,nameValue, numOccur, parentNode):
        self.name = nameValue
        self.count = numOccur
        self.parent = parentNode
        self.children = {}   #用于存放节点的子节点
        self.nodeLink = None #用于连接相似的元素项
    
    #对count变量增加给定值
    def inc(self, numOccur):
        self.count += numOccur
     
    #用于将树以文本形式显示，对于构建树来说并不是需要的   
    def disp(self, ind = 1):
        print "  " * ind, self.name, "  ",self.count
        for child in self.children.values():
            child.disp(ind + 1)

#FP树的构建函数
def createTree(dataSet, minSup=1):
    ''' 创建FP树 '''
    # 第一次遍历数据集，创建头指针表
    headerTable = {}
    for trans in dataSet:
        for item in trans:
            headerTable[item] = headerTable.get(item, 0) + dataSet[trans]
    # 移除不满足最小支持度的元素项
    for k in headerTable.keys():
        if headerTable[k] < minSup:
            del(headerTable[k])
    # 空元素集，返回空
    freqItemSet = set(headerTable.keys())
    if len(freqItemSet) == 0:
        return None, None
    # 增加一个数据项，用于存放指向相似元素项指针
    for k in headerTable:
        headerTable[k] = [headerTable[k], None]
    retTree = treeNode('Null Set', 1, None) # 根节点
    # 第二次遍历数据集，创建FP树
    for tranSet, count in dataSet.items():
        localD = {} # 对一个项集tranSet，记录其中每个元素项的全局频率，用于排序
        for item in tranSet:
            if item in freqItemSet:
                localD[item] = headerTable[item][0] # 注意这个[0]，因为之前加过一个数据项
        if len(localD) > 0:
            orderedItems = [v[0] for v in sorted(localD.items(), r_cmp, reverse=True)] # 排序
            updateTree(orderedItems, retTree, headerTable, count) # 更新FP树
    return retTree, headerTable

def r_cmp(x, y):
    if x[1] < y[1]:
        return -1
    if x[1] > y[1]:
        return 1
    if x[1] == y[1]:
        if x[0] < y[0]:
            return -1
        else:
            return 1
    return 0	

def updateTree(items, inTree, headerTable,count):
    #判断事务中的第一个元素项是否作为子节点存在，如果存在则更新该元素项的计数
    if items[0] in inTree.children:
        inTree.children[items[0]].inc(count)
    #如果不存在，则创建一个新的treeeNode并将其作为子节点添加到树中    
    else:
        inTree.children[items[0]] = treeNode(items[0],count,inTree)
        # 更新头指针表或前一个相似元素项节点的指针指向新节点
        if headerTable[items[0]][1]==None:
            headerTable[items[0]][1] = inTree.children[items[0]]
        else:
            updateHeader(headerTable[items[0]][1],inTree.children[items[0]])
     # 对剩下的元素项迭代调用updateTree函数            
    if len(items) > 1:
        updateTree(items[1::], inTree.children[items[0]], headerTable, count)    

#获取头指针表中该元素项对应的单链表的尾节点，然后将其指向新节点targetNode            
def updateHeader(nodeToTest, targetNode):
    while (nodeToTest.nodeLink != None):
        nodeToTest = nodeToTest.nodeLink
    nodeToTest.nodeLink = targetNode   

def createInitSet(dataSet):
    retDict = {}
    for trans in dataSet:
		if frozenset(trans) not in retDict.keys():
			retDict[frozenset(trans)] = dataSet.count(trans)
    return retDict
#=========================================================

#给定元素项生成一个条件模式基（前缀路径）
#basePat表示输入的频繁项，treeNode为当前FP树中对应的第一个节点（可在函数外部通过headerTable[basePat][1]获取）
def findPrefixPath(basePat,treeNode):
    condPats = {}
    while treeNode != None:
        prefixPath = []     
        ascendTree(treeNode, prefixPath)
        if len(prefixPath) > 1:
            condPats[frozenset(prefixPath[1:])] = treeNode.count
        treeNode = treeNode.nodeLink
    #返回函数的条件模式基
    return condPats

#辅助函数，直接修改prefixPath的值，将当前节点leafNode添加到prefixPath的末尾，然后递归添加其父节点
def ascendTree(leafNode, prefixPath):
    if leafNode.parent != None:
        prefixPath.append(leafNode.name)
        ascendTree(leafNode.parent, prefixPath)    
        
#递归查找频繁项集
#参数：inTree和headerTable是由createTree()函数生成的数据集的FP树
#    : minSup表示最小支持度
#    ：preFix请传入一个空集合（set([])），将在函数中用于保存当前前缀
#    ：freqItemList请传入一个空列表（[]），将用来储存生成的频繁项集
def mineTree(inTree,headerTable,minSup,preFix,freqItemList):
    bigL = [v[0] for v in sorted(headerTable.items(),key = lambda p:p[1])]
    bigL1 = [v[1][0] for v in sorted(headerTable.items(),key = lambda p:p[1])]
    for basePat in bigL:
        newFreqSet = preFix.copy()
        newFreqSet.add(basePat)
        freqItemList.append(newFreqSet)
		
        freqItemList.append(bigL1[bigL.index(basePat)])
		
        condPattBases = findPrefixPath(basePat, headerTable[basePat][1])
        myConTree,myHead = createTree(condPattBases, minSup)
        
        if myHead != None:
            #用于测试
            #print 'conditional tree for :', newFreqSet
            #myConTree.disp()
            
            mineTree(myConTree, myHead, minSup, newFreqSet, freqItemList)

#封装算法
def fpGrowth(dataSet, minSup=300000):
    initSet = createInitSet(dataSet)
    myFPtree, myHeaderTab = createTree(initSet, minSup)
    freqItems = []
    mineTree(myFPtree, myHeaderTab, minSup, set([]), freqItems)

    sup = {}
    for i in range(0,len(freqItems),2):
        sup[frozenset(freqItems[i])] = freqItems[i+1]

    for i in range(1,1 + len(freqItems)/2):
        freqItems.pop(i)
	
    for i in range(0,len(freqItems)):
        freqItems[i] = frozenset(freqItems[i])
    return freqItems,sup

#挖掘关联规则
def generateRules3(L, supportData, minConf=0.7):
    bigRuleList = []
    for freqSet in L:
        if len(freqSet) > 1:
            H1 = [frozenset([item]) for item in freqSet]
            rulesFromConseq3(freqSet, H1, supportData, bigRuleList, minConf)
    return bigRuleList

def rulesFromConseq3(freqSet, H, supportData, brl, minConf=0.7):
    m = len(H[0])
    while (len(freqSet) > m): # 判断长度 > m，这时即可求H的可信度
        H = calcConf(freqSet, H, supportData, brl, minConf)
        if (len(H) > 1): # 判断求完可信度后是否还有可信度大于阈值的项用来生成下一层H
            H = aprioriGen(H, m + 1)
            m += 1
        else: # 不能继续生成下一层候选关联规则，提前退出循环
            break

def calcConf(freqSet,H,supportData, br1, minConf=0.7):
    prunedH = []
    for conseq in H:
        conf = float(supportData[freqSet])/float(supportData[freqSet - conseq])
      
        if conf>= minConf:
            #print freqSet-conseq,"-->",conseq ,"conf:",conf
            '''
            fro = freqSet-conseq
            i = 0
            temp = True
            while i < len(br1):
                if (fro & br1[i][0] == br1[i][0] and conseq == br1[i][1]) or (br1[i][0] == fro and br1[i][1] & conseq == conseq):
                    temp = False
                    break
                if (fro & br1[i][0] == fro and conseq == br1[i][1]) or (br1[i][0] == fro and br1[i][1] & conseq == br1[i][1]):
                    del(br1[i])
                    i = i - 1
                i = i + 1
            if temp:
                br1.append((fro,conseq,conf))  #填充可信度列表
            '''
            '''
            fro = freqSet-conseq
            i = 0
            temp = True
            while i < len(br1):
                if (br1[i][0] == fro and br1[i][1] & conseq == conseq):
                    temp = False
                    break
                if (br1[i][0] == fro and br1[i][1] & conseq == br1[i][1]):
                    del(br1[i])
                    i = i - 1
                i = i + 1
            if temp:
                br1.append((fro,conseq,conf))  #填充可信度列表
            '''
            '''
            fro = freqSet-conseq
            i = 0
            temp = True
            while i < len(br1):
                if (fro & br1[i][0] == fro and conseq == br1[i][1]):
                    temp = False
                    break
                if (fro & br1[i][0] == br1[i][0] and conseq == br1[i][1]):
                    del(br1[i])
                    i = i - 1
                i = i + 1
            if temp:
                br1.append((fro,conseq,conf))  #填充可信度列表
            '''
            br1.append((freqSet-conseq,conseq,conf,conf/float(supportData[conseq])))  #填充可信度列表
            prunedH.append(conseq)    #保存满足最小置信度的规则
    return prunedH
	
	
def aprioriGen(Lk,k):
    retList = []
    lenLk = len(Lk)
    for i in range(lenLk):
        for j in range(i+1,lenLk):
            #前k-2项相同时合并两个集合
            L1 = list(Lk[i])[:k-2]
            L2 = list(Lk[j])[:k-2]
            L1.sort()
            L2.sort()
            if L1 == L2:
                retList.append(Lk[i] | Lk[j])
            
    return retList
