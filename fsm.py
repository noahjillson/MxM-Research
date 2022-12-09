from vertices import VertexName


class FSMGenerator:
    @staticmethod
    def generate_fsm_nodes(c_map=None, o_map=None) -> dict:
        if c_map is None:
            c_map = {'a': ['b', 'e'], 'b': ['a', 'c'], 'c': ['b', 'd'], 'd': ['c', 'e'], 'e': ['d', 'a']}
        if o_map is None:
            o_map = {'a': 0, 'c': 1, 'b': 2, 'd': 3, 'e': 4}
        nodes = {}

        def is_in_nodes(length):
            for idx in range(0, length+1):
                last_op = candidate.name[-idx:]
                if last_op in nodes and nodes[last_op] == connections:
                    return True
                idx += 1
            return False

        count = 0
        kcount = 0
        # Queue With Start Node
        queue = [VertexName(c_map=c_map, o_map=o_map)]
        longest_node = 0
        while len(queue) > 0:
            candidate = queue.pop(0)
            count += 1
            if count % 10000 == 0:
                count = 0
                kcount += 10
                print(str(kcount) + "k nodes considered, " + str(len(queue) % 1000) + "k nodes queued, "
                      + str(len(nodes)) + " nodes are final")
            connections = candidate.generate_truth_table()
            if len(candidate.name) > 0:
                # last_op = candidate.name[-1:]
                # # Maybe an error here. What if we are considering a connection of a double letter node like ec?
                # if last_op in nodes and nodes[last_op] == connections:
                #     continue
                # for idx in range(0, longest_node):
                #     last_op = candidate.name[-idx:]
                #     if last_op in nodes and nodes[last_op] == connections:
                #         break
                #     if idx == longest_node:
                #         longest_node = max(len(candidate.name), longest_node)
                #         nodes[candidate.name] = connections
                #     idx += 1
                if is_in_nodes(longest_node):
                    continue

            longest_node = max(len(candidate.name), longest_node)
            nodes[candidate.name] = connections

            for key in connections:
                if connections[key]:
                    queue.append(VertexName(start_name=candidate.name + key, c_map=c_map, o_map=o_map))

        return nodes

    @staticmethod
    def generate_jump_table(c_map=None, o_map=None) -> list[list]:
        if c_map is None:
            c_map = {'a': ['b', 'e'], 'b': ['a', 'c'], 'c': ['b', 'd'], 'd': ['c', 'e'], 'e': ['d', 'a']}
        if o_map is None:
            o_map = {'a': 0, 'c': 1, 'b': 2, 'd': 3, 'e': 4}
        nodes = FSMGenerator.generate_fsm_nodes(c_map=c_map, o_map=o_map)

        return nodes
