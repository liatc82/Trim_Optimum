# -*- coding: utf-8 -*-
"""
Created on Thu Oct 30 18:54:13 2014

@author: liat
"""
import BellmanFord
from OptTrim import *


from lxml import etree
import xml.etree.ElementTree as ET
import random
import scipy.stats
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.mlab as mlab
import time
import sys


def readXml(fileName, fileAttrib):
    tree = ET.parse(fileName)
    root = tree.getroot()
    treeAttribe = ET.parse(fileAttrib)
    rootAttrib = treeAttribe.getroot()
    for tsk in root.iter('tsk'):
        succDist = findName(rootAttrib,tsk.get('name'))
        tsk.set('Successdistribution', succDist)
        
    return  tree   
        
def findName(root, name):
    for tsk in root.iter('tsk'):
        if tsk.get('name')==name:
            return tsk.get('Successdistribution')
        
def updateSize(root):
    size=1
    if root.tag =="tsk":
        root.set("size",str(size))
    else:
        for child in root:
            updateSize(child)
            size = size+int(child.get("size"))
        root.set("size",str(size))    

def constructDistSample(root,samplesNum,bine):
    M={}
    for i in range(samplesNum):
        val = sampling(root,bine)
        if M.has_key(val):
            M[val] = M[val]+1
        else:
            M[val] = 1
            
    for key in M:
        M[key] = M[key]/float(samplesNum)
    
    return M
        

        
        
        

def sampling(root,bine):
    if root.tag == "tsk":
        return sample(root.get('Successdistribution'),bine)
    elif root.tag == "seq":
            sami=0
            for child in root:
                dist = sampling(child,bine)
                sami = sami+ dist            
            return sami
    else:    
        if root.tag == "par":
            maxi=0
            for child in root:
                dist = sampling(child,bine)
                maxi=max(maxi,dist)            
            return maxi  
            
            
def sample(s,bine):
    if s[0]=="C":
        dist = s[3:len(s)-2].split("][")
        x=random.random()
        tmp=0
        for el in dist:          
            splitedEl = el.split(",")
            tmp=tmp+float(splitedEl[1])
            if tmp> x:
                return float(splitedEl[0])       
                
    if s[0]=="N":
        [mu,sig] = s[2:len(s)-1].split(",")
        xN= random.normalvariate(float(mu),float(sig),bine)
        MN =  normToDiscrete(float(mu),float(sig))
        MNS = sorted(MN)
        tmp =MNS[0] 
        for i in MNS[1:len(MNS)]:
            if i >= xN:
                return tmp
            tmp = i 
        return tmp    
    if s[0]=="U":
        [a,b] = s[2:len(s)-1].split(",")
        xU= random.uniform(float(a),float(b))  
        MU = uniformToDiscrete(float(a),float(b),bine)   
        MUS = sorted(MU)
        tmp =MUS[0] 
        for i in MUS[1:len(MUS)]:
            if i >= xU:
                return tmp
            tmp=i    
        return tmp
        
        
#     if s[0]=="N":
#        [mu,sig] = s[2:len(s)-1].split(",")
#        return random.normalvariate(float(mu),float(sig),e)
#    if s[0]=="U":
#        [a,b] = s[2:len(s)-1].split(",")
#        return random.uniform(float(a),float(b),e)     
    
            

def goOverTree(root,f,bine, e,n):
    distTable = []
    if root.tag == "tsk":       
        return stringToDist(root.get('Successdistribution'),bine)
    elif root.tag == "seq":
            for child in root:
                dist = goOverTree(child,f,bine, e*float(root.get("size"))/n,n)
                distTable.append(dist)
            distSccSeq = f(distTable,e,n)
            return distSccSeq
    else:    
        if root.tag == "par":
            for child in root:
                dist = goOverTree(child,f,bine, min(e*float(root.get("size"))/n, 1.0/(len(root)^2+len(root))),n)
                distTable.append(dist)
            distSccPar = parallel(distTable)
            return distSccPar            


