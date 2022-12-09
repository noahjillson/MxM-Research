from fsm import FSMGenerator, FSMCrawler
import matplotlib.pyplot as plt
from vertices import VertexName
import networkx as nx
#import scipy


class HorosphereGenerator:
    @staticmethod
    def generate_horosphere(depth, c_map=None, o_map=None) -> list:
        if c_map is None:
            c_map = {'a': ['b', 'e'], 'b': ['a', 'c'], 'c': ['b', 'd'], 'd': ['c', 'e'], 'e': ['d', 'a']}
        if o_map is None:
            o_map = {'a': 0, 'c': 1, 'b': 2, 'd': 3, 'e': 4}

        jump_table = FSMGenerator.generate_jump_table(c_map=c_map, o_map=o_map)

        # Uses assumption that a and c connect to the same vertices
        length = 0
        queue = [FSMCrawler(VertexName('b', c_map=c_map, o_map=o_map), VertexName(c_map=c_map, o_map=o_map), 'b', 1),
                 FSMCrawler(VertexName('d', c_map=c_map, o_map=o_map), VertexName(c_map=c_map, o_map=o_map), 'd', 1),
                 FSMCrawler(VertexName('e', c_map=c_map, o_map=o_map), VertexName(c_map=c_map, o_map=o_map), 'e', 1)]
        horosphere = ['', 'b', 'd', 'e']

        while len(queue) > 0:
            crawler = queue.pop(0)
            if crawler.dist_crawled < depth:
                for edge in jump_table[crawler.current_vertex.name]:
                    # Will cause problem with EC
                    queue.append(FSMCrawler(VertexName(edge, c_map=c_map, o_map=o_map),
                                            VertexName(crawler.current_vertex.name, c_map=c_map, o_map=o_map),
                                            crawler.crawl_history + edge[-1],
                                            crawler.dist_crawled + 1))
                    horosphere.append(crawler.crawl_history + edge[-1])

        return horosphere

    @staticmethod
    def process_horosphere(horosphere):

        post_processed_horosphere = []
        map = ['a', 'c']
        for vertex in horosphere:
            mod = 0
            prefix = ''
            for idx, x in enumerate(vertex):
                prefix = prefix + map[mod]
                mod = (mod + 1) % 2
            post_processed_horosphere.append(prefix + vertex)

        return post_processed_horosphere


    @staticmethod
    def visualize_horosphere(horosphere):
        connections = []
        for idx, x in enumerate(horosphere):
            if len(x) == 0:
                pass
            else:
                window = idx + 1
                while window < len(horosphere) and abs(len(horosphere[window]) - len(horosphere[idx])) <= 2:
                    if len(VertexName.append(horosphere[window], horosphere[idx])) == 2:
                        connections.append([horosphere[idx], horosphere[window]])
                    window += 1

        G = nx.Graph()
        print(G)
        print(connections)
        connections.append(['', 'ab'])
        connections.append(['', 'ad'])
        connections.append(['', 'ae'])
        fig, axes = plt.subplots(figsize=(9, 5))
        G.add_edges_from(connections)

        nx.draw(G, pos=nx.planar_layout(G), node_size=20, with_labels=False, font_size=5, node_color='pink', alpha=1)

        plt.show()
