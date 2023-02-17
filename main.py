from vertices import VertexName
from fsm import FSMGenerator
from horospheres import HorosphereGenerator


def test_horosphere():
    indentation = "     "
    c_map = {'a': ['b', 'e'], 'b': ['a', 'c'], 'c': ['b', 'd'], 'd': ['c', 'e'], 'e': ['d', 'a']}
    o_map = {'a': 0, 'c': 1, 'b': 2, 'd': 3, 'e': 4}
    depth = 4

    # Print global values used by all functions
    print("Globals:\n" + indentation + "c_map: " + str(c_map) + "\n" + indentation + "o_map: " + str(o_map))

    # Print function name, function specific args, and function return value
    print("\nTesting \'generate_horosphere\' function:\n" + indentation + "Args: depth=" + str(depth))
    partial_horosphere = HorosphereGenerator.generate_horosphere(depth=depth, c_map=c_map, o_map=o_map)
    print(indentation + "Returns: " + str(partial_horosphere))

    print("\nTesting \'process_horosphere\' function:\n" + indentation + "Args: horosphere=generate_horosphere(" + str(depth) + ")")
    processed_horosphere = HorosphereGenerator.process_horosphere(partial_horosphere)
    print(indentation + "Returns: " + str(processed_horosphere))

    print("\nTesting \'last_operations\' function:\n" + indentation + "Args: horosphere=generate_horosphere()")
    name_ops_pair = []
    for name in processed_horosphere:
        name_ops_pair += [VertexName(name).last_operations(), name]
    print(indentation + "Returns: " + str(name_ops_pair))

    print("\nTesting \'evaluate_horosphere_edges\' function:\n" + indentation + "Args: horosphere=process_horosphere( " + "generate_horosphere(" + str(depth) + ")" + " )")
    horosphere_graph = HorosphereGenerator.evaluate_horosphere_edges(processed_horosphere)
    print(indentation + "Returns: " + str(horosphere_graph))

    c_map_set = {'a': {'b', 'e'}, 'b': {'a', 'c'}, 'c': {'b', 'd'}, 'd': {'c', 'e'}, 'e': {'d', 'a'}}
    def last_letters_recursion(w):
        if len(w) == 0:
            return 'empty word inputted'
        if len(w) == 1:
            return set(w)
        return last_letters_recursion(w[:-1])      \
                    .intersection(c_map_set[w[-1]])     \
                    .union(set(w[-1]))

    for name in processed_horosphere:
        print(name, last_letters_recursion(name))

    # print("\nTesting \'evaluate_horosphere_edges\' function:\n" + indentation + "Args: horosphere=process_horosphere( " + "generate_horosphere(" + str(depth) + ")" + " )")
    # horosphere_graph = HorosphereGenerator.evaluate_horosphere_edges(processed_horosphere)
    # print(indentation + "Returns: " + str(horosphere_graph))

    # print("\nTesting \'visualize_horosphere\' function:\n" + indentation + "Verify results in Matplotlib window")
    # HorosphereGenerator.visualize_horosphere(processed_horosphere)



if __name__ == '__main__':
    # v = VertexName("dcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadcadc")
    v = VertexName("acabeb")  # ADC??
    print("LAST OPERATIONS: " + str(v.last_operations()))
    print(VertexName.last_op("ab", c_map = {'a': ['b', 'e'], 'b': ['a', 'c'], 'c': ['b', 'd'], 'd': ['c', 'e'], 'e': ['d', 'a']}))
    # v = VertexName("eca") """'acabda', {'d', 'a', 'e'}, 'acadbe'"""
    # print(v.name)
    # print(v.sort_name("c"))
    # print(v.is_valid_append("c"))
    # print(v.generate_truth_table())
    # print(FSMGenerator.generate_fsm_nodes())

    # ACTUALLY IMPORTANT STUFF
    # d = FSMGenerator.generate_fsm_nodes(o_map={'a': 0, 'c': 1, 'b': 2, 'd': 3, 'e': 4})
    # for key in d:
    #     print(key + "," + str(d[key]))
    #
    # jt = FSMGenerator.generate_jump_table(o_map={'a': 0, 'c': 1, 'b': 2, 'd': 3, 'e': 4})
    # print(jt)
    #
    FSMGenerator.visualize_from_jump_table(o_map={'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4},
                                            c_map={'a': ['b', 'd'], 'b': ['a', 'c'], 'c': ['b', 'd'], 'd': ['a', 'c'], 'e': []})

    test_horosphere()

    horo = HorosphereGenerator.generate_horosphere(4)
    proc_horo = HorosphereGenerator.process_horosphere(horo)
    # print(proc_horo)
    # print(VertexName.remove_dupes('aa'))
    # print(VertexName.append('ab', 'ad'))
    HorosphereGenerator.visualize_horosphere(proc_horo)
    # print("hello world")

    FSMGenerator.visualize_from_jump_table(o_map={'b': 0, 'a': 1, 'c': 2, 'd': 3, 'e': 4})

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
