import networkx
import matplotlib.colors
from word import Word, WordGenerator
from FSM_Generator import FSMGenerator
import networkx as nx
import matplotlib.pyplot as plt


class HorosphereGenerator:
    def __init__(self, commutation_dict: dict[str, set], order_dict: dict[str, int], ray: list[str] = ['a', 'c']):
        """
        Initialize a Horosphere Generator Object. Using the defining graph of a right-angled coxeter
        group, horosphere's can be created can be created.

        :param commutation_dict: A dictionary representation of a defining graph. A letter (key) is associated with a list of letters (value) in the dictionary such that all letters in the list commute with the key.
        :param order_dict: A dictionary representation of a total ordering on the letter in the defining graph. A letter (key) is associated with an index (value) that represents that letters relative position in the ordering.
        :param ray: A list representing our ray of alternating letters (typically 'a' and 'c').
        """
        self.c_map = commutation_dict
        self.o_map = order_dict
        self.alphabet = set().union(letter for letter in self.o_map)
        self.ray = ray
        fsm_gen = FSMGenerator(self.c_map, self.o_map)
        self.fiber_product_fsm = fsm_gen.generate_fiber_product_fsm_as_dict()

    def locate_associated_state(self, word: str):
        """
        The number of adjacencies of a node is bounded above by the number of letters in out alphabet/defining graph
        Thus we result in a pseudo-polynomial algorithm for canonical word lookup in our FSM. Correctness is dependent
        on word being constructible via traversal through the FSM. Complexity O(nD) where n is the length of the word
        and D is the number of letters in our alphabet/defining graph.

        :param word: The word for which we want to find the associated fiber product FSM state.
        :return: A fiber product FSM state (A, B) where A denotes the letters that can be written while keeping the word short-lex and B denotes the letters that can be commuted to be last in the word.
        """
        current_state = (''.join(sorted(self.alphabet)), '')
        # Lookup in this sense is linear with respect to length of our word
        for letter in word:
            current_state = self.fiber_product_fsm[current_state][letter]

        return current_state

    def get_all_length_n_words(self, n: int):
        """
        Finds all words that have a suffix up to length n with a BFS

        :param n: The depth with which the BFS will be conducted. The algorithm will compute all short-lex words of this length.
        :return: All possible short-lex words of length n.
        """
        n += 1
        origin = (''.join(sorted(self.alphabet)), '')

        # All elements of the frontier are of the form (node, current depth, word)
        frontier = [(origin, 0, '')]
        # We will add the words to words_out
        words_out = []

        while frontier:
            node, depth, word = frontier.pop(0)
            # Only go to depth n
            if depth == n:
                continue

            # Ignore words that start with the letters in our ray
            if word.startswith(self.ray[0]) or word.startswith(self.ray[1]):
                continue
            
            words_out.append(word)

            # Continue traversing
            for next_letter in self.locate_associated_state(word)[0]:
                frontier.append((self.fiber_product_fsm[node][next_letter], depth+1, word + next_letter))

        return words_out
    
    def calculate_same_length_word_adj(self, word: str):
        """
        Given a word, "word", find all connections to same length words on the horosphere

        :param word: A word that does NOT start with the ray to infinity on the horosphere.
        :return: The list of all such same length words.
        """

        # Edge case: empty string "" 
        if len(word) == 0:
            return [word]
        
        adjacencies = []

        # Find the node in the FSM where the word is located 
        word_node = self.locate_associated_state(word)

        for last_letter in word_node[1]:

            # Remove the first instance of the last letter from the right end of the word; This is our reduced word
            reduced_word = Word(word[::-1].replace(last_letter, '', 1)[::-1], self.c_map, self.o_map)

            reduced_word_state = self.locate_associated_state(reduced_word)

            # Append 'a' or 'c' to the beginning of the reduced word
            a_aug_word_state = self.locate_associated_state(reduced_word.copy().insert(0, self.ray[0]))
            c_aug_word_state = self.locate_associated_state(reduced_word.copy().insert(0, self.ray[1]))

            # Deal with the issue of words commuting all the way forward
            connecting_letters = self.alphabet.copy().difference(set(reduced_word_state[1]))
            ray_augmented_letters = set(a_aug_word_state[1]).union(set(c_aug_word_state[1]))
            
            # The extra difference of set(reduced_word_state[1]) here is unnecessary
            connecting_letters = connecting_letters.difference(ray_augmented_letters.difference(set(reduced_word_state[1])))

            # Lengthen the reduced word by its (shortlex) legal next letters to get all same length adjacent words
            for letter in connecting_letters:
                adjacencies.append((word, reduced_word.copy().shortlex_append(letter)))

        return adjacencies

        # By construction, word cannot start with 'a' or 'c' as this would cause issues with the latter added prefix

    def calculate_different_length_adj(self, word: str):
        """
        Given a word, "word", find all connections to different length words on the horosphere.
        If the word has length n, then the different length connections we find will have length n+2.

        :param word: A word that does NOT start with the ray to infinity on the horosphere.
        :return: The list of all such different length words.
        """

        # "suffix" is the word without the ray at the beginning
        suffix = Word(word, self.c_map, self.o_map)
        suffix_state = self.locate_associated_state(suffix)

        # Append 'a' or 'c' to the beginning of the reduced word
        a_suffix_state = self.locate_associated_state(suffix.copy().insert(0, self.ray[0]))
        c_suffix_state = self.locate_associated_state(suffix.copy().insert(0, self.ray[1]))

        # Need better variable name, the contents of this set represent which letters can commute forward and cause
        # issue with the prefix of a word. This set will only ever have either 'a', 'c', or will be empty
        ac_suffix_state = set(a_suffix_state[1]).union(set(c_suffix_state[1])).difference(set(suffix_state[1]))

        # If there are no such issues, then there are no different length adjacent words; exit
        if len(ac_suffix_state) == 0:
            return []

        adjacencies = []

        # Word (suffix) has even length
        if len(suffix) % 2 == 0:
            if self.ray[0] in ac_suffix_state:
                # Lengthen word by a (shortlex) legal next letter 
                for next_letter in self.alphabet.copy().difference(set(suffix_state[1])).difference(ac_suffix_state):
                    adjacencies.append([word, suffix.copy().shortlex_append(next_letter)])
                pass
            if self.ray[1] in ac_suffix_state:
                # Shorten word by one of its possible last letters
                for last_letter in suffix_state[1]:
                    adjacencies.append([word, word[::-1].replace(last_letter, '', 1)[::-1]])

        # Word (suffix) has odd length
        else:
            if self.ray[0] in ac_suffix_state:
                # Shorten
                for last_letter in suffix_state[1]:
                    adjacencies.append([word, word[::-1].replace(last_letter, '', 1)[::-1]])
            if self.ray[1] in ac_suffix_state:
                # Lengthen
                for next_letter in self.alphabet.copy().difference(set(suffix_state[1])).difference(ac_suffix_state):
                    adjacencies.append([word, suffix.copy().shortlex_append(next_letter)])
        return adjacencies

    def calculate_word_adj(self, word):
        """
        Use "calculate_same_length_word_adj" and "calculate_different_length_adj" to find all adjacent words overall.

        :param word: A word that does NOT start with the ray to infinity on the horosphere.
        :return: All adjacent words.
        """

        adjacencies = []
        adjacencies.extend(self.calculate_same_length_word_adj(word))
        adjacencies.extend(self.calculate_different_length_adj(word))
        return adjacencies

    def calculate_horosphere_edges(self, word_list: list[str], length: int):
        """
        Add all the edges to the horosphere. 

        :param word_list: List of all ShortLex words (prefixes).
        :param length: Length of the longest ShortLex word.
        :return: All edges on the graph.
        """

        # Intialize the string "acacac..."
        ray_string = (self.ray[0] + self.ray[1]) * length

        edges = []
        edges_set = set()
        processed_edges = []

        # Extend edges with all adjacencies on the horosphere.
        for word in word_list:
            edges.extend(self.calculate_word_adj(word))

        # Append the prefix to our edges
        for edge in edges:
            prefix_edge = []
            for u in edge:
                # idx = 0
                prefix = ray_string[:len(u)]
                # for i in range(len(u)):
                #     prefix = prefix + self.ray[idx]
                #     idx = (idx + 1) % 2
                prefix_edge.append(prefix + str(u))
            processed_edges.append(prefix_edge)
            edges_set.add(tuple(prefix_edge))

        processed_edges.pop(0)
        processed_edges = [edge for edge in processed_edges if edge[0] != edge[1]]
        return processed_edges

    def horosphere_as_networkx(self, length):
        words = self.get_all_length_n_words(length)
        print(f"Words of length {length} calculated: \n\t\t {len(words)} words found")
        processed_edges = self.calculate_horosphere_edges(words, length)
        print(f"Words processing completed: \n\t\t {len(words)} words processed")

        G = networkx.Graph()
        G.add_edges_from(processed_edges)
        print(f"Length {length} Horosphere generated: \n\t\t {G}")
        return G

    @staticmethod
    def visualize_horosphere(G):
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

    def save_horosphere_as_graphml(self, horosphere_length, G=None, horosphere_type="horosphere"):
        if G is None:
            G = self.horosphere_as_networkx(horosphere_length)
        nx.write_graphml_lxml(G, f"Horosphere_Graphml/{horosphere_type}_length_{horosphere_length}.graphml")


