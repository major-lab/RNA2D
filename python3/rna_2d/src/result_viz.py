# -*- coding: utf-8 -*-
""" this script allows the displays of the results of 
centrality search"""

import networkx
import matplotlib
from shapedistance import *
from script import THRESHOLD


with open("result.txt", "r") as r:
    all_lines = r.readlines()
    all_results = [(line.split()[0], int(line.split()[1])) for line in all_lines]

top_results = all_results[0:500]  # arbitrarily choose 100

# initialize the graph object
result_graph = networkx.Graph()

# add the nodes (Vienna dot brackets)
for i in range(0, len(top_results)):
    result_graph.add_node(i)

THRESHOLD = 4

# add the edges between the nodes (if they are at a tree
# edit distance of less than threshold)
for i in range(0, len(top_results)-1):
    for j in range(i+1, len(top_results)):
            tree1 = dot_bracket_to_tree(top_results[i][0])
            tree2 = dot_bracket_to_tree(top_results[j][0])
            distance = unlabeled_distance(tree1, tree2)
            if distance < THRESHOLD:
                result_graph.add_edge(i, j)
                result_graph[i][j]['weight'] = distance

# display the graph
#pos = networkx.spring_layout(result_graph)
networkx.draw(result_graph)#, pos)
#edge_weight=dict([((u,v,),int(d['weight'])) for u,v,d in result_graph.edges(data=True)])

#networkx.draw_networkx_edge_labels(result_graph,pos,edge_labels=edge_weight)
#networkx.draw_networkx_nodes(result_graph,pos)
#networkx.draw_networkx_edges(result_graph,pos)
#networkx.draw_networkx_labels(result_graph,pos)
#matplotlib.pyplot.axis('off')
#matplotlib.pyplot.show()