def stringToDist(s,e):
    M={}
    if s[0]=="C":
        dist = s[3:len(s)-2].split("][")
        for el in dist:
            splitedEl = el.split(",")
            if M.has_key(float(splitedEl[0])):
                M[float(splitedEl[0])]=M[float(splitedEl[0])]+float(splitedEl[1])
            else:  
                M[float(splitedEl[0])]=float(splitedEl[1])
        return M    
    if s[0]=="N":
        [mu,sig] = s[2:len(s)-1].split(",")
        return normToDiscrete(float(mu),float(sig),e)
    if s[0]=="U":
        [a,b] = s[2:len(s)-1].split(",")
        return uniformToDiscrete(float(a),float(b),e)    
        
        
        
def normToDiscrete(mu,sigma,e):
    f=scipy.stats.norm(mu,sigma)
    fDiscrete={}
    for i in range(int(1.0/e)):
        val = f.ppf(e*i)
        fDiscrete[val]=e
    return fDiscrete    
        
    
def uniformToDiscrete(a,b,e):
    dif = (b-a)*e
    fDiscrete={}
    for i in range(int(1.0/e)):
        val = a+(dif*i)
        fDiscrete[val]=e
    #print  fDiscrete   
    return fDiscrete              
        
    
                
                
#get data and returns (1) sorted data (2)a map with all values (3) sorted array af values
def _AllTimes(data):
    allTimes={}
    for dist in data:
        for val in dist:
            allTimes[val]=1
    #allTimes=sorted(allTimes) 
    return data, allTimes 


# compute the dist in a case of palAnd    
def parallel(data):
    (data,allTimes)=_AllTimes(data)
    sortedVals = sorted(allTimes)
    sumi=0
    for ell in sortedVals:
        for dist in data:
            for val in dist:
                if (val<=ell):
                    sumi+= dist[val]
            
            allTimes[ell]*=sumi
            sumi=0
    return CDFToPDF(allTimes, sortedVals)


#get data in a form of CDF and return PDF
def CDFToPDF(mapCdf,arrCdf):    
    arrCdf.reverse()
    for i in range(len(arrCdf)-1):
        mapCdf[arrCdf[i]]=mapCdf[arrCdf[i]]-mapCdf[arrCdf[i+1]]
    #print mapCdf    
    return  mapCdf 
    

    
def SumAccurateDescrete(data,e,n):
    M = {}
    tempM = {0:1}
    for dist in data:
        for val in dist:
            for i in tempM:
        		if M.has_key(val+i):
        		    M[val+i]=dist[val]*tempM[i] + M[val+i]
        		else:
        		    M[val+i]=dist[val]*tempM[i]
		    		
        tempM=M
        #print  len(M)
        M = {}
    return tempM
       

def gridyAlgo(data,error,n):
    e=error/n
    M={}
    temp=-1
    tempM = {0:1}
    for dist in data:
        for val in dist:
            for i in tempM:
                if tempM[i]!=0:    
                    if M.has_key(val+i):
                        M[val+i]=dist[val]*tempM[i] + M[val+i] 
                    else:
                        M[val+i]=dist[val]*tempM[i]+0
        #print M                
        if (len(M.keys())>int(1/e)+1):
            d= sorted(M)  
            for key in d:
                if (M.has_key(temp) and M[temp]+M[key]<e):                    
                    M[temp]=M[temp]+M[key]
                    M.pop(key)
                else:
                    temp=key                    
        #print M            
        temp=-1                           
        tempM=M
        M = {}
    #prob=sumMapLessThenT(dist,T)
    return tempM


# do not check if the size is more than 1/e and if the error is < p - the worst
def gridyAlgoDowngrade(data,error,n):
    #print "data*******", data
    e=error/n
    M={}
    tempM = {0:1}
    
    for dist in data:
        p=0
        for val in dist:
            for i in tempM:
                if tempM[i]!=0:    
                    if M.has_key(val+i):
                        M[val+i]=dist[val]*tempM[i] + M[val+i] 
                    else:
                        M[val+i]=dist[val]*tempM[i]+0
                        
        #print M
        d= sorted(M)  
        temp = d[0]
        #print "d--------->", d
        #print "M1--------->", M
        for key in d[1:len(d)]:
            if (p+M[key]<=e): 
                
                p=p + M[key] 
                M.pop(key)
            else:
                M[temp]=M[temp]+p
                temp=key 
                p=0                   
        #temp=-1 
        M[temp]=M[temp]+p
        #print "M2--------->", M 
        #print "M2 SUM--------->", sum(M.values())                         
                        
        tempM=M
        M = {}
    #print tempM
    return tempM  

