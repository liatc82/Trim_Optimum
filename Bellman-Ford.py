# -*- coding: utf-8 -*-

import pdb
"""
The Bellman-Ford algorithm
Graph API:
    iter(graph) gives all nodes
    iter(graph[u]) gives neighbours of u
    graph[u][v] gives weight of edge (u, v)
"""
#From:https://gist.github.com/joninvski/701720
# Step 1: For each node prepare the destination and predecessor
def initialize(graph, source):
    d = {} # Stands for destination
    p = {} # Stands for predecessor
    for node in graph:
        d[node] = float('Inf') # We start admiting that the rest of nodes are very very far
        p[node] = None
    d[source] = 0 # For the source we know how to reach
    return d, p

def relax(node, graph, d, p):
    # If the distance between the node and the neighbour is lower than the one I have now
    #bottleneck(x) =    min   [max(bottleneck(v),w(e))]
    maxi = -float('Inf')
    for ng in graph[node]:
        maxi = max(d[node],graph[node][ng])
        d[ng] = min(maxi,d[ng])
      

def bellman_ford(graph, source):
    d, p = initialize(graph, source)
    for i in range(len(graph)-1): #Run this until is converges
        for u in graph:
            #for v in graph[u]: #For each neighbour of u
                relax(u, graph, d, p) #Lets relax it

    return d, p


def test():
    
    graph = {
        'a': {'b': 1, 'c':  4},
        'b': {'c':  3, 'd':  2, 'e':  1},
        'c': {},
        'd': {'b':  1, 'c':  5},
        'e': {'d': 1}
        }
        
    d, p = bellman_ford(graph, 'a')
    print iter(graph)
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