# -*- coding: utf-8 -*-

import pdb
from toposort import toposort, toposort_flatten
import TopoSort


"""
The Bellman-Ford algorithm
Graph API:
    iter(graph) gives all nodes
    iter(graph[u]) gives neighbours of u
    graph[u][v] gives weight of edge (u, v)
    #From:https://gist.github.com/joninvski/701720
"""

# Step 1: For each node prepare the destination and predecessor
def initialize(graph, source, m):
    d = {} # Stands for destination
    p = {} # Stands for predecessor
    for i in range(m):
        d[i]={}
        p[i]={}
        for node in graph:
            d[i][node] = float('Inf') # We start admiting that the rest of nodes are very very far
            p[i][node] = None
        if i==0:    
            d[i][source] = 0 # For the source we know how to reach
    return d, p

def relax(node, graph, d, p, k):
    # If the distance between the node and the neighbour is lower than the one I have now
    #bottleneck(x) =    min   [max(bottleneck(v),w(e))]
    maxi = -float('Inf')
    for ng in graph[node]:
        maxi = max(d[k-1][node],graph[node][ng])
        if d[k][ng]>maxi:
            d[k][ng] = maxi
            p[k][ng] = node
      

def bellman_ford(graph, source, m):
    d, p = initialize(graph, source,m)
    g = creatGraph(graph)    
    #g = TopoSort.topological(g)
    g = toposort_flatten(g)
    for i in range(m):
        if i==0: continue
        for u in g:
            relax(u, graph, d, p, i) #Lets relax it
    return d, p

def creatGraph(wGraph):
    g={}
    for u in wGraph:
        g[u]=set()
        for v in wGraph[u]:
            g[u].add(v)
    return g   

def test():
    graph = {
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

    
#    g =  TopoSort.creatGraph(graph)    
#    g = TopoSort.topological(g)
    d, p = bellman_ford(graph, 'a',3)
    print d, p
    d == {
        'a':  0,
        'b': -1,
        'c':  2,
        'd': -2,
        'e':  1
        }

    p == {
        'a': None,
        'b': 'a',
        'c': 'b',
        'd': 'e',
        'e': 'b'
        }
    

if __name__ == '__main__': test()



#
## Step 1: For each node prepare the destination and predecessor
#def initialize(graph, source):
#    d = {} # Stands for destination
#    p = {} # Stands for predecessor
#    for node in graph:
#        d[node] = float('Inf') # We start admiting that the rest of nodes are very very far
#        p[node] = None
#    d[source] = 0 # For the source we know how to reach
#    return d, p
#
#def relax(node, graph, d, p):
#    # If the distance between the node and the neighbour is lower than the one I have now
#    #bottleneck(x) =    min   [max(bottleneck(v),w(e))]
#    maxi = -float('Inf')
#    for ng in graph[node]:
#        maxi = max(d[node],graph[node][ng])
#        if d[ng]>maxi:
#            d[ng] = maxi
#            p[ng] = node
#      
#
#def bellman_ford(graph, source):
#    d, p = initialize(graph, source)
#    #for i in range(len(graph)-1): #Run this until is converges
#    g = TopoSort.creatGraph(graph)    
#    g = TopoSort.topological(g)
#    for u in g:
#        #for v in graph[u]: #For each neighbour of u
#            relax(u, graph, d, p) #Lets relax it
#    return d, p
#
