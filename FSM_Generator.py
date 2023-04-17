from word import Word, WordGenerator


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
        print(self.alphabet.copy())
        self.language = WordGenerator(self.c_map, self.o_map)

    def generate_short_lex_vertices_edges(self):
        """
        Generate the finite state machine of all possible last letters. Edges represent writing a letter while vertices
        represent the set of possible last letters given the edges follower / letters written.

        :return: list of lists; The first entry is the list of vertices; The second is the list of edges.
        """
        origin = self.alphabet
        vertices = [origin]
        edges = []
        frontier = []

        for letter in self.alphabet:
            print(f"letter {letter}")
            destination = Word(letter, self.c_map, self.o_map).legal_next_letters()
            frontier.append(destination)
            edges.append((origin, destination, letter))

        while len(frontier) > 0:
            source = frontier.pop(0)

            # We have already considered source and all its outgoing edges, we can skip its consideration
            if source in vertices:
                continue
            vertices.append(source)

            # Record outgoing edges from v, this is guaranteed to be unique by above if-statement
            # Add the destination vertex, u, to our frontier to ensure all vertices are reached
            # alphabet.copy().difference(v)
            for edge in source:
                destination = Word(edge, self.c_map, self.o_map).forbidden_letters()\
                    .union(self.alphabet.copy().difference(source).intersection(set(self.c_map[edge])))
                destination = self.alphabet.copy().difference(destination)
                frontier.append(destination)
                edges.append((source, destination, edge))

        return [vertices, edges]

    def generate_short_lex_fsm_as_networkx(self):
        pass

    def generate_last_letter_fsm_as_networkx(self):
        pass

    def generate_fiber_product_fsm_as_networkx(self):
        pass

    def generate_short_lex_fsm_as_adj(self):
        pass

    def generate_last_letter_fsm_as_adj(self):
        pass

    def generate_fiber_product_fsm_as_adj(self):
        pass

    def visualize_fsm(self):
        pass


pentagonal_c_map = {'a': {'b', 'e'}, 'b': {'a', 'c'}, 'c': {'b', 'd'}, 'd': {'e', 'c'}, 'e': {'a', 'd'}}
pentagonal_alphabet = {'a', 'b', 'c', 'd', 'e'}
pentagonal_lst_alphabet = [{'c'}, {'d'}, {'b'}, {'e'}, {'a'}]
pentagonal_o_map = {'a': 0, 'c': 1, 'b': 2, 'd': 3, 'e': 4}
a = FSMGenerator(commutation_dict=pentagonal_c_map, order_dict=pentagonal_o_map).generate_short_lex_vertices_edges()
print(a[0])
print(a[1])
