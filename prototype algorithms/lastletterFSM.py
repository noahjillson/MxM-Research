def gen_fsm() -> list:
    """
    Generate the finite state machine of all possible last letters. Edges represent writing a letter while vertices
    represent the set of possible last letters given the edges follower / letters written.

    :return: list of lists; The first entry is the list of vertices; The second is the list of edges.
    """
    vertices = []
    edges = []
    frontier = []

    frontier.extend(alphabet)
    while len(frontier) > 0:
        v = frontier.pop(0)

        # We have already considered v and all its outgoing edges, we can skip its consideration
        if v in vertices:
            continue
        vertices.append(v)

        # Record outgoing edges from v, this is guaranteed to be unique by above if-statement
        # Add the destination vertex, u, to our frontier to ensure all vertices are reached
        for e in alphabet.copy().difference(v):
            u = set(e).union(set(v).intersection(c_map[e]))
            frontier.append(u)
            edges.append([v, u])

    print("Vertices: " + str(vertices))
    print("Edges: " + str(edges))
    return [vertices, edges]


def fsm():
    letters = alphabet
    for l in letters:
        adjacent_letters = c_map[l]
        intermediary_letters = []
        for al in adjacent_letters:
            intermediary_letters.extend(c_map[al].copy().difference(set(l)))
            print(l + " -" + al + "-> " + al + l)
        for il in intermediary_letters:
            print(l + " -" + il + "-> " + il + l)
            for x in c_map[il].copy().intersection(c_map[l]):
                print(l + il + " -" + x + "-> " + x + l)


pentagonal_c_map = {'a': {'b', 'e'}, 'b': {'a', 'c'}, 'c': {'b', 'd'}, 'd': {'e', 'c'}, 'e': {'a', 'd'}}
pentagonal_alphabet = {'a', 'b', 'c', 'd', 'e'}
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

c_map = torus_c_map
alphabet = torus_alphabet
# fsm()
gen_fsm()
