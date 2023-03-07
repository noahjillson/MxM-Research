import networkx as nx
from itertools import product
import matplotlib.pyplot as plt

# https://codereview.stackexchange.com/questions/86849/cartesian-product-of-two-tuples-python
def cartesian_product(tup1, tup2): 
    return tuple(product(tup1, tup2))

def fiber_product(M: nx.DiGraph, N: nx.DiGraph):
    # The cartesian product of M nodes and N nodes gives the nodes for the fiber product
    M_fiber_N_nodes = cartesian_product(M.nodes, N.nodes) 

    M_fiber_N = nx.DiGraph() 
    M_fiber_N.add_nodes_from(M_fiber_N_nodes)
    
    # Iterate over all edges in both graphs and add edges in the fiber product graph
    for M_edge in M.edges:
        for N_edge in N.edges:
            M_fiber_N.add_edge((M_edge[0],N_edge[0]), (M_edge[1],N_edge[1]))
    return M_fiber_N

def test_fiber_product():
    M = nx.DiGraph()
    N = nx.DiGraph()

    M.add_nodes_from(range(1,4))
    N.add_nodes_from(range(1,4))
    M.add_edge(1,2)
    M.add_edge(2,3)
    N.add_edge(1,2)

    M_x_N = fiber_product(M,N)
    nx.draw(M_x_N, with_labels=True, font_size=15, arrowsize=15, node_size = 1000)
    plt.show()

# test_fiber_product()