"""
Class that models the name of a dual graph vertex
"""


class VertexName:
    """
    :var start_name - The sorted starting name of this vertex. The value passed must be sorted relative to the passed
                      o_map, or the nice properties of sorted vertex names are lost. An unsorted vertex name will lead
                      to undefined behavior

    :var c_map - Dictionary representing the group's coxter diagram. Each group operation is a key and a list of
                 commutable group operations are mapped as the value.

    :var o_map - Dictionary representing the ordering imposed on the group operations. Each operation is a key and its
                 position in the ordering represented as an integer is mapped as the value
    """

    def __init__(self, start_name="", c_map=None, o_map=None):
        if c_map is None:
            c_map = {'a': ['b', 'e'], 'b': ['a', 'c'], 'c': ['b', 'd'], 'd': ['c', 'e'], 'e': ['d', 'a']}
        if o_map is None:
            o_map = {'a': 0, 'c': 1, 'b': 2, 'd': 3, 'e': 4}
        self.name = start_name
        self.c_map = c_map
        self.o_map = o_map

    """
    :return - str value name of VertexName
    """

    def __str__(self):
        return self.name

    """
    :return - str value name of VertexName
    """

    def __repr__(self):
        return self.__str__()

    """
    :return - True if the exact string value of self.name and VertexName.name are equal; False otherwise
    """

    def __eq__(self, other):
        if other is VertexName:
            return self.name == other.name
        return False

    """
    Appends a single operation to the end of the VertexName's name and sorts the concatenated value according to the
    VertexName's o_map and c_map. Method correctness depends on the assumption that VertexName.name is already in 
    sorted order.
    
    :var char - Group operation to append to the name
    :return - VertexName.name with passed group operation inserted from the right in best sorted with respect to the
              coxter diagram and imposed ordering (c_map and o_map)
    """

    def sort_name(self, char: str) -> str:
        if len(char) > 1 or len(char) == 0:
            print("Cannot sort multiple operations at one time")
            return self.name
        if len(self.name) == 0:
            return char

        min_str = self.name + char
        idx = len(self.name) - 1

        while idx >= 0 and char in self.c_map[self.name[idx]]:
            if self.o_map[char] < self.o_map[self.name[idx]]:
                min_str = self.name[:idx] + char + self.name[idx:]
            idx -= 1

        # Does not remove double letters correctly?
        # It seems like we are removing double letters even if we should not have commuted in the first place
        # consider 'adc' and 'd', then clearly 'adcd' is an accepted string however after the loop we will have
        # idx = 1 and 'd' == 'adc'.charAt(1) but we never should have commuted in the first place
        # print("Char:" + char + ",Name[idx]:" + self.name[idx] + ",idx:" + str(idx))
        # To fix this we can compare char == self.name[idx] and idx == min_char_idx MAYBE
        # UPDATE: I believe this is not an issue because of our assumption that self.name is already ordered.
        # In our scenario of {a,b,c,d,e}, we won't have any cases where a commutation happens like this
        # leading to a cancellation as we would have not allowed the original string in the first place if letter c_1
        # c_2 commute and c_1 > c_2
        if idx >= 0 and char == self.name[idx]:
            if idx + 1 > len(self.name) - 1:
                return self.name[:idx]
            return self.name[:idx] + self.name[idx + 1]

        return min_str

    """
    Determines if a given group operation can be appended to the name without breaking sorted order.

    :var char - Group operation to append to the name
    :return - True if the group operation will be inserted into the name at the right end; False if the group operation
              requires commutations or cancellations to maintain sorted order
    """

    def is_valid_append(self, char: str) -> bool:
        if len(char) > 1 or len(char) == 0:
            print("Cannot append multiple operations at one time")
            return False

        return self.sort_name(char) == self.name + char

    """
    Generates a truth table for the current name where each row is the potential appendment of every possible group
    operation. If appending an operation maintains sorted order, we consider this logically true. If the last index of
    the name is not the sorted position of the added group operation in the name, we consider this logically false.

    :return Dictionary representation of the truth table where each key is a group operation. The mapped value is
            True if simple appending of the key to the vertex name maintains sorted order; False otherwise.
    """

    def generate_truth_table(self) -> dict:
        truth_table = {}
        for char in self.o_map:
            truth_table[char] = self.is_valid_append(char)
        return truth_table

    """
    Determines path between two vertices. By reversing one name and prepending it to the other, we can obtain the path
    within the graph between the two nodes (which is the sequence of operating required to take one vertex to the other)
    
    :var vertex_name - The name of the first vertex
    :var op_string - The name of the second vertex. For optimal performance, this vertex should be the shorter of the
                     two vertices
    :var c_map - Dictionary representing the group's coxter diagram. Each group operation is a key and a list of
                 commutable group operations are mapped as the value.
    """

    @staticmethod
    def append(vertex_name, op_string: str, c_map=None):
        if c_map is None:
            c_map = {'a': ['b', 'e'], 'b': ['a', 'c'], 'c': ['b', 'd'], 'd': ['c', 'e'], 'e': ['d', 'a']}

        for op in op_string:
            idx = 0
            while idx < len(vertex_name) and op in c_map[vertex_name[idx]]:
                idx += 1
            if idx < len(vertex_name) - 1 and op == vertex_name[idx]:
                vertex_name = vertex_name[:idx] + vertex_name[idx + 1:]
            elif idx < len(vertex_name) and op == vertex_name[idx]:
                vertex_name = vertex_name[:idx]
            elif idx < len(vertex_name):
                vertex_name = vertex_name[:idx] + op + vertex_name[idx:]
            else:
                vertex_name = vertex_name + op

        return vertex_name

    """
    UNFINISHED; Goal is to remove all immediate and obtainable double letters in a string. Obtainable double letters are
    achievable by commuting letters that commute. 
    """

    @staticmethod
    def remove_dupes(vertex_name, c_map=None):
        if c_map is None:
            c_map = {'a': ['b', 'e'], 'b': ['a', 'c'], 'c': ['b', 'd'], 'd': ['c', 'e'], 'e': ['d', 'a']}

        for idx, char in enumerate(vertex_name):
            while idx < len(vertex_name) and char in c_map[vertex_name[idx]]:
                idx += 1
            if idx < len(vertex_name) - 2 and char == vertex_name[idx]:
                vertex_name = vertex_name[:idx] + vertex_name[idx + 2:]
            elif idx < len(vertex_name) and char == vertex_name[idx]:
                vertex_name = vertex_name[:idx]
            elif idx < len(vertex_name):
                vertex_name = vertex_name + char + vertex_name[idx:]
            else:
                vertex_name = vertex_name + char

        return vertex_name

    """
    Last letter algorithm. Recursive algo.
    
    Start with a shortlex word. Determine what the last possible letters of the word can be if we were to commute
        letters to get all possible permutations.
    """

    def last_operations(self):
        if self.name is None or len(self.name) == 0:
            return set()

        last_ops = set(self.name[-1])
        if len(self.name) == 1:
            return last_ops

        return last_ops.union(self.last_operations_recursive(len(self.name) - 1, set(self.c_map[self.name[-1]])))

    def last_operations_recursive(self, end, possible_last_ops):
        last_ops = set(self.name[end])
        if len(self.name[:end]) == 1:
            return last_ops

        possible_last_ops = possible_last_ops.intersection(self.last_operations_recursive(end-1, set(self.c_map[self.name[end]])))
        return last_ops.union(possible_last_ops)

    @staticmethod
    def last_op(name, c_map):
        if len(name) <= 1:
            return set(name)

        l = set(name[-1])
        set(c_map[name[-1]])
        return set(c_map[name[-1]]).intersection(VertexName.last_op(name[:-1], c_map)).union(l)

