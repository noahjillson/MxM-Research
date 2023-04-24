from vertices import VertexName
from FSM_Generator import FSMGenerator
from Horosphere_Generator import HorosphereGenerator
from Defining_Graphs import DefiningGraphs as DG


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
    FSM_Gen = FSMGenerator(DG.torus_c_map, DG.pentagonal_o_map)

