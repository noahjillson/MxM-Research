import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import numpy as np
import random
from typing import List, Tuple

# Default values
pentagonal_c_map = {'a': {'b', 'e'}, 'b': {'a', 'c'}, 'c': {'b', 'd'}, 'd': {'e', 'c'}, 'e': {'a', 'd'}}
pentagonal_alphabet = {'a', 'b', 'c', 'd', 'e'}
pentagonal_lst_alphabet = [{'c'}, {'d'}, {'b'}, {'e'}, {'a'}]

torus_o_map = {
                'a': 0, 'b': 2, 'c': 1, 'd': 3, 'e': 4, 'f': 5, 'g': 6,
                'A': 7, 'B': 8, 'C': 9, 'D': 10, 'E': 11, 'F': 12, 'G': 13,
                '1': 14, '2': 15, '3': 16, '4': 17, '5': 18, '6': 19, '7': 20
}
torus_c_map = {
    'a': {'b', 'g', 'D', 'E', '4', '5'}, 'b': {'a', 'c', 'E', 'F', '5', '6'},
    'c': {'b', 'd', 'F', 'G', '6', '7'}, 'd': {'c', 'e', 'A', 'G', '1', '7'},
    'e': {'d', 'f', 'A', 'B', '1', '2'}, 'f': {'e', 'g', 'B', 'C', '2', '3'},
    'g': {'a', 'f', 'C', 'D', '3', '4'},
    'A': {'d', 'e', 'B', 'G', '4', '5'}, 'B': {'e', 'f', 'A', 'C', '5', '6'},
    'C': {'f', 'g', 'B', 'D', '6', '7'}, 'D': {'a', 'g', 'C', 'E', '1', '7'},
    'E': {'a', 'b', 'D', 'F', '1', '2'}, 'F': {'b', 'c', 'E', 'G', '2', '3'},
    'G': {'c', 'd', 'A', 'F', '3', '4'},
    '1': {'d', 'e', 'D', 'E', '2', '7'}, '2': {'e', 'f', 'E', 'F', '1', '3'},
    '3': {'f', 'g', 'F', 'G', '2', '4'}, '4': {'a', 'g', 'A', 'G', '3', '5'},
    '5': {'a', 'b', 'A', 'B', '4', '6'}, '6': {'b', 'c', 'B', 'C', '5', '7'},
    '7': {'c', 'd', 'C', 'D', '1', '6'}
}
torus_alphabet = {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'A', 'B', 'C', 'D', 'E', 'F', 'G', '1', '2', '3', '4', '5', '6',
                  '7'}
torus_lst_alphabet = [{'f'}, {'C'}, {'b'}, {'F'}, {'c'}, {'A'}, {'4'}, {'d'}, {'2'}, {'1'}, {'e'}, {'7'}, {'G'},
                      {'g'}, {'E'}, {'B'}, {'a'}, {'3'}, {'6'}, {'D'}, {'5'}]

def neighborhood(p: int, c_map=torus_c_map) -> set[str]:
    """Return the 1.5 radius neighborhood around point p (just p and all its adjacent vertices)"""
    nbhd = set(c_map[p])
    # nbhd.append(p)
    return nbhd

def legal_next_letters(w: str, alphabet=torus_alphabet, c_map=torus_c_map, o_map=torus_o_map) -> set[str]:
    return alphabet - forbidden_letters(w=w, alphabet=alphabet, c_map=c_map, o_map=o_map)


def forbidden_letters(w: str, alphabet=torus_alphabet, c_map=torus_c_map, o_map=torus_o_map) -> set[str]:
    """
    Find the forbidden letters for a word w.s

    Params:
    :w str: The input word.
    :return: The list of forbidden letters that can follow w.
    """

    if len(w) == 1:
        # If the word length is 1, then the last letters are just the adjacent letters than come before that letter
        return set(filter(lambda x: o_map[x] > o_map[w], neighborhood(w, c_map)))
    else:
        # F(wl) = F(l) union (F(w) intersection N_l)
        return alphabet - forbidden_letters(w[-1]) \
                    .union(forbidden_letters(w[:-1], c_map=c_map, o_map=o_map) \
                    .intersection(neighborhood(w[-1], c_map=c_map)))

