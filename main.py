from vertices import VertexName
from fsm import FSMGenerator


#def generate_fsm_nodes() -> list:
#    pass


if __name__ == '__main__':
    # v = VertexName("dcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadc")
    # v = VertexName("acd") # ADC??
    # v = VertexName("eca")
    # print(v.name)
    # print(v.sort_name("c"))
    # print(v.is_valid_append("c"))
    # print(v.generate_truth_table())
    # print(FSMGenerator.generate_fsm_nodes())
    d = FSMGenerator.generate_fsm_nodes(o_map={'a': 0, 'c': 1, 'b': 2, 'd': 3, 'e': 4})
    for key in d:
        print(key + "," + str(d[key]))

    jt = FSMGenerator.generate_jump_table(o_map={'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4})
    print(jt)

    FSMGenerator.visualize_from_jump_table(o_map={'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4})

    #
    # d = FSMGenerator.generate_fsm_nodes(o_map={'a': 0, 'b': 1, 'c': 2, 'd': 3},
    #                                     c_map={'a': ['b', 'd'], 'b': ['a', 'c'], 'c': ['b', 'd'], 'd': ['a', 'c']})
    # for key in d:
    #     print(key + "," + str(d[key]))

    # d = FSMGenerator.generate_fsm_nodes(o_map={'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6,
    #                                            'A': 7, 'B': 8, 'C': 9, 'D': 10, 'E': 11, 'F': 12, 'G': 13,
    #                                            '1': 14, '2': 15, '3': 16, '4': 17, '5': 18, '6': 19, '7': 20},
    #                                     c_map={'a': ['g', 'b', 'D', 'E', '4', '5'], 'b': ['a', 'c', 'A', 'C', '1', '3'],
    #                                            'c': ['b', 'd', 'B', 'D', '2', '4'], 'd': ['c', 'e', 'C', 'E', '3', '5'],
    #                                            'e': ['d', 'f', 'D', 'F', '4', '6'], 'f': ['e', 'g', 'E', 'G', '5', '7'],
    #                                            'g': ['f', 'a', 'F', 'A', '6', '1'],
    #                                            'A': ['G', 'B', 'd', 'e', '4', '5'], 'B': ['A', 'C', 'a', 'c', '1', '3'],
    #                                            'C': ['B', 'D', 'b', 'd', '2', '4'], 'D': ['C', 'E', 'c', 'e', '3', '5'],
    #                                            'E': ['D', 'F', 'd', 'f', '4', '6'], 'F': ['E', 'G', 'e', 'g', '5', '7'],
    #                                            'G': ['F', 'A', 'f', 'a', '6', '1'],
    #                                            '1': ['7', '2', 'd', 'e', 'D', 'E'], '2': ['1', '3', 'e', 'f', 'E', 'F'],
    #                                            '3': ['2', '4', 'f', 'g', 'F', 'G'], '4': ['3', '5', 'g', 'a', 'G', 'A'],
    #                                            '5': ['4', '6', 'a', 'b', 'A', 'B'], '6': ['5', '7', 'b', 'c', 'B', 'C'],
    #                                            '7': ['6', '1', 'c', 'd', 'C', 'D']})
    # for key in d:
    #     print(key + "," + str(d[key]))
