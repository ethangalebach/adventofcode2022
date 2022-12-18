import utils
from itertools import product
import heapq
from dataclasses import dataclass

class Graph:
    def __init__(self, path:str):
        self.start_coord = (None, None)
        self.end_coord = (None, None)
        self.grid = self._parse_grid(path)
        self.coord_to_node_map = self._create_coord_to_node_map(self.grid)
        self.graph = self._create_graph(self.grid, self.coord_to_node_map)

    def _parse_grid(self, path):
        grid = []
        with open(path) as f:
            for line in f:
                row = list(line.strip())
                for col, c in enumerate(row):
                    if c == 'S':
                        self.start_coord = (len(grid), col)
                        row[col] = 'a'
                    if c == 'E':
                        self.end_coord = (len(grid), col)
                        row[col] = 'z'
                grid.append(row)

        return grid

    def _create_coord_to_node_map(self, grid):
        map = {}
        num_rows = len(grid)
        num_cols = len(grid[0])
        for i,j in product(range(num_rows), range(num_cols)):
            node = Node(height=grid[i][j],coord=(i,j))
            map[(i,j)] = node
        return map

    def _create_graph(self, grid, map):
        graph = {}
        for _, node in map.items():
            if not graph.get(node): graph[node] = set()
            graph = self._add_edges(node,graph,grid,map)
        return graph

    def _add_edges(self, node, graph, grid, map):
        num_rows = len(grid)
        num_cols = len(grid[0])
        r = node.coord[0]
        c = node.coord[1]
        if c > 0:
            adj_node = map[(r,c-1)]
            if ord(node.height) - ord(adj_node.height) >= -1:
                graph[node].add(adj_node)
        if c < num_cols-1:
            adj_node = map[(r,c+1)]
            if ord(node.height) - ord(adj_node.height) >= -1:
                graph[node].add(adj_node)
        if r > 0:
            adj_node = map[(r-1,c)]
            if ord(node.height) - ord(adj_node.height) >= -1:
                graph[node].add(adj_node)
        if r < num_rows-1:
            adj_node = map[(r+1,c)]
            if ord(node.height) - ord(adj_node.height) >= -1:
                graph[node].add(adj_node)
        return graph

    def get_shortest_path(self, start_coord=None):
        if not start_coord: start_coord = self.start_coord
        visited = set()
        start_node = self.coord_to_node_map[self.start_coord]
        tentative_paths = [(999_999,node.coord,()) for node in self.graph if node != start_node]
        heapq.heapify(tentative_paths)
        heapq.heappush(tentative_paths, (0,start_node.coord,()))
        while True:
            score, coord, path = heapq.heappop(tentative_paths)
            if coord == self.end_coord:
                return path
            if coord not in visited:
                visited.add(coord)
                cur_node = self.coord_to_node_map[coord]
                for adj_node in self.graph[cur_node]:
                    heapq.heappush(tentative_paths, (score+1, adj_node.coord, path + (adj_node.coord,)))

@dataclass(frozen=True,eq=True)
class Node:
    height: str
    coord: tuple[int,int]


def get_answer(input_path: str, part: int) -> int:
    if part == 1:
        map = Graph(input_path)
        #return [(k.height, k.coord, v) for k, v in map.graph[map.coord_to_node_map[map.end_coord]].items()]
        return len(map.get_shortest_path())
    elif part == 2:
        pass
    else:
        raise Exception('not part 1 or 2')

if __name__ == "__main__":
    input_path = utils.get_input_path(__file__)
    part1_answer = get_answer(input_path, part=1)
    part2_answer = get_answer(input_path, part=2)

    print(
        f"Part 1 Answer: {part1_answer},",
        f"Part 2 Answer: {part2_answer}"
    )
