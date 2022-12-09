from fsm import FSMGenerator, FSMCrawler
from vertices import VertexName


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
        queue = [FSMCrawler(VertexName(c_map=c_map, o_map=o_map), VertexName(c_map=c_map, o_map=o_map), '', 0)]
        horosphere = []
        # while length <= depth:
        #     if len(queue) == 0:
        #         length += 1
        # while len(queue) > 0:
        #     current_pos = queue.pop(0)
        #     if current_pos[1] < depth:
        #         for edge in jump_table[current_pos[0].name[-1]]:
        #             # Will cause problem with EC
        #             queue.append((VertexName(current_pos[0].name + edge[-1], c_map=c_map, o_map=o_map), current_pos[1] + 1))
        #     horosphere.append(current_pos[0].name)

        while len(queue) > 0:
            crawler = queue.pop(0)
            if crawler.dist_crawled <= depth:
                for edge in jump_table[crawler.current_vertex.name]:
                    # Will cause problem with EC
                    if len(crawler.current_vertex.name) > 0:
                        queue.append(FSMCrawler(VertexName(edge, c_map=c_map, o_map=o_map),
                                                VertexName(crawler.current_vertex.name, c_map=c_map, o_map=o_map),
                                                crawler.current_vertex.name[-1] + edge[-1],
                                                crawler.dist_crawled + 1))
                        horosphere.append(crawler.crawl_history + edge[-1])
                    else:
                        queue.append(FSMCrawler(VertexName(edge, c_map=c_map, o_map=o_map),
                                                VertexName(crawler.current_vertex.name, c_map=c_map, o_map=o_map),
                                                crawler.current_vertex.name + edge[-1],
                                                crawler.dist_crawled + 1))
                        horosphere.append(crawler.crawl_history + edge[-1])

        print(horosphere)


