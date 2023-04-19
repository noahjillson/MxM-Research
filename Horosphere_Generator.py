import networkx

from word import Word, WordGenerator
from FSM_Generator import FSMGenerator
import networkx as nx
import matplotlib.pyplot as plt


class HorosphereGenerator:
    def __init__(self, commutation_dict: dict[str: list], order_dict: dict[str: int], ray: list[str]):
        """
        Initialize a Horosphere Generator Object. Using the defining graph of a right-angled coxeter
        group, horosphere's can be created can be created.

        :param commutation_dict: A dictionary representation of a defining graph. A letter (key) is associated with a list of letters (value) in the dictionary such that all letters in the list commute with the key
        :param order_dict: A dictionary representation of a total ordering on the letter in the defining graph. A letter (key) is associated with an index (value) that represents that letters relative position in the ordering.
        """
        self.c_map = commutation_dict
        self.o_map = order_dict
        self.alphabet = set().union(letter for letter in self.o_map)
        self.ray = ray
        fsm_gen = FSMGenerator(self.c_map, self.o_map)
        self.fiber_product_fsm = fsm_gen.generate_fiber_product_fsm_as_dict()

    def locate_associated_state(self, word):
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

    def get_all_length_n_words(self, n):
        """
        Finds all words that have a suffix up to length n with a BFS

        :param n: The depth with which the BFS will be conducted. The algorithm will compute all short-lex words of this length.
        :return: All possible short-lex words of length n.
        """
        n += 1
        fix_words = 'ac' * n
        origin = (''.join(sorted(self.alphabet)), '')

        # All elements of the frontier are of the form (node, current depth, word), we want the words
        frontier = [(origin, 0, '')]
        words_out = []

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
                frontier.append((self.fiber_product_fsm[node][next_letter], depth+1, word + next_letter))

        return words_out

    def __calculate_different_length_adj(self, word):
        if len(word) % 2 == 0:
            if 'a' in word.copy().insert(0, 'a').last_letters().difference(word.last_letters()):
                pass
        return []

    def __calculate_same_length_adj(self):
        pass

    def calculate_word_adj(self, word: str):
        """

        :param word: A word that does NOT start with the ray to infinity on the horosphere
        :param G:
        :return:
        """
        if len(word) == 0:
            return [word]
        adjacencies = []
        word_node = self.locate_associated_state(word)

        # Finds connections between same length words on the horosphere
        for last_letter in word_node[1]:
            print(word_node[1])
            print(f"Last Letter: {last_letter}")
            # Remove the first instance of the last letter from the right end of the word; This is our reduced word
            reduced_word = Word(word[::-1].replace(last_letter, '', 1)[::-1], self.c_map, self.o_map)
            # print(f"Word: {word}, Reduced Word: {reduced_word}")
            reduced_word_state = self.locate_associated_state(reduced_word)
            a_aug_word_state = self.locate_associated_state(reduced_word.copy().insert(0, 'a'))
            c_aug_word_state = self.locate_associated_state(reduced_word.copy().insert(0, 'c'))

            # I believe this is where the issue is, sometimes an a can commute all the way forward and this is meand to stop that
            connecting_letters = self.alphabet.copy().difference(set(reduced_word_state[1]))
            ray_augmented_letters = set(a_aug_word_state[1]).union(set(c_aug_word_state[1]))
            # The extra difference of set(reduced_word_state[1]) here is unnecessary see proof on blackboard
            connecting_letters = connecting_letters.difference(ray_augmented_letters.difference(set(reduced_word_state[1])))

            for letter in connecting_letters:
                print(f"Word: {word}, Reduced Word: {reduced_word.copy().shortlex_append(letter)}, Letter: {letter}")
                adjacencies.append((word, reduced_word.copy().shortlex_append(letter)))

        return adjacencies

        # By construction, word cannot start with 'a' or 'c' as this would cause issues with the latter added prefix
        # prefixed_words = [word.copy().insert(0, 'a'), word.copy().insert(0, 'c')]
        # last_letters = word.last_letters()
        # Word(word.word_as_list.insert(0, 'a'))

    def adj_words(self, word, G):
        if word == '':
            return

        word_prefix = word[:len(word) // 2]
        word_suffix = word[len(word) // 2:]
        word_node = self.locate_associated_state(word_suffix)

        # Finds connections between same length words on the horosphere
        for last_letter in word_node[1]:
            # Remove the first instance of the last letter from the right end of the word; This is our reduced word
            adj_word = word_suffix[::-1].replace(last_letter, '', 1)[::-1]

            for add in self.locate_associated_state(adj_word)[0]:
                # add the possible legal remaining letters, so we are still on the horosphere
                # if the length of the test word is 2, then 'ac' and 'aa' will get registered as on the horosphere
                if len(word) == 2:
                    # so we do not consider possible added letters that would be on the ray or cancel
                    if add not in {'a', 'c'}:
                        # print(word, '--', word[:len(word) // 2] + adj_word + add)
                        G.add_node(word[:len(word) // 2] + adj_word + add)
                        if word[:len(word) // 2] + adj_word + add != word:
                            G.add_edge(word, word[:len(word) // 2] + adj_word + add)
                else:
                    G.add_node(word[:len(word) // 2] + adj_word + add)
                    if word[:len(word) // 2] + adj_word + add != word:
                        # print(word, '--')
                        G.add_edge(word, word[:len(word) // 2] + adj_word + add)

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

length = 4
print(f"Generating Horosphere with length {2*length} nodes...")
pentagonal_c_map = {'a': {'b', 'e'}, 'b': {'a', 'c'}, 'c': {'b', 'd'}, 'd': {'e', 'c'}, 'e': {'a', 'd'}}
pentagonal_alphabet = {'a', 'b', 'c', 'd', 'e'}
pentagonal_lst_alphabet = [{'c'}, {'d'}, {'b'}, {'e'}, {'a'}]
pentagonal_o_map = {'a': 0, 'c': 1, 'b': 2, 'd': 3, 'e': 4}

hg = HorosphereGenerator(commutation_dict=pentagonal_c_map, order_dict=pentagonal_o_map, ray=['a', 'c'])
words = hg.get_all_length_n_words(length)
edges = []
processed_edges = []
hray = ['a', 'c']

# print(hg.calculate_word_adj("dabe"))# Word("dacb", commutation_dict=pentagonal_c_map, order_dict=pentagonal_o_map)))

print(words)
for word in words:
    edges.extend(hg.calculate_word_adj(word))
print(edges)
for edge in edges:
    uv = []
    for u in edge:
        idx = 0
        prefix = ''
        for i in range(len(u)):
            prefix = prefix + hray[idx]
            idx = (idx + 1) % 2
        uv.append(prefix + str(u))
    processed_edges.append(uv)

        #u.insert(0, hray[idx])
processed_edges.pop(0)

processed_edges = [edge for edge in processed_edges if edge[0] != edge[1]]

G = networkx.Graph()
G.add_edges_from(processed_edges)
# nx.draw_spring(G)
# plt.show()

pos = nx.spring_layout(G, dim=2)
options = {
    # "node_color": node_colors,
    # "edge_color": edge_colors,
    # "width": 4,
    "font_size": 8,
    # "edge_cmap": plt.cm.Blues,
    "with_labels": True,
    "node_size": 200,
    "font_color": "black"
}
nx.draw(G, pos, **options)
plt.show()

print(processed_edges)
