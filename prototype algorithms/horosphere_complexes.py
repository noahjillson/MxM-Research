import fiber_product_FSM
import legal_next_letters_FSM
import last_letter_FSM

# Default values
pentagonal_c_map = {'a': {'b', 'e'}, 'b': {'a', 'c'}, 'c': {'b', 'd'}, 'd': {'e', 'c'}, 'e': {'a', 'd'}}
pentagonal_alphabet = {'a', 'b', 'c', 'd', 'e'}
pentagonal_origin = 'abcde'
pentagonal_o_map = {'a': 0, 'c': 1, 'b': 2, 'd': 3, 'e': 4}
pentagonal_lst_alphabet = [{'c'}, {'d'}, {'b'}, {'e'}, {'a'}]

FSM_M = legal_next_letters_FSM.generate_fsm_forbidden_letters(alphabet=pentagonal_alphabet, c_map=pentagonal_c_map,
                                                             o_map=pentagonal_o_map)

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

# The real algorithm below
G, final_edge_labels = fiber_product_FSM.fiber_product(labeled_edges_M, labeled_edges_N)
adj_list = G.adj

# print(final_edge_labels)
for edge, label in final_edge_labels.items():
    adj_list[edge[0]][edge[1]]['label'] = label

#print(adj_list)


# Termination is dependent on word being constructible via traversal through the FSM
# O(nD) where n is the length of the word and D is the number of letters in our alphabet/defining graph
def locate_associated_state(word, adj_dict):
    current_state = (pentagonal_origin, '')
    constructed_word = ''

    # Lookup in this sense is linear with respect to length of our word
    for idx in range(len(word)):
        # The number of adjacencies of a node is bounded above by the number of letters in out alphabet/defining graph
        # Thus we result in a pseudo-polynomial algorithm for canonical word lookup in our FSM
        for (key, value) in adj_dict[current_state].items():
            if value['label'] == word[idx]:
                current_state = key
                break

    return current_state


# Could be optimized right now we run in O(nKD)
# where n is the length of our current word, K is the size of the largest complete subgraph in our defining graph, and
# D is the size of our alphabet/defining graph
def reduce_word(current, reduction_letter, adj_dict):
    reduced_name = ""

    if current['name'][-1] == reduction_letter:
        reduced_name = current['name'][:-1]
        # print("REDUCED NAME TEST1: " + str(reduced_name))
    else:
        for idx in reversed(range(len(current['name']))):
            letter = current['name'][idx]
            # print("LETTER: " + str(letter))
            if letter == reduction_letter:
                reduced_name = current['name'][:idx] + current['name'][idx + 1:]
                # print("REDUCED NAME TEST2: " + str(reduced_name))
                break
    print("reduced name: " + str(reduced_name) + " original name: " + str(current['name']) + " reduction letter: " + str(reduction_letter))
    return {'name': reduced_name, 'id': locate_associated_state(reduced_name, adj_dict)}


# Given a current node in the FSM, we compute what other nodes will connect to this node on the horosphere
def make_horosphere_connections(current, adj_dict):
    last_letters = current['id'][1]
    reduced_words = []
    horosphere_connections = []
    frontier_extension = []

    for letter in last_letters:
        reduced_words.append(reduce_word(current, letter, adj_dict))
    print(reduced_words)
    # print(reduced_words)
    # !we can obtain the outgoing edges from the forbidden letters of our state!
    # However, for simplicity of code we will iterate through all outgoing edges (slightly more expensive but linear)
    # print(current['id'])
    # print(adj_dict[current['id']])
    for reduced_word in reduced_words:
        for (key, properties) in adj_dict[reduced_word['id']].items():
            horosphere_connections.append((current['name'], reduced_word['name'] + properties['label']))
            frontier_extension.append({'name': reduced_word['name'] + properties['label'], 'id': key})

    return {'horosphere_connections': horosphere_connections, 'frontier_extension': frontier_extension}


# Iterating through fiber product FSM
def connect_same_length_adj_nodes(depth, G, adj_dict):
    origin = ('', '')
    # List of (string, tuple) dicts representing current node's name represented as a string and as stored in G
    frontier = [{'name': '', 'id': origin}]
    edges = []

    current = {'name': '', 'id': origin}
    while len(current['name']) <= depth:
        current = frontier.pop(0)
        connections = make_horosphere_connections(current, adj_dict)
        edges.extend(connections['horosphere_connections'])
        frontier.extend(connections['frontier_extension'])

        adjacencies = adj_dict[current['id']]
        # do_stuff() i.e. the important connecting stuff
        # for (key, value) in adjacencies.items():
        #     frontier.append({'name': current['name'] + value['label'], 'id': key})

    return edges


#edges = connect_same_length_adj_nodes(2, G, adj_list)
#print(edges)
print(make_horosphere_connections({'name': 'dab', 'id': ('ab', 'ab')}, adj_list))
print(adj_list[locate_associated_state("b", adj_list)])
print("––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––")
#print(connect_same_length_adj_nodes(3, G, adj_list))
test_word = 'ec'
print(str(test_word) + ": " + str(locate_associated_state(test_word, adj_list)))
print(adj_list[('abcde', '')])
print(make_horosphere_connections({'name': 'ec', 'id': ('abe', 'c')}, adj_list))
print("––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––")
w = "dab"
current_node = ('abcde', '')
current_node_traversal = [current_node]

#print("TEST")
# traversal
for letter in w:
    for out_node, properties in adj_list[current_node].items():
        if properties['label'] == letter:
            current_node = out_node
            current_node_traversal.append(out_node)
            break

for last in current_node[0]:
    idx = len(w) - 1
    w_prime = w
    while idx >= 0:
        if w[idx] == last:
            w_prime = w_prime.replace(w_prime[idx], '', 1)
            break
        idx -= 1
    cnode = ('abcde', '')
    # traversal
    for letter in w_prime:
        for out_node, properties in adj_list[cnode].items():
            if properties['label'] == letter:
                cnode = out_node
                break
    for properties in adj_list[cnode].values():
        # print(w_prime + properties['label'])
        pass

# print("In Edges: ")
# print(G.in_edges(('de', 'd')))
# print(current_node)
# print(current_node_traversal)