# do not check if the size is more than 1/e and if the error is < p - the worst
def gridyAlgoDowngradeLowBound(data,error,n):
    e=error/n
    #print e
    M={}
    tempM = {0:1}
    
    for dist in data:
        p=0
        for val in dist:
            for i in tempM:
                if tempM[i]!=0:    
                    if M.has_key(val+i):
                        M[val+i]=dist[val]*tempM[i] + M[val+i] 
                    else:
                        M[val+i]=dist[val]*tempM[i]+0
                        
        #print M
        d= sorted(M) 
        d.reverse()
        temp = d[0]
        
        for key in d[1:len(d)]:
            if (p+M[key]<=e): 
                
                p=p + M[key] 
                M.pop(key)
            else:
                M[temp]=M[temp]+p
                temp=key 
                p=0                   
        #temp=-1 
        M[temp]=M[temp]+p
                                 
        tempM=M
        M = {}
    #print tempM
    return tempM 
    
    
# do not check if the size is more than 1/e and if the error is < p - the worst
#def gridyAlgoDowngradeLowBoundNOTGOOD(data,error,n):
#    e=error/n
#    #print e
#    M={}
#    tempM = {0:1}
#    p=0
#    for dist in data:
#        for val in dist:
#            for i in tempM:
#                if tempM[i]!=0:    
#                    if M.has_key(val+i):
#                        M[val+i]=dist[val]*tempM[i] + M[val+i] 
#                    else:
#                        M[val+i]=dist[val]*tempM[i]+0
#                        
#        #print M
#        d= sorted(M)  
#        
#        for key in d:
#            
#            if (p+M[key]<=e): 
#                
#                p=p + M[key] 
#                M.pop(key)
#            else:
#                M[key]=M[key]+p
#                p=0                   
#        #temp=-1 
#        if M.has_key(key):
#            M[key]=M[key]+p
#        else:
#            M[key]=p
#        tempM=M
#        M = {}
#    #print tempM
#    return tempM      
    
def lessThanT(dist,T): 
    prob = 0
    for key in dist:
        if (key<=T):
            prob = prob + dist[key]
    return prob    


        
    
