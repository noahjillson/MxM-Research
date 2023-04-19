from word import Word, WordGenerator
import networkx as nx
import matplotlib.pyplot as plt
from itertools import product
import json


class FSMGenerator:
    def __init__(self, commutation_dict: dict[str: list], order_dict: dict[str: int]):
        """
        Initialize a Finite State Machine (FSM) Generator Object. Using the defining graph of a right-angled coxeter
        group, necessary short-lex, last-letter, and fiber-product machines can be created.

        :param commutation_dict: A dictionary representation of a defining graph. A letter (key) is associated with a list of letters (value) in the dictionary such that all letters in the list commute with the key
        :param order_dict: A dictionary representation of a total ordering on the letter in the defining graph. A letter (key) is associated with an index (value) that represents that letters relative position in the ordering.
        """
        self.c_map = commutation_dict
        self.o_map = order_dict
        self.alphabet = set().union(letter for letter in self.o_map)
        self.language = WordGenerator(self.c_map, self.o_map)

    def __format_directed_edge(self, edge: tuple[set, set, str]):
        """Make a directed edge (of length 3) to a tuple of 3 strings"""
        hashable_edge = [None] * 3

        hashable_edge[0] = ''.join(sorted(list(edge[0])))
        hashable_edge[1] = ''.join(sorted(list(edge[1])))
        hashable_edge[2] = edge[2]

        return hashable_edge

    def __generate_short_lex_vertices_edges(self):
        """
        Generate the finite state machine of all possible last letters. Edges represent writing a letter while vertices
        represent the set of possible last letters given the edge's follower / letters written.

        :return: list of lists; The first entry is the list of vertices; The second is the list of edges.
        """
        origin = self.alphabet
        vertices = [origin]
        edges = []
        frontier = []

        for letter in self.alphabet:
            destination = Word(letter, self.c_map, self.o_map).legal_next_letters()
            frontier.append(destination)
            edges.append((origin, destination, letter))

        while len(frontier) > 0:
            source = frontier.pop(0)

            # We have already considered source and all its outgoing edges, we can skip its consideration
            if source in vertices:
                continue
            vertices.append(source)

            # Record outgoing edges from source, this is guaranteed to be unique by above if-statement
            # Add the destination vertex, destination, to our frontier to ensure all vertices are reached
            for edge in source:
                destination = Word(edge, self.c_map, self.o_map).forbidden_letters()\
                    .union(self.alphabet.copy().difference(source).intersection(set(self.c_map[edge])))
                destination = self.alphabet.copy().difference(destination)
                frontier.append(destination)
                edges.append((source, destination, edge))

        return {'vertices': vertices, 'edges': edges}
    
    def __generate_last_letter_vertices_edges(self):
        origin = ''
        vertices = []
        edges = []
        frontier = []

        # Initialize the frontier
        for letter in self.alphabet:
            destination = Word(letter, self.c_map, self.o_map).last_letters()
            edges.append((origin, destination, letter))
            frontier.append(set(letter))

        while len(frontier) > 0:
            v = frontier.pop(0)

            # We have already considered v and all its outgoing edges, we can skip its consideration
            if v in vertices:
                continue
            vertices.append(v)

            # Record outgoing edges from v, this is guaranteed to be unique by above if-statement
            # Add the destination vertex, u, to our frontier to ensure all vertices are reached
            for e in self.alphabet.copy().difference(v):
                u = set(e).union(v.intersection(self.c_map[e]))
                frontier.append(u)
                edges.append([v, u, e])

        return {'vertices': vertices, 'edges': edges}

    def generate_short_lex_fsm_as_networkx(self):
        # Generate the short-lex FSM as a dictionary of vertices and edges
        fsm = self.__generate_short_lex_vertices_edges()

        # Represent edges as strings so that they can be hashed by networkx
        hashable_edges = []
        for edge in fsm['edges']:
            hashable_edges.append(self.__format_directed_edge(edge))

        # Associate each edge (key) with a dictionary containing its label (value)
        labeled_edges = {
            (ele[0], ele[1]): {'label': ele[2]} for ele in hashable_edges
        }

        G = nx.DiGraph()
        G.add_edges_from(labeled_edges)
        nx.set_edge_attributes(G, labeled_edges)
        return G

    def generate_last_letter_fsm_as_networkx(self):
        # Generate the short-lex FSM as a dictionary of vertices and edges
        fsm = self.__generate_last_letter_vertices_edges()

        # Represent edges as strings so that they can be hashed by networkx
        hashable_edges = []
        for edge in fsm['edges']:
            hashable_edges.append(self.__format_directed_edge(edge))

        for node in fsm['vertices']:
            if len(node) == 1:
                hashable_edges.append(('', list(node)[0], list(node)[0]))
        
        # Associate each edge (key) with a dictionary containing its label (value)
        labeled_edges = {
            (ele[0], ele[1]): {'label': ele[2]} for ele in hashable_edges
        }

        G = nx.DiGraph()
        G.add_edges_from(labeled_edges)
        nx.set_edge_attributes(G, labeled_edges)
        return G

    def generate_fiber_product_fsm_as_networkx(self):
        """
        Create a fiber product of our shortlex and last_letter machine to starte generating 
        adjacent words on the horosphere.
        """
        shortlex_fsm = self.__generate_short_lex_vertices_edges()
        last_letter_fsm = self.__generate_last_letter_vertices_edges()

        fiber_graph = nx.DiGraph() 

        labeled_edges = {}
        
        # Iterate over all edges in both graphs and add edges in the fiber product graph
        for shortlex_edge in shortlex_fsm['edges']:
            for last_letter_edge in last_letter_fsm['edges']:
                # Format edges for comparison and to add to graph
                shortlex_formatted = self.__format_directed_edge(shortlex_edge)
                last_letter_formatted = self.__format_directed_edge(last_letter_edge)
                
                # Check if edges have the same label, and add it to the graph if so
                if shortlex_formatted[2] == last_letter_formatted[2]:
                    labeled_edges[(shortlex_formatted[0], last_letter_formatted[0]),\
                                  (shortlex_formatted[1], last_letter_formatted[1])] = {'label': shortlex_formatted[2]}
                    
        fiber_graph.add_edges_from(labeled_edges)
        nx.set_edge_attributes(fiber_graph, labeled_edges)
        return fiber_graph

    def generate_short_lex_fsm_as_adj(self):
        return self.generate_short_lex_fsm_as_networkx().adj

    def generate_last_letter_fsm_as_adj(self):
        return self.generate_last_letter_fsm_as_networkx().adj

    def generate_fiber_product_fsm_as_adj(self):
        return self.generate_fiber_product_fsm_as_networkx().adj
    
    def generate_fiber_product_fsm_as_dict(self):
        """
        Creates a dictionary of the fiber product that allows for fast graph traversing.
        """
        fsm_dict = {}

        adj = self.generate_fiber_product_fsm_as_adj()
        for v, v_adj in adj.items():
            fsm_dict[v] = {}
            for u in v_adj:
                fsm_dict[v][v_adj[u]['label']] = tuple(u)
        self.fsm_dict = fsm_dict
        return fsm_dict

    def visualize_fsm(self, G):
        pos = nx.circular_layout(G, dim=2)
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
        nx.draw_networkx_edge_labels(G, pos)
        nx.draw(G, pos, **options)
        plt.show()

    def locate_associated_state(self, word):
        current_state = (''.join(sorted(self.alphabet)), '')

        # Lookup in this sense is linear with respect to length of our word
        for l in word:
            current_state = self.fsm_dict[current_state][l]

        return current_state
    
    def all_length_words(self, n):
        """
        Finds all words that have a suffix up to length n with a BFS
        """
        n += 1
        fix_words = 'ac' * n
        origin = (''.join(sorted(self.alphabet)), '')

        # All elements of the frontier are of the form (node, current depth, word), we want the words
        frontier = [(origin, 0, '')]
        words_out = []
        # visited = set()

        while frontier:
            node, depth, word = frontier.pop(0)
            # Only go to depth n
            if depth == n:
                continue
            if word.startswith('a') or word.startswith('c'):
                continue
            # visited.add(node)
            words_out.append(word)
            for next_letter in self.locate_associated_state(word)[0]:
                frontier.append((self.fsm_dict[node][next_letter],\
                                    depth+1, word + next_letter))
        
        return [fix_words[:len(word)] + word for word in words_out]
    
    # TODO: Update this algorithm to the new method
    def adj_words(self, word, G):
        if word == '':
            return
        word_prefix = word[:len(word) // 2]
        word_suffix = word[len(word) // 2:]
        word_node = self.locate_associated_state(word_suffix)

        # print('CASE 1 (same-length) CONNECTIONS:')
        # find a subset of the adjacent words on the horosphere of the same length
        for last_letter in word_node[1]:
            adj_word = word_suffix[::-1].replace(last_letter, '', 1)[::-1]
            for add in self.locate_associated_state(adj_word)[0]:
                # add the possible legal remaining letters so we are still on the horosphere
                # if the length of the test word is 2, then 'ac' and 'aa' will get registered as on the horosphere
                if len(word) == 2:
                    # so we do not consider possible added letters that would be on the ray or cancel
                    if add not in {'a', 'c'}:
                        # print(word, '--', word[:len(word) // 2] + adj_word + add)
                        G.add_node(word[:len(word) // 2] + adj_word + add)
                        if (word[:len(word) // 2] + adj_word + add != word):
                            G.add_edge(word, word[:len(word) // 2] + adj_word + add)
                else:
                    # print(word, '--', word[:len(word) // 2] + adj_word + add)
                    G.add_node(word[:len(word) // 2] + adj_word + add)
                    if (word[:len(word) // 2] + adj_word + add != word):
                        # print(word, '--')
                        G.add_edge(word, word[:len(word) // 2] + adj_word + add)

        # print('CASE 2 ((n -- n-2)-length) CONNECTIONS:')
        # test if the last letter of prefix ray can commute with test_word (subset check)
        if set(word_suffix) <= self.c_map[word[len(word) // 2 - 1]]: 
            # get the word without the last letter of the prefix (since it will cancel)
            reduced_test_word = word_prefix[:-1] + word_suffix
            # use the possible last letters to make another cancellation and still remain of the horosphere
            for last_letter in word_node[1]:
                adj_word = reduced_test_word[::-1].replace(last_letter, '', 1)[::-1]
                # print(word, '--', adj_word)
                G.add_node(adj_word)
                if adj_word != word:
                    G.add_edge(word, adj_word)

    def visualize_horosphere(self, G):
        pos = nx.spring_layout(G, dim=2)
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
        nx.draw(G, pos, **options)
        plt.show()



pentagonal_c_map = {'a': {'b', 'e'}, 'b': {'a', 'c'}, 'c': {'b', 'd'}, 'd': {'e', 'c'}, 'e': {'a', 'd'}}
pentagonal_alphabet = {'a', 'b', 'c', 'd', 'e'}
pentagonal_lst_alphabet = [{'c'}, {'d'}, {'b'}, {'e'}, {'a'}]
pentagonal_o_map = {'a': 0, 'c': 1, 'b': 2, 'd': 3, 'e': 4}

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

torus_o_map = {
                'a': 0, 'b': 2, 'c': 1, 'd': 3, 'e': 4, 'f': 5, 'g': 6,
                'A': 7, 'B': 8, 'C': 9, 'D': 10, 'E': 11, 'F': 12, 'G': 13,
                '1': 14, '2': 15, '3': 16, '4': 17, '5': 18, '6': 19, '7': 20
}

# generator = FSMGenerator(commutation_dict=torus_c_map, order_dict=torus_o_map)
generator = FSMGenerator(commutation_dict=pentagonal_c_map, order_dict=pentagonal_o_map)
networkx = generator.generate_short_lex_fsm_as_networkx()
networkx2 = generator.generate_last_letter_fsm_as_networkx()
# fiber_nx = generator.generate_fiber_product_fsm_as_networkx()

# generator.visualize_fsm(networkx)
# generator.visualize_fsm(networkx2)
# generator.visualize_fsm(fiber_nx)
generator.generate_fiber_product_fsm_as_dict()
# pprint(adj)

# print(generator.locate_associated_state('acadec'))
n = 3
all_words = generator.all_length_words(n)

# print(all_words)
print(len(all_words))

Horosphere = nx.Graph()

for w in all_words:
    generator.adj_words(w, Horosphere)

generator.visualize_horosphere(Horosphere)

# generator.visualize_fsm(Horosphere)

# nx.write_graphml_lxml(Horosphere, "horosphere_1.graphml")
