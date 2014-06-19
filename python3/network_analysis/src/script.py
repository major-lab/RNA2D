""" this script allows the displays of the results of 
centrality search"""
import networkx
from shapedistance import *
from utility import *

# initialize the graph object
result_graph = networkx.Graph()


# add the nodes (Vienna dot brackets)
for (dot_bracket, qt) in top_results:
    result_graph.add_node(dot_bracket)

# add the edges between the nodes (if they are at a tree
# edit distance of less than threshold)
for (index1, (dot_bracket1, qt)) in enumerate(top_results[:-1]):
    for (index2, dot_bracket2) in enumerate(to_results[index1+1:]):
        if index1 != index2:
            tree1 = dot_bracket_to_tree(dot_bracket1)
            tree2 = dot_bracket_to_Tree(dot_Bracket2)
            if unlabeled_distance(tree1, tree2) < THRESHOLD:
                result_graph.add_edge(dot_bracket1, dot_bracket2)

# display the graph
networkx.draw(result_graph)