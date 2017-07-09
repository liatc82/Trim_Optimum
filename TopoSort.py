# -*- coding: utf-8 -*-
from collections import deque
"""
Created on Thu Jul  6 12:36:50 2017

@author: liat

taken from: https://gist.github.com/kachayev/5910538
"""

# Simple:
# a --> b
#   --> c --> d
#   --> d 
graph1 = {
    "a": ["b", "c", "d"],
    "b": [],
    "c": ["d"],
    "d": []
}

# 2 components
graph2 = {
    "a": ["b", "c", "d"],
    "b": [],
    "c": ["d"],
    "d": [],
    "e": ["g", "f", "q"],
    "g": [],
    "f": [],
    "q": []
}

# cycle
graph3 = {
    "a": ["b", "c", "d"],
    "b": [],
    "c": ["d", "e"],
    "d": [],
    "e": ["g", "f", "q"],
    "g": ["c"],
    "f": [],
    "q": []
}

GRAY, BLACK = 0, 1

def creatGraph(wGraph):
    g={}
    for u in wGraph:
        g[u]=[]
        for v in wGraph[u]:
            g[u].append(v)
    return g        
            
        

def topological(graph):
    order, enter, state = deque(), set(graph), {}

    def dfs(node):
        state[node] = GRAY
        for k in graph.get(node, ()):
            sk = state.get(k, None)
            if sk == GRAY: raise ValueError("cycle")
            if sk == BLACK: continue
            enter.discard(k)
            dfs(k)
        order.appendleft(node)
        state[node] = BLACK

    while enter: dfs(enter.pop())
    return order

# check how it works
print topological(graph1)
print topological(graph2)
try: topological(graph3)
except ValueError: print "Cycle!"