from vertices import VertexName
import networkx as nx
import matplotlib.pyplot as plt


class FSMGenerator:
    @staticmethod
    def generate_fsm_nodes(c_map=None, o_map=None) -> dict:
        if c_map is None:
            c_map = {'a': ['b', 'e'], 'b': ['a', 'c'], 'c': ['b', 'd'], 'd': ['c', 'e'], 'e': ['d', 'a']}
        if o_map is None:
            o_map = {'a': 0, 'c': 1, 'b': 2, 'd': 3, 'e': 4}
        nodes = {}

        def is_in_nodes(length):
            for idx in range(0, length + 1):
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
                if is_in_nodes(longest_node):
                    continue

            longest_node = max(len(candidate.name), longest_node)
            nodes[candidate.name] = connections

            for key in connections:
                if connections[key]:
                    queue.append(VertexName(start_name=candidate.name + key, c_map=c_map, o_map=o_map))

        return nodes

    @staticmethod
    def generate_jump_table(c_map=None, o_map=None) -> dict:
        if c_map is None:
            c_map = {'a': ['b', 'e'], 'b': ['a', 'c'], 'c': ['b', 'd'], 'd': ['c', 'e'], 'e': ['d', 'a']}
        if o_map is None:
            o_map = {'a': 0, 'c': 1, 'b': 2, 'd': 3, 'e': 4}
        nodes = FSMGenerator.generate_fsm_nodes(c_map=c_map, o_map=o_map)

        return FSMGenerator.generate_jump_table_from_nodes(nodes)

    @staticmethod
    def generate_jump_table_from_nodes(nodes) -> dict:
        if nodes is None:
            print("nodes cannot be None, empty jump table returned")
            return {}

        jump_table = {}
        # Loop through each vertex in the nodes
        for name in nodes:
            connections = nodes[name]
            out_connections = set()
            # Add all vertices that name connects to (we can think of these as edges from name to edge)
            for edge in connections:
                if connections[edge]:
                    # Connect edges to special nodes (think e to ec)
                    if name + edge in nodes:
                        out_connections.add(name + edge)
                    else:
                        out_connections.add(edge)
            jump_table[name] = out_connections

        return jump_table

    @staticmethod
    def visualize_from_jump_table(c_map=None, o_map=None):
        if c_map is None:
            c_map = {'a': ['b', 'e'], 'b': ['a', 'c'], 'c': ['b', 'd'], 'd': ['c', 'e'], 'e': ['d', 'a']}
        if o_map is None:
            o_map = {'a': 0, 'c': 1, 'b': 2, 'd': 3, 'e': 4}

        G = nx.DiGraph()
        jump_table = FSMGenerator.generate_jump_table(c_map=c_map, o_map=o_map)

        # Load all nodes into the digraph
        for node in jump_table:
            G.add_node(node)

        # Load all directional edges
        for start in jump_table:
            for end in jump_table[start]:
                print(start + ", " + end)
                G.add_edge(start, end, label=end[-1])

        print(G)
        # edge_labels = {(n1, n2[-1]): n2[-1] for n1, n2 in G.edges}
        # print(edge_labels)
        #pos = nx.shell_layout(G)
        #pos = {'': [0, -0.4], 'a': [-0.32348962, -0.78183162], 'c': [0.22252104, -0.9749279], 'b': [0.40096885, -0.23388376], 'd': [0.30096891, 0.33388364], 'e': [-0.12252069, 0.67492796], 'ec': [-0.32348956,  0.28183168]}
        #pos = {'': [0, 0], 'a': [-1.1, -1.2], 'c': [1, -1], 'b': [0.5, -0.5], 'd': [1, 1], 'e': [-1, 1], 'ec': [-1.5,  0.5]}
        edge_labels = dict([((u, v,), d['label']) for u, v, d in G.edges(data=True)])
        nx.draw(G, pos=nx.circular_layout(G), node_size=500, with_labels=True, font_size=12, arrowsize=15, node_color='pink')
        # nx.draw_networkx_edge_labels(G, pos=pos, edge_labels=edge_labels)
        plt.show()
