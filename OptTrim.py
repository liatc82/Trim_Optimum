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
    for p in vals:
        g[p] = {}
        for q in vals:
            if q>p:
                for t in vals[i:j]:
                    c=c+prob[t]
                g[p][q]=c
            c=0
            j=j+1
        i=i+1    
    return g        



def createMPathsGraph(graph,source,m,g):
    if m==0:
        return g
    g[source] =  graph[source]
    for v in graph[source]:
        createMPathsGraph(graph,v,m-1,g)
    return g


def optTrim(prob,m):
    graph = createProbGraph(prob)
    source = min(prob.keys())
    graph = createMPathsGraph(graph, source, m, {})
    d, p = BellmanFord.bellman_ford(graph, source)
    print d, p
    
    
    
    
    
def test():
    prob={1:0.3333, 2:0.3333, 3:0.333}
    print prob
    graph = createProbGraph(prob)
    print graph
    optTrim(prob,2)
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