# length = 4
# print(f"Generating Horosphere with length {2*length} nodes...")
# pentagonal_c_map = {'a': {'b', 'e'}, 'b': {'a', 'c'}, 'c': {'b', 'd'}, 'd': {'e', 'c'}, 'e': {'a', 'd'}}
# pentagonal_alphabet = {'a', 'b', 'c', 'd', 'e'}
# pentagonal_lst_alphabet = [{'c'}, {'d'}, {'b'}, {'e'}, {'a'}]
# pentagonal_o_map = {'a': 0, 'c': 1, 'b': 2, 'd': 3, 'e': 4}
# torus_o_map = {
#                 'a': 0, 'b': 2, 'c': 1, 'd': 3, 'e': 4, 'f': 5, 'g': 6,
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
#
#
# hg = HorosphereGenerator(commutation_dict=torus_c_map, order_dict=torus_o_map, ray=['a', 'c'])
# words = hg.get_all_length_n_words(length)
# edges = []
# edges_set = set()
# processed_edges = []
# hray = ['a', 'c']
#
# x = hg.calculate_different_length_adj('b')
# for n in x:
#     print(f" DIFF LEN TEST: [{str(n[0])}, {str(n[1])}]") # Word("dacb", commutation_dict=pentagonal_c_map, order_dict=pentagonal_o_map)))
#
# print(words)
# for word in words:
#     edges.extend(hg.calculate_word_adj(word))
# print(edges)
# for edge in edges:
#     uv = []
#     for u in edge:
#         idx = 0
#         prefix = ''
#         for i in range(len(u)):
#             prefix = prefix + hray[idx]
#             idx = (idx + 1) % 2
#         uv.append(prefix + str(u))
#     processed_edges.append(uv)
#     edges_set.add(tuple(uv))
#
#         # u.insert(0, hray[idx])
# processed_edges.pop(0)
#
# processed_edges = [edge for edge in processed_edges if edge[0] != edge[1]]
# # print(edges_set)
# print(len(edges_set))
# G = networkx.Graph()
# G.add_edges_from(processed_edges)
# # nx.draw_spring(G)
# # plt.show()
#
# # pos = nx.spring_layout(G, pos={"": (0, 0)}, dim=2, iterations=500, fixed=[""])
# #pos = nx.spring_layout(G, dim=2, iterations=100, weight=5)
# colors = []
# for node in G:
#     if len(node) == 12:
#         colors.append(matplotlib.colors.to_rgba("#8E44AD", 1))
#     elif len(node) == 10:
#         colors.append(matplotlib.colors.to_rgba("#F1C40F", 1))
#     elif len(node) == 8:
#         colors.append(matplotlib.colors.to_rgba("#FF5733", 1))
#     elif len(node) == 6:
#         colors.append(matplotlib.colors.to_rgba("#ff96d5", 1))
#     elif len(node) == 4:
#         colors.append(matplotlib.colors.to_rgba("#96b9ff", 1))
#     elif len(node) == 2:
#         colors.append(matplotlib.colors.to_rgba("#e4ff85", 1))
#     elif len(node) == 0:
#         colors.append(matplotlib.colors.to_rgba("#b0b0b0", 1))
# options = {
#     "node_color": colors,
#     # "edge_color": edge_colors,
#     # "width": 4,
#     "font_size": 20,
#     # "edge_cmap": plt.cm.Blues,
#     "with_labels": True,
#     "node_size": 400,
#     "font_color": "black"
# }
# nx.write_graphml_lxml(G, f"horosphere_length_{length}.graphml")
# #nx.draw(G, **options)
# #plt.show()
#
# #print(processed_edges)