def testTotalApp(fileName,fileAttrib,bine,output):
    print "stsrt"
    res=open(output,"a")
    #fileName = sys.argv[1]#'tests/along.xml'
    #fileAttrib =sys.argv[2] #'tests/along_attribUni.xml'
    err1=0
    err2=0
    err3 = 0
    err0 = 0
    maxI0=0
    maxI1=0
    maxI2=0
    maxI3=0
    tree = readXml(fileName,fileAttrib)
    updateSize(tree.getroot())
    #samples = int(sys.argv[3])
    #bine=float(sys.argv[5])
    #e=float(sys.argv[4])
    e=1
    bine = float(bine)
    res.write(fileName+"\n"+
                    fileAttrib+"\n"+
                    "n="+str(int(tree.getroot()[0].get("size")))+"\n"+
                    "m="+str(1/bine)+"\n")
    start_time = time.time() 
    dist1 =goOverTree(tree.getroot()[0],gridyAlgoDowngrade,bine,0.001,int(tree.getroot()[0].get("size")))
    elapsed_time_accurate = time.time() - start_time 
    print "elapsed_time_accurate", elapsed_time_accurate
    
    res.write("elapsed_time_accurate "+str(elapsed_time_accurate)+"\n")
    sortedDist1 = sorted(dist1)
    
    
    for e in [0.1,0.01]:
            
        #--------------------APPROXIMATION - DOWNGRADE - UPPERBOUND------------------------
        start_time = time.time()
        dist3= goOverTree(tree.getroot()[0],gridyAlgoDowngrade,bine,e,int(tree.getroot()[0].get("size")))
        elapsed_time_gridyBad = time.time() - start_time
        print "elapsed_time_gridyBad", elapsed_time_gridyBad
        
        #--------------------APPROXIMATION - DOWNGRADE - LOWERBOUND-------------------------
        start_time = time.time()
        dist4= goOverTree(tree.getroot()[0],gridyAlgoDowngradeLowBound,bine,e,int(tree.getroot()[0].get("size")))
        elapsed_time_gridyBadDown = time.time() - start_time
        print "elapsed_time_gridyBadLowBound", elapsed_time_gridyBadDown
    
        d1=0
    
        for i in sortedDist1: 
            
            d1 = d1 + dist1[i]                        
            tmp2 = lessThanT(dist3,i)-d1
            if tmp2>=err2:
                err2=tmp2   
                maxI2=i
            tmp3 = lessThanT(dist4,i)-d1
            if abs(tmp3)>=err3:
                err3=abs(tmp3)   
                maxI3=i  
                
        print "gridyAlgoDowngrade", err2,maxI2
        print "gridyAlgoDowngradeLowBound", err3,maxI2        
        res.write("e="+str(e)+"\n"+
                    "elapsed_time_gridyBadUp "+str( elapsed_time_gridyBad)+"\n"+
                    "elapsed_time_gridyBadDown "+str( elapsed_time_gridyBadDown)+"\n"+
                     "Error gridyAlgoDowngrade "+str(err2)+" "+str(maxI2)+"\n"+   
                    "Error gridyAlgoDowngradeLowBound "+str(err3)+" "+str(maxI3)+"\n")                       
    
        err2=0
        err3=0
    
    for samples in [1000,10000,100000,1000000,10000000]:
        
    #--------------------SAMPLING------------------------
        start_time = time.time()    
        dist0 = constructDistSample(tree.getroot()[0],samples,bine)
        elapsed_time_sampling = time.time() - start_time
        print "elapsed_time_sampling", elapsed_time_sampling 
        d1=0
        for i in sortedDist1: 
        
            d1 = d1 + dist1[i]
            #lessThanTDist1 = lessThanT(dist1,i)
            tmp0 = lessThanT(dist0,i)-d1
            if abs(tmp0)>=err0:
                err0=abs(tmp0)
                maxI0=i  
        print "samplin", err0,maxI0       
        res.write("#samples="+str(samples)+"\n"+
                    "elapsed_time_sampling "+str(elapsed_time_sampling)+"\n"+
                    "Error samplin "+str(err0)+" "+str(maxI0)+"\n")
        err0=0 
        
    
    


    res.write("*****************************************************\n")                
    
    
