# -*- coding: utf-8 -*-
"""
Created on Thu Jul  6 22:12:17 2017

@author: liat
"""
import BellmanFord

def createProbGraph(prob):
    g={}
    c=0
    i=1
    j=0
    vals = prob.keys()
    vals.sort()
    vals.append(float('Inf'))
    for p in vals:
        g[p] = {}
        j=0
        for q in vals:
            if q>p:
                for t in vals[i:j]:
                    c=c+prob[t]
                g[p][q]=c
            c=0
            j=j+1
        i=i+1    
    return g        

def createProb(prob,source,p,m):
    s = float('Inf')
    t = float('Inf')
    aProb = {}
    i=m
    while s:
        s = p[i][s]
        aProb[s] = getSubProbSum(prob,s,t)
        t=s
        i=i-1
        if s==source: break
    return aProb

def getSubProbSum(prob,s,t):
    res = 0
    for i in prob.keys():
        if i>=s and i<t:
            res = res + prob[i]
    return res        
    
def optTrim(prob,m):
    graph = createProbGraph(prob)
    source = min(prob.keys())
    d, p = BellmanFord.bellman_ford(graph, source,m+1)
    #print d
    #print p
    return createProb(prob,source,p,m)
    
def appxProb(prob,m):   #shorter algo?
    vals = prob.keys()
    vals.sort()
    n = len(vals)-m
    minVals = min(vals)
    vals.remove(minVals)
    for i in range(n):
        mini = float('Inf')
        vals = prob.keys()
        vals.sort()
        vals.remove(minVals)
        for v in vals:
            if prob[v]<mini:
                mini = prob[v]
                vMin = v
        prv = minVals
        for v in vals:
            if v==vMin:
                prob[prv] = prob[prv]+prob[v]
                prob.pop(v)
                break
            prv = v  
    return prob           

def sumRandVars(p1,p2):
    p={}
    for v1 in p1.keys():
        for v2 in p2.keys():
            if not p.has_key(v1+v2):
                p[v1+v2] = 0
            p[v1+v2]= p[v1+v2]+ p1[v1]*p2[v2]
    return p        
        
def test():
    prob={1:0.3333, 20:0.12, 6:0.16666, 4:0.1, 12:0.08, 100:0.05, 50:0.15}
    prob1={1:1.0/3, 2:1.0/3, 3:1.0/3}
    p= sumRandVars(prob1,prob1)
    print "p=prob1+prob1:", p
#    prob2={1:0.3333, 2:0.4, 3:0.16666, 4:0.1}
#    #print prob
#    graph = createProbGraph(prob)
#    #print graph
    print "optTrim(p,2):",optTrim(p,2)
    
    p1= optTrim(prob1,2)
    print "p1:", p1
    
    p2 = sumRandVars(p1,p1)
    print "p2=p1+p1:",p2
    print "optTrim(p2,2):", optTrim(p2,2)
    
    print prob1
    print "p1:", p1
    p3 = sumRandVars(p1,prob1)
    print "p1+prob1=",p3
    print "optTrim(p3,2):", optTrim(p3,2)
#    print appxProb(p2,2)
#    p1 = {1:1.0/4, 4:3.0/4}
#    p2 = {1:1.0/16, 4:15.0/16}
#    p= sumRandVars(p1,p2)
#    p3 = {2:1.0/16, 5:3.0/8, 8:9.0/16}
#    p= sumRandVars(p,p3)
#    print p
#    graph2 = {
#        'a': {'b': 1, 'c':  4},
#        'b': {'c':  3, 'e':  1},
#        'c': {},
#        'd': {'b':  1},
#        'e': {}
#        }
#        
#    graph1 = {
#    'a': {'b': 1, 'c':  4},
#    'b': {'c':  3, 'd':  2, 'e':  1},
#    'c': {},
#    'd': {'b':  1, 'c':  5},
#    'e': {'d': 1}
#    }

if __name__ == '__main__': test()    