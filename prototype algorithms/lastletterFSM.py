import lastletter


def fsm():
    E = set()
    V = set()

    letters = {'a', 'b', 'c', 'd', 'e'}
    for l in letters:
        adjacent_letters = c_map[l]
        intermediary_letters = []
        for al in adjacent_letters:
            intermediary_letters.extend(c_map[al].copy().difference(set(l)))
            print(l + " -" + al + "-> " + al+l)
        for il in intermediary_letters:
            print(l + " -" + il + "-> " + il+l)
            for x in c_map[il].copy().intersection(c_map[l]):
                print(l + il + " -" + x + "-> " + x+l)


"""
Algorithm for Generating a FSM that dictates which letters can be the last letters of a word by reading the letters
of any given input word in reverse order.
"""
def g_fsm_n(c_map) :
    E = set()  # Edge Set
    V = set()  # Vertex Set

    Q = [""]

    while len(Q) > 0:
        l = Q.pop()
        V.add(l)
        for adjacent in c_map[l]:
            Q.append(adjacent)




"""
Algorithm to generate a FSM that reads in the letters of a word and outputs the possible last letters
"""


def generate_fsm_n(c_map):
    class Node:
        def __init__(self, name, pll):
            self.name = name
            self.pll = pll
            self.edges = []

        def add_edge(self, edge):
            self.edges.append(edge)

    class Edge:
        def __init__(self, label, s, d):
            self.label = label
            self.s = s
            self.d = d

    fsm_n = []
    # Initialize a Queue with each operation in the defining graph
    queue = [Node("", "")]
    while len(queue) > 0:
        tmp = queue.pop()
        edges = None

        # If we are working with the start node (Special Case)
        if len(tmp.name) == 0:
            edges = list(c_map[tmp.name])
            for e in edges:
                tmp.add_edge(Edge(e, "", e))
                queue.append((Node(e, e)))

        # If tmp is not the starting vertex
        else:
            # The last letter of the tmp's name is the label of the connecting edge to tmp
            # We get all edges that commute with the previous letter in hopes that one can be a last letter
            # edges = list(c_map[tmp.name[-1]])
            print("TEST: " + tmp.name[-1])
            edges = list(c_map[''])
            for e in edges:
                if e == tmp.name[-1] or e == tmp.name[0]:
                    continue
                # If the first edge in the path to tmp commutes with a neighbor of
                if len(c_map[tmp.name[0]].intersection(c_map[e])) > 0:
                    tmp.add_edge(Edge(e, tmp.name, tmp.name + e))
                    pll = ""
                    if e in c_map[tmp.name[0]]:
                        pll = tmp.name[0] + e
                    else:
                        pll = tmp.name[0]
                    if len(pll) < 2:
                        queue.append((Node(tmp.name + e, pll)))
                    print(tmp.name + e)
        print(len(queue))
        fsm_n.append(tmp)

    return fsm_n


c_map = {'a': {'b', 'e'}, 'b': {'a', 'c'}, 'c': {'b', 'd'}, 'd': {'e', 'c'}, 'e': {'a', 'd'}, '': {'a', 'b', 'c', 'd', 'e'}}
fsm()
# print(generate_fsm_n(c_map))
# fsm = generate_fsm_n(c_map)
# Q = fsm
# while len(Q) > 0:
#     tmp = Q.pop()
#     for edge in tmp.edges:
#         print("|" + str(edge.s) + "| ---" + str(edge.label) + "--> |" + str(edge.d) + "|")
