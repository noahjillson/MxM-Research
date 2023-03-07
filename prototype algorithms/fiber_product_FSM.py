import last_letter_FSM
import forbidden_letters_FSM
import fiber_product

# Default values
# pentagonal_c_map = {'a': {'b', 'e'}, 'b': {'a', 'c'}, 'c': {'b', 'd'}, 'd': {'e', 'c'}, 'e': {'a', 'd'}}
# pentagonal_alphabet = {'a', 'b', 'c', 'd', 'e'}
# pentagonal_lst_alphabet = [{'c'}, {'d'}, {'b'}, {'e'}, {'a'}]

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

FSM_M = forbidden_letters_FSM.generate_fsm_forbidden_letters()
# print("Vertices: " + str(FSM[0]))
# print("Edges: " + str(FSM[1]))
# print(str(len(FSM[0])) + " Vertices")
# print(str(len(FSM[1])) + " Edges")

hashable_edges_M = []
for edge in FSM_M[1]:
    hashable_edges_M.append(forbidden_letters_FSM.format_directed_edge(edge))

# add length 1 edges
for node in FSM_M[0]:
    if len(node) == 1:
        hashable_edges_M.append(('', list(node)[0], list(node)[0]))

labeled_edges_M = {
    (ele[0], ele[1]): ele[2] for ele in hashable_edges_M
}

FSM_N = last_letter_FSM.generate_fsm_last_letter()
# print("Vertices: " + str(FSM[0]))
# print("Edges: " + str(FSM[1]))
# print(str(len(FSM[0])) + " Vertices")
# print(str(len(FSM[1])) + " Edges")

hashable_edges_N = []
for edge in FSM_N[1]:
    hashable_edges_N.append(last_letter_FSM.generate_fsm_last_letter(edge))

# add length 1 edges
for node in FSM_N[0]:
    if len(node) == 1:
        hashable_edges_N.append(('', list(node)[0], list(node)[0]))

labeled_edges_N = {
    (ele[0], ele[1]): ele[2] for ele in hashable_edges_N
}

print(labeled_edges_M, labeled_edges_N)