def generate_fsm_forbidden_letters(alphabet=torus_alphabet, c_map=torus_c_map, o_map=torus_o_map) -> list:
    """
    Generate the finite state machine of all possible last letters. Edges represent writing a letter while vertices
    represent the set of possible last letters given the edges follower / letters written.

    :return: list of lists; The first entry is the list of vertices; The second is the list of edges.
    """
    vertices = []
    edges = []
    frontier = []
    origin = alphabet

    for l in alphabet:
        frontier.append(forbidden_letters(l, alphabet=alphabet, c_map=c_map, o_map=o_map))

    while len(frontier) > 0:
        v = frontier.pop(0)

        # We have already considered v and all its outgoing edges, we can skip its consideration
        if v in vertices:
            continue
        vertices.append(v)

        # Record outgoing edges from v, this is guaranteed to be unique by above if-statement
        # Add the destination vertex, u, to our frontier to ensure all vertices are reached
        for e in v:
            u = forbidden_letters(e, alphabet=alphabet, c_map=c_map, o_map=o_map). \
                union(alphabet.copy().difference(v).intersection(neighborhood(e)))
            u = alphabet.copy().difference(u)
            frontier.append(u)
            # print('connecting', v, 'to', u, 'by', e)
            edges.append((v, u, e))
            

    return [vertices, edges]

def format_directed_edge(edge: Tuple[set[str], set[str], str]) -> Tuple[str, str, str]:
    """Make a directed edge (of length 3) to a tuple of 3 strings"""
    hashable_edge = [None] * 3

    hashable_edge[0] = ''.join(sorted(list(edge[0])))
    hashable_edge[1] = ''.join(sorted(list(edge[1])))

    return (hashable_edge[0], hashable_edge[1], edge[2])

def display_fsm(G: nx.DiGraph):
    # colors = np.random.rand(126, 4)
    pos = nx.circular_layout(G, dim=2)

    # colors = []
    # for i in range(127):
    #     hue = i / 127.0
    #     red, green, blue = colorsys.hsv_to_rgb(hue, 1, 1)
    #     alpha = random.random()
    #     colors.append((red, green, blue, alpha))

    # node_colors = []
    # for node in G:
    #     if len(node) == 3:
    #         node_colors.append(matplotlib.colors.to_rgba("#ff96d5", 1))
    #     elif len(node) == 2:
    #         node_colors.append(matplotlib.colors.to_rgba("#96b9ff", 1))
    #     elif len(node) == 1:
    #         node_colors.append(matplotlib.colors.to_rgba("#e4ff85", 1))
    #     elif node == '':
    #         node_colors.append(matplotlib.colors.to_rgba("#000000", 1))

    # edge_colors = []
    # alph1 = 0.5
    # alph2 = 0.5
    # alph3 = 0.5
    # for edge in G.edges:
    #     s = edge[0]
    #     e = edge[1]

    #     if len(s) == 1 and len(e) == 1:
    #         edge_colors.append(matplotlib.colors.to_rgba("#00a76c", alph1))  # Blue
    #     if len(s) == 1 and len(e) == 2:
    #         edge_colors.append(matplotlib.colors.to_rgba("#00c6f8", alph1))  # Turquoise
    #     if len(s) == 1 and len(e) == 3:
    #         edge_colors.append(matplotlib.colors.to_rgba("#b80058", alph1))  # Maroon
    #     if len(s) == 2 and len(e) == 1:
    #         edge_colors.append(matplotlib.colors.to_rgba("#ebac23", alph2))  # Orange
    #     if len(s) == 2 and len(e) == 2:
    #         edge_colors.append(matplotlib.colors.to_rgba("#3A3CA6", alph2))  # Blue
    #     if len(s) == 2 and len(e) == 3:
    #         edge_colors.append(matplotlib.colors.to_rgba("#d163e6", alph2))  # Lavender
    #     if len(s) == 3 and len(e) == 1:
    #         edge_colors.append(matplotlib.colors.to_rgba("#c22f4e", alph3))  # Red
    #     if len(s) == 3 and len(e) == 2:
    #         edge_colors.append(matplotlib.colors.to_rgba("#00a76c", alph3))  # Jade
    #     if len(s) == 3 and len(e) == 3:
    #         edge_colors.append(matplotlib.colors.to_rgba("#b24502", alph3))  # Brown


    # print(len(colors))
    options = {
        # "node_color": node_colors,
        # "edge_color": edge_colors,
        # "width": 4,
        "font_size": 8,
        # "edge_cmap": plt.cm.Blues,
        "with_labels": True,
        "node_size": 250,
        "font_color": "black"
    }

    # colors = []
    # for node in G:
    #     if len(node) == 3:
    #         colors.append(matplotlib.colors.to_rgba("#ff96d5", 1))
    #     elif len(node) == 2:
    #         colors.append(matplotlib.colors.to_rgba("#96b9ff", 1))
    #     elif len(node) == 1:
    #         colors.append(matplotlib.colors.to_rgba("#e4ff85", 1))
    #     elif len(node) == 0:
    #         colors.append(matplotlib.colors.to_rgba("#b0b0b0", 1))


    # x = [pos[n][0] for n in G.nodes()]
    # y = [pos[n][1] for n in G.nodes()]
    #z = [pos[n][2] for n in G.nodes()]

    # fig = plt.figure()
    # ax = fig.add_subplot(111, projection='3d')
    # ax.scatter(x, y, z, color='red')
    # edges = [(u, v) for (u, v) in G.edges()]
    # for (u, v) in edges:
    #     ax.plot([pos[u][0], pos[v][0]], [pos[u][1], pos[v][1]], [pos[u][2], pos[v][2]], color='black', alpha=.2)
    #print(pos)
    # nx.draw_networkx_nodes(G, pos, edgecolors="black")
    pos[''] = [0.051, 0]
    nx.draw(G, pos, **options)
    # nx.draw_networkx_edge_labels(G, pos, edge_labels=hashable_edges_dictionary)
    #plt.legend(["1—>1", "1—>2", "1—>3", "2—>1", "2—>2", "2—>3", "3—>1", "3—>2", "3—>3"])

    # one = mlines.Line2D([], [], color='#00a76c', marker='>', ls='', label='1—>1')
    # two = mlines.Line2D([], [], color='blue', marker='>', ls='', label='9')
    # # etc etc
    # plt.legend(handles=[one, two])

    plt.show()

