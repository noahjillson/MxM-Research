class VertexName:
    def __init__(self, start_name="", c_map=None, o_map=None):
        if c_map is None:
            c_map = {'a': ['b', 'e'], 'b': ['a', 'c'], 'c': ['b', 'd'], 'd': ['c', 'e'], 'e': ['d', 'a']}
        if o_map is None:
            o_map = {'a': 0, 'c': 1, 'b': 2, 'd': 3, 'e': 4}
        self.name = start_name
        self.c_map = c_map
        self.o_map = o_map

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if other is VertexName:
            return self.name == other.name
        return False

    def sort_name(self, char: str) -> str:
        if len(char) > 1 or len(char) == 0:
            print("Cannot sort multiple operations at one time")
            return self.name
        if len(self.name) == 0:
            return char

        min_str = self.name + char
        min_char_idx = len(self.name + char)  # this is just len(self.name) but more legible
        idx = len(self.name) - 1

        while idx >= 0 and char in self.c_map[self.name[idx]]:
            if self.o_map[char] < self.o_map[self.name[idx]]:
                min_str = self.name[:idx] + char + self.name[idx:]
                # Set min_char_idx
                min_char_idx = idx # Doesn't work
            idx -= 1

        # Does not remove double letters correctly
        # It seems like we are removing double letters even if we should not have commuted in the first place
        # consider 'adc' and 'd', then clearly 'adcd' is an accepted string however after the loop we will have
        # idx = 1 and 'd' == 'adc'.charAt(1) but we never should have commuted in the first place
        # print("Char:" + char + ",Name[idx]:" + self.name[idx] + ",idx:" + str(idx))
        # To fix this we can compare char == self.name[idx] and idx == min_char_idx MAYBE
        if idx >= 0 and char == self.name[idx]:  # and idx == min_char_idx:
            if idx+1 > len(self.name) - 1:
                return self.name[:idx]
            return self.name[:idx] + self.name[idx+1]

        return min_str

    def is_valid_append(self, char: str) -> bool:
        if len(char) > 1 or len(char) == 0:
            print("Cannot append multiple operations at one time")
            return False

        return self.sort_name(char) == self.name + char

    def generate_truth_table(self) -> dict:
        truth_table = {}
        for char in self.o_map:
            truth_table[char] = self.is_valid_append(char)
        return truth_table


    @staticmethod
    def append(vertex_name, op_string: str, c_map=None):
        if c_map is None:
            c_map = {'a': ['b', 'e'], 'b': ['a', 'c'], 'c': ['b', 'd'], 'd': ['c', 'e'], 'e': ['d', 'a']}

        for op in op_string:
            idx = 0
            while idx < len(vertex_name) and op in c_map[vertex_name[idx]]:
                idx += 1
            if idx < len(vertex_name)-1 and op == vertex_name[idx]:
                vertex_name = vertex_name[:idx] + vertex_name[idx+1:]
            elif idx < len(vertex_name) and op == vertex_name[idx]:
                vertex_name = vertex_name[:idx]
            elif idx < len(vertex_name):
                vertex_name = vertex_name[:idx] + op + vertex_name[idx:]
            else:
                vertex_name = vertex_name + op

        return vertex_name


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
