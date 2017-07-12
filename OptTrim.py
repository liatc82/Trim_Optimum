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
        print s, t
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
    print d
    print p
    print createProb(prob,source,p,m)
    
    
    
    
def test():
    prob1={1:0.3333, 2:0.3333, 3:0.333}
    prob2={1:0.3333, 2:0.4, 3:0.16666, 4:0.1}
    prob={1:0.3333, 20:0.12, 6:0.16666, 4:0.1, 12:0.08, 100:0.05, 50:0.15}
    #print prob
    graph = createProbGraph(prob)
    #print graph
    optTrim(prob,3)
    graph2 = {
        'a': {'b': 1, 'c':  4},
        'b': {'c':  3, 'e':  1},
        'c': {},
        'd': {'b':  1},
        'e': {}
        }
        
    graph1 = {
    'a': {'b': 1, 'c':  4},
    'b': {'c':  3, 'd':  2, 'e':  1},
    'c': {},
    'd': {'b':  1, 'c':  5},
    'e': {'d': 1}
    }
#    print "g2"
#    print createMPathsGraph(graph,'a',3,{})    
    
if __name__ == '__main__': test()    