# def adj_words(self, word, G):
#     if word == '':
#         return

#     word_prefix = word[:len(word) // 2]
#     word_suffix = word[len(word) // 2:]
#     word_node = self.locate_associated_state(word_suffix)

#     # Finds connections between same length words on the horosphere
#     for last_letter in word_node[1]:
#         # Remove the first instance of the last letter from the right end of the word; This is our reduced word
#         adj_word = word_suffix[::-1].replace(last_letter, '', 1)[::-1]

#         for add in self.locate_associated_state(adj_word)[0]:
#             # add the possible legal remaining letters, so we are still on the horosphere
#             # if the length of the test word is 2, then 'ac' and 'aa' will get registered as on the horosphere
#             if len(word) == 2:
#                 # so we do not consider possible added letters that would be on the ray or cancel
#                 if add not in {'a', 'c'}:
#                     # print(word, '--', word[:len(word) // 2] + adj_word + add)
#                     G.add_node(word[:len(word) // 2] + adj_word + add)
#                     if word[:len(word) // 2] + adj_word + add != word:
#                         G.add_edge(word, word[:len(word) // 2] + adj_word + add)
#             else:
#                 G.add_node(word[:len(word) // 2] + adj_word + add)
#                 if word[:len(word) // 2] + adj_word + add != word:
#                     # print(word, '--')
#                     G.add_edge(word, word[:len(word) // 2] + adj_word + add)