# c_map = torus_c_map  # pentagonal_c_map
# alphabet = torus_alphabet  # pentagonal_alphabet
# lst_alphabet = torus_lst_alphabet  # pentagonal_lst_alphabet

# FSM = generate_fsm_forbidden_letters(alphabet=pentagonal_alphabet, c_map=pentagonal_c_map)
# # # print("Vertices: " + str(FSM[0]))
# # # print("Edges: " + str(FSM[1]))
# # print(str(len(FSM[0])) + " Vertices")
# # print(str(len(FSM[1])) + " Edges")

# hashable_edges = []
# for edge in FSM[1]:
#     hashable_edges.append(format_directed_edge(edge))

# # # add length 1 edges
# for node in FSM[0]:
#     if len(node) == 1:
#         hashable_edges.append(('', list(node)[0], list(node)[0]))

# labeled_edges = {
#     (ele[0], ele[1]): ele[2] for ele in hashable_edges
# }

# print(labeled_edges)s

# G = nx.DiGraph()
# nx.set_edge_attributes(G, labeled_edges)
# G.add_edges_from(labeled_edges)
# print(G.number_of_nodes())
# print(G.adj)
# print(G.adj['ab'])
# display_fsm(G)
# pentagonal_o_map = {'a': 0, 'c': 1, 'b': 2, 'd': 3, 'e': 4}
# print("Legal next letters: " + str(legal_next_letters('ec', pentagonal_alphabet, pentagonal_c_map, pentagonal_o_map)))
# print(legal_next_letters('c', pentagonal_alphabet, pentagonal_c_map, pentagonal_o_map))
#print(neighborhood('b', pentagonal_c_map))
# AAAAAAHHHH, The lambda function and filter seems to be giving the wrong answer here. clearly 'b' has forbidden letters
# The forbidden letters of a single letter should be the letters that commute with your letter 'l' and come before it
# as well as the letter itself as we cannot write 'l' twice
#print(set(filter(lambda x: pentagonal_o_map[x] < pentagonal_o_map['b'], neighborhood('b', c_map=pentagonal_c_map))))

