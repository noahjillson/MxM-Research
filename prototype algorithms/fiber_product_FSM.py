import last_letter_FSM
import legal_next_letters_FSM
import networkx as nx
# import scipy
from itertools import product
import matplotlib.pyplot as plt

def cartesian_product(tup1, tup2): 
    return list(product(tup1, tup2))

# Default values
pentagonal_c_map = {'a': {'b', 'e'}, 'b': {'a', 'c'}, 'c': {'b', 'd'}, 'd': {'e', 'c'}, 'e': {'a', 'd'}}
pentagonal_alphabet = {'a', 'b', 'c', 'd', 'e'}
pentagonal_o_map = {'a': 0, 'c': 1, 'b': 2, 'd': 3, 'e': 4}
pentagonal_lst_alphabet = [{'c'}, {'d'}, {'b'}, {'e'}, {'a'}]

# torus_o_map = {
#                 'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6,
#                 'A': 7, 'B': 8, 'C': 9, 'D': 10, 'E': 11, 'F': 12, 'G': 13,
#                 '1': 14, '2': 15, '3': 16, '4': 17, '5': 18, '6': 19, '7': 20
# }
# torus_c_map = {
#     'a': {'b', 'g', 'D', 'E', '4', '5'}, 'b': {'a', 'c', 'E', 'F', '5', '6'},
#     'c': {'b', 'd', 'F', 'G', '6', '7'}, 'd': {'c', 'e', 'A', 'G', '1', '7'},
#     'e': {'d', 'f', 'A', 'B', '1', '2'}, 'f': {'e', 'g', 'B', 'C', '2', '3'},
#     'g': {'a', 'f', 'C', 'D', '3', '4'},
#     'A': {'d', 'e', 'B', 'G', '4', '5'}, 'B': {'e', 'f', 'A', 'C', '5', '6'},
#     'C': {'f', 'g', 'B', 'D', '6', '7'}, 'D': {'a', 'g', 'C', 'E', '1', '7'},
#     'E': {'a', 'b', 'D', 'F', '1', '2'}, 'F': {'b', 'c', 'E', 'G', '2', '3'},
#     'G': {'c', 'd', 'A', 'F', '3', '4'},
#     '1': {'d', 'e', 'D', 'E', '2', '7'}, '2': {'e', 'f', 'E', 'F', '1', '3'},
#     '3': {'f', 'g', 'F', 'G', '2', '4'}, '4': {'a', 'g', 'A', 'G', '3', '5'},
#     '5': {'a', 'b', 'A', 'B', '4', '6'}, '6': {'b', 'c', 'B', 'C', '5', '7'},
#     '7': {'c', 'd', 'C', 'D', '1', '6'}
# }
# torus_alphabet = {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'A', 'B', 'C', 'D', 'E', 'F', 'G', '1', '2', '3', '4', '5', '6',
#                   '7'}
# torus_lst_alphabet = [{'f'}, {'C'}, {'b'}, {'F'}, {'c'}, {'A'}, {'4'}, {'d'}, {'2'}, {'1'}, {'e'}, {'7'}, {'G'},
#                       {'g'}, {'E'}, {'B'}, {'a'}, {'3'}, {'6'}, {'D'}, {'5'}]

FSM_M = legal_next_letters_FSM.generate_fsm_forbidden_letters(alphabet=pentagonal_alphabet, c_map=pentagonal_c_map, o_map=pentagonal_o_map)

hashable_edges_M = []
for edge in FSM_M[1]:
    hashable_edges_M.append(legal_next_letters_FSM.format_directed_edge(edge))

# add length 1 edges
for node in FSM_M[0]:
    if len(node) == 1:
        hashable_edges_M.append(('', list(node)[0], list(node)[0]))

labeled_edges_M = {
    (ele[0], ele[1]): ele[2] for ele in hashable_edges_M
}

FSM_N = last_letter_FSM.generate_fsm_last_letter(alphabet=pentagonal_alphabet, c_map=pentagonal_c_map)
# print("Vertices: " + str(FSM[0]))
# print("Edges: " + str(FSM[1]))
# print(str(len(FSM[0])) + " Vertices")
# print(str(len(FSM[1])) + " Edges")

hashable_edges_N = []
for edge in FSM_N[1]:
    hashable_edges_N.append(last_letter_FSM.format_directed_edge(edge))

# add length 1 edges
for node in FSM_N[0]:
    if len(node) == 1:
        hashable_edges_N.append(('', list(node)[0], list(node)[0]))

labeled_edges_N = {
    (ele[0], ele[1]): ele[2] for ele in hashable_edges_N
}

# print('labeled_edges_M', labeled_edges_M,'labeled_edges_N' ,labeled_edges_N, sep='\n')

# Take a cartesian product of the torus alphabet with itself as the nodes
nodes = cartesian_product(pentagonal_alphabet, pentagonal_alphabet)

# Join nodes together if they have the same label and edges exist in both
def fiber_product(labeled_edges_1, labeled_edges_2) -> nx.DiGraph:
    final_labeled_edges = {}
    for e1 in labeled_edges_1:
        for e2 in labeled_edges_2:
            if labeled_edges_1[e1] == labeled_edges_2[e2]:
                final_labeled_edges[((e1[0], e2[0]), (e1[1], e2[1]))] = labeled_edges_1[e1]
    G = nx.DiGraph()
    G.add_edges_from(final_labeled_edges)
    return (G, final_labeled_edges)

G, final_edge_labels = fiber_product(labeled_edges_M, labeled_edges_N)

options = {"node_size": 50, "with_labels": True}

pos = nx.circular_layout(G)
nx.draw_networkx_edge_labels(G, pos, final_edge_labels)
nx.draw(G, pos, **options)
# print('Final fiber product: \n', G.edges)
plt.show()
# nx.write_edgelist(G, "test.edgelist")
# for edge in G.edges():
#     print(edge)
#     print(labeled_edges_M[(edge[0][0], edge[1][0])], labeled_edges_N[(edge[0][1], edge[1][1])])

# def save_graph(graph,file_name):
# #initialze Figure
#     plt.figure(num=None, figsize=(20, 20), dpi=80)
#     plt.axis('off')
#     fig = plt.figure(1)
#     pos = nx.spring_layout(graph)
#     nx.draw_networkx_nodes(graph,pos)
#     nx.draw_networkx_edges(graph,pos)
#     nx.draw_networkx_labels(graph,pos)

#     cut = 1.00
#     xmax = cut * max(xx for xx, yy in pos.values())
#     ymax = cut * max(yy for xx, yy in pos.values())
#     plt.xlim(0, xmax)
#     plt.ylim(0, ymax)

#     plt.savefig(file_name,bbox_inches="tight")
#     pylab.close()
#     del fig

# #Assuming that the graph g has nodes and edges entered
# save_graph(G,"my_graph.pdf")