def testTotal(fileName,fileAttrib,bine,output):
    print "stsrt"
    res=open(output,"a")
    #fileName = sys.argv[1]#'tests/along.xml'
    #fileAttrib =sys.argv[2] #'tests/along_attribUni.xml'
    err1=0
    err2=0
    err3 = 0
    err0 = 0
    maxI0=0
    maxI1=0
    maxI2=0
    maxI3=0
    err5 = 0
    maxI5=0
    tree = readXml(fileName,fileAttrib)
    updateSize(tree.getroot())
    #samples = int(sys.argv[3])
    #bine=float(sys.argv[5])
    #e=float(sys.argv[4])
    e=1
    bine = float(bine)

    res.write(fileName+"\n"+
                    fileAttrib+"\n"+
                    "n="+str(int(tree.getroot()[0].get("size")))+"\n"+
                    "m="+str(1/bine)+"\n")
    start_time = time.time() 
    dist1 = goOverTree(tree.getroot()[0],SumAccurateDescrete,bine,e,1)
    elapsed_time_accurate = time.time() - start_time 
    print "elapsed_time_accurate", elapsed_time_accurate
    
    res.write("elapsed_time_accurate "+str(elapsed_time_accurate)+"\n")
    sortedDist1 = sorted(dist1)

    
    for e in [0.1]:
            
        #--------------------APPROXIMATION - DOWNGRADE - UPPERBOUND------------------------
        start_time = time.time()
        dist3= goOverTree(tree.getroot()[0],gridyAlgoDowngrade,bine,e,int(tree.getroot()[0].get("size")))
        elapsed_time_gridyBad = time.time() - start_time
        print "elapsed_time_gridyBad", elapsed_time_gridyBad
        
        #--------------------APPROXIMATION - DOWNGRADE - LOWERBOUND-------------------------
        start_time = time.time()
        dist4= goOverTree(tree.getroot()[0],gridyAlgoDowngradeLowBound,bine,e,int(tree.getroot()[0].get("size")))
        elapsed_time_gridyBadDown = time.time() - start_time
        print "elapsed_time_gridyBadLowBound", elapsed_time_gridyBadDown
    
        d1=0
    
        for i in sortedDist1: 
            
            d1 = d1 + dist1[i]                        
            tmp2 = lessThanT(dist3,i)-d1
            if tmp2>=err2:
                err2=tmp2   
                maxI2=i
            tmp3 = lessThanT(dist4,i)-d1
            if abs(tmp3)>=err3:
                err3=abs(tmp3)   
                maxI3=i  
                
        print "gridyAlgoDowngrade", err2,maxI2
        print "gridyAlgoDowngradeLowBound", err3,maxI2        
        res.write("e="+str(e)+"\n"+
                    "elapsed_time_gridyBadUp "+str( elapsed_time_gridyBad)+"\n"+
                    "elapsed_time_gridyBadDown "+str( elapsed_time_gridyBadDown)+"\n"+
                     "Error gridyAlgoDowngrade "+str(err2)+" "+str(maxI2)+"\n"+   
                    "Error gridyAlgoDowngradeLowBound "+str(err3)+" "+str(maxI3)+"\n")                       
    
        err2=0
        err3=0
    
    for samples in []:
        
    #--------------------SAMPLING------------------------
        start_time = time.time()    
        dist0 = constructDistSample(tree.getroot()[0],samples,bine)
        elapsed_time_sampling = time.time() - start_time
        print "elapsed_time_sampling", elapsed_time_sampling 
        d1=0
        
	for i in sortedDist1: 
	
	    d1 = d1 + dist1[i]
	    #count=count+1
	    #lessThanTDist1 = lessThanT(dist1,i)
	    
	    tmp0 = lessThanT(dist0,i)-d1
	    if abs(tmp0)>=err0:
		err0=abs(tmp0)
		maxI0=i  
	      
	print "samplin", err0,maxI0       
	res.write("#samples="+str(samples)+"\n"+
		    "elapsed_time_sampling "+str(elapsed_time_sampling)+"\n"+
		    "Error samplin "+str(err0)+" "+str(maxI0)+"\n")
	err0=0 
        
    
    #--------------------OptTrim------------------------
    print "opt"
    start_time = time.time()
    dist5= goOverTree(tree.getroot()[0],sumOptTrim,bine,0.1,int(tree.getroot()[0].get("size")))
    elapsed_time_optrim = time.time() - start_time
    print "elapsed_time_optrim", elapsed_time_optrim
    
    d1=0
    for i in sortedDist1: 
        d1 = d1 + dist1[i]                        
        tmp5 = lessThanT(dist5,i)-d1
        if tmp5>=err5:
            err5=tmp5   
            maxI5=i
    print "optrim", err5,maxI5
    res.write("m="+str(10)+"\n"+
                    "elapsed_time_optrim "+str( elapsed_time_optrim)+"\n"+
                     "Error optrim "+str(err5)+" "+str(maxI5)+"\n")
    
    res.write("*****************************************************\n")                

        
if __name__ == "__main__":
    testTotal("tests/event1.xml", "tests/event1_attrib.xml", 0.5, "testBla.txt")
    #testTotal("tests/along.xml", "tests/along_attribUni2.xml", 0.1, "testBla.txt")
#    print "stsrt"
#    res=open("testLogistics.txt","a")
#    fileName = 'tests/liat.xml'
#    fileAttrib ='tests/liatAttrib.xml'
#    err1=0
#    err2=0
#    err3 = 0
#    err0 = 0
#    maxI0=0
#    maxI1=0
#    maxI2=0
#    maxI3=0
#    tree = readXml(fileName,fileAttrib)
#    updateSize(tree.getroot())
#    tree.write("exampleTree.xml")        
#    samples = 0#int(sys.argv[3])
#    bine=0.25#float(sys.argv[5])
#    e= 0.1#float(sys.argv[4])
#    #--------------------SAMPLING------------------------
#    start_time = time.time()    
#    dist0 = constructDistSample(tree.getroot()[0],samples,bine)
#    elapsed_time_sampling = time.time() - start_time
#    print "elapsed_time_sampling", elapsed_time_sampling    
#    
#    #--------------------APPROXIMATION - BEST------------------------
##    start_time = time.time()
##    dist2= goOverTree(tree.getroot()[0],gridyAlgo,bine,e,int(tree.getroot()[0].get("size")))
##    elapsed_time_gridyGood = time.time() - start_time
##    print "elapsed_time_gridyGood", elapsed_time_gridyGood
#    
#    #--------------------APPROXIMATION - DOWNGRADE - UPPERBOUND------------------------
#    start_time = time.time()
#    dist3= goOverTree(tree.getroot()[0],gridyAlgoDowngrade,bine,e,int(tree.getroot()[0].get("size")))
#    elapsed_time_gridyBad = time.time() - start_time
#    print "elapsed_time_gridyBad", elapsed_time_gridyBad
#    
#    #--------------------APPROXIMATION - DOWNGRADE - LOWERBOUND-------------------------
#    start_time = time.time()
#    dist4= goOverTree(tree.getroot()[0],gridyAlgoDowngradeLowBound,bine,e,int(tree.getroot()[0].get("size")))
#    elapsed_time_gridyBadDown = time.time() - start_time
#    print "elapsed_time_gridyBadLowBound", elapsed_time_gridyBadDown
#    
#    res.write(fileName+"\n"+
#                    fileAttrib+"\n"+
#                    "n="+str(int(tree.getroot()[0].get("size")))+"\n"+
#                    "m="+str(1/bine)+"\n"+
#                    "e="+str(e)+"\n"+
#                    "#samples="+str(samples)+"\n"+
#                    "elapsed_time_sampling "+str(elapsed_time_sampling)+"\n"+ 
#                    #"elapsed_time_gridyGood "+str( elapsed_time_gridyGood)+"\n"+
#                    "elapsed_time_gridyBadUp "+str( elapsed_time_gridyBad)+"\n"+
#                    "elapsed_time_gridyBadDown "+str( elapsed_time_gridyBadDown)+"\n")                    
#    #--------------------ACCURATE-------------------------
#    start_time = time.time() 
#    dist1 = goOverTree(tree.getroot()[0],SumAccurateDescrete,bine,e,1)
#    elapsed_time_accurate = time.time() - start_time 
#    print "elapsed_time_accurate", elapsed_time_accurate
#    
#    sortedDist1 = sorted(dist1)
#    d1=0
#    
#    
#    #maxT = max(dist1.keys())
#    #for i in range(int(maxT)):
#    for i in sortedDist1: 
#        
#        d1 = d1 + dist1[i]
#        #####debug:print d1
#        #lessThanTDist1 = lessThanT(dist1,i)
#        tmp0 = lessThanT(dist0,i)-d1
#        if abs(tmp0)>=err0:
#            err0=abs(tmp0)
#            maxI0=i
##        tmp1 = lessThanT(dist2,i)-d1
##        if tmp1>=err1:
##            err1=tmp1
##            maxI1=i
#        tmp2 = lessThanT(dist3,i)-d1
#        #####debug:print "tmp2 ********",(tmp2+d1)
#        if tmp2>=err2:
#            err2=tmp2   
#            maxI2=i
#        tmp3 = lessThanT(dist4,i)-d1
#        if abs(tmp3)>=err3:
#            err3=abs(tmp3)   
#            maxI3=i    
#        
#    print "samplin", err0,maxI0    
#    print "gridyAlgo", err1,maxI1
#    print "gridyAlgoDowngrade", err2,maxI2
#    print "gridyAlgoDowngradeLowBound", err3,maxI2
#    
#    res.write("elapsed_time_accurate "+str(elapsed_time_accurate)+"\n"+
#                    "Error samplin "+str(err0)+" "+str(maxI0)+"\n"+   
#                    "Error gridyAlgo "+str(err1)+" "+str(maxI1)+"\n"+
#                    "Error gridyAlgoDowngrade "+str(err2)+" "+str(maxI2)+"\n"+   
#                    "Error gridyAlgoDowngradeLowBound "+str(err3)+" "+str(maxI3)+"\n")
#
#    res.write("*****************************************************\n")                
