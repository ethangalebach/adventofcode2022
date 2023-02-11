import utils
import functools
import itertools
import networkx as nx
from dataclasses import dataclass

class ValveGraph:
    def __init__(self, path:str):
        self.graph, self.pressure_map, self.nodes, self.flow_nodes = self._parse_graph(path)

    def _parse_graph(self, path):
        graph = nx.Graph()
        pressure_map = {}
        nodes = frozenset()
        flow_nodes = frozenset()
        with open(path) as f:
            for line in f:
                words = str.split(line, ' ')
                valve = words[1]
                graph.add_node(valve)
                for w in words[9:]:
                    graph.add_edge(valve, w[:-1])
                pressure = int(str.split(words[4],'=')[-1][:-1])
                pressure_map[valve] = pressure
                nodes = nodes.union(frozenset([valve]))
                if pressure > 0:
                    flow_nodes = flow_nodes.union(frozenset([valve]))
        return self._get_subgraph(flow_nodes,graph), pressure_map, nodes, flow_nodes

    def _get_subgraph(self, flow_nodes, graph):
        subgraph = {k:{} for k in flow_nodes | {'AA'}}
        for fn1,fn2 in itertools.product(flow_nodes | {'AA'}, flow_nodes):
            if fn1 == fn2: continue
            to = {fn2: nx.shortest_path_length(graph,fn1,fn2)}
            subgraph[fn1][fn2] = nx.shortest_path_length(graph,fn1,fn2)
        return subgraph

    def get_max_pressure(self, travelers:int):
        if travelers==1:
            return self.dfs('AA',0,frozenset(),0,min_left=30)
        if travelers==2:
            return self.dfs2(frozenset({('AA',0)}),frozenset(),0,min_left=26)

    @functools.cache
    def dfs(self, dest_node, dist, open, flow, min_left):
        future_flow = flow*min_left
        if open.union(frozenset([dest_node])) == self.flow_nodes:
            future_flow = flow*(dist+1)+(min_left-dist-1)*(flow+self.pressure_map[dest_node])
        elif dest_node == 'AA':
            for nb,l in self.graph[dest_node].items():
                future_flow = max(future_flow, self.dfs(nb,l,open,flow,min_left))
        elif dist < min_left:
            new_open = open.union(frozenset([dest_node]))
            new_flow = flow + self.pressure_map[dest_node]
            for nb,l in self.graph[dest_node].items():
                if nb not in open:
                    future_flow = max(future_flow, flow*(dist+1)+self.dfs(nb,l,new_open,new_flow,min_left-dist-1))
        return future_flow

    @functools.cache
    def dfs2(self, dest_nodes, open, flow, min_left):
        if min_left == 0:
            return 0
        if len(dest_nodes) == 1:
            ((dest_node1,dist1),) = dest_nodes
            ((dest_node2,dist2),) = dest_nodes
        else:
            (dest_node1,dist1),(dest_node2,dist2) = dest_nodes

        if dist1 > 0 and dist2 > 0:
            new_dest_nodes = frozenset({(dest_node1, dist1-1), (dest_node2,dist2-1)})
            future_flow = self.dfs2(new_dest_nodes,open,flow,min_left-1)
            return flow + future_flow

        future_flow = 0
        closed_nbs1 = [(nb,l) for nb,l in self.graph[dest_node1].items() if nb not in open]
        closed_nbs2 = [(nb,l) for nb,l in self.graph[dest_node2].items() if nb not in open]

        if dist1 == 0 and dist2 == 0:
            if open.union(frozenset([dest_node1,dest_node2])) == self.flow_nodes:
                new_flow = sum([self.pressure_map[n] for n in self.flow_nodes])
                future_flow = (min_left-1)*new_flow
                return flow + future_flow
            if dest_node1 == 'AA' and dest_node2 == 'AA':
                for (nb1,l1),(nb2,l2) in itertools.product(closed_nbs1,closed_nbs2):
                    if nb1 != nb2:
                        new_dest_nodes = frozenset({(nb1,l1-1),(nb2,l2-1)})
                        pass_future_flow = self.dfs2(new_dest_nodes,open,flow,min_left-1)
                        future_flow = max(future_flow, pass_future_flow)
            if dest_node1 not in open and dest_node2 not in open and dest_node1 != 'AA' and dest_node2 != 'AA':
                new_open = open.union(frozenset([dest_node1,dest_node2]))
                new_flow = flow + self.pressure_map[dest_node1] + self.pressure_map[dest_node2]
                for (nb1,l1),(nb2,l2) in itertools.product(closed_nbs1,closed_nbs2):
                    if nb1 != nb2:
                        new_dest_nodes = frozenset({(nb1,l1),(nb2,l2)})
                        openboth_future_flow = self.dfs2(new_dest_nodes,new_open,new_flow,min_left-1)
                        future_flow = max(future_flow, openboth_future_flow)

        elif dist1 == 0 and dist2 > 0:
            if open.union(frozenset([dest_node1])) == self.flow_nodes:
                new_flow = sum([self.pressure_map[n] for n in self.flow_nodes])
                future_flow = (min_left-1)*new_flow
                return flow + future_flow
            if dest_node1 not in open and dest_node1 != 'AA':
                new_open = open.union(frozenset([dest_node1]))
                new_flow = flow + self.pressure_map[dest_node1]
                for nb1,l1 in closed_nbs1:
                    if nb1 != dest_node2 or len(closed_nbs1) == 1:
                        new_dest_nodes = frozenset({(nb1,l1),(dest_node2,dist2-1)})
                        open1_future_flow = self.dfs2(new_dest_nodes,new_open,new_flow,min_left-1)
                        future_flow = max(future_flow, open1_future_flow)

        elif dist2 == 0 and dist1 > 0:
            if open.union(frozenset([dest_node2])) == self.flow_nodes:
                new_flow = sum([self.pressure_map[n] for n in self.flow_nodes])
                future_flow = (min_left-1)*new_flow
                return flow + future_flow
            if dest_node2 not in open and dest_node2 != 'AA':
                new_open = open.union(frozenset([dest_node2]))
                new_flow = flow + self.pressure_map[dest_node2]
                for nb2,l2 in closed_nbs2:
                    if nb2 != dest_node1 or len(closed_nbs2) == 1:
                        new_dest_nodes = frozenset({(nb2,l2),(dest_node1,dist1-1)})
                        open2_future_flow = self.dfs2(new_dest_nodes,new_open,new_flow,min_left-1)
                        future_flow = max(future_flow, open2_future_flow)

        return flow + future_flow

def get_answer(input_path:str, part:int) -> int:
    valve_graph = ValveGraph(input_path)
    if part == 1:
        return valve_graph.get_max_pressure(travelers=1)
    elif part == 2:
        return valve_graph.get_max_pressure(travelers=2) #not sure how to further reduce time complexity
    else:
        raise Exception('not part 1 or 2')

if __name__ == "__main__":
    input_path = utils.get_input_path(__file__)
    test_path = utils.get_test_path(__file__)
    test_part1_answer = get_answer(test_path, part=1)
    assert test_part1_answer == 1651, f"got max pressure of {test_part1_answer} on {test_path}, should be 1651"
    part1_answer = get_answer(input_path, part=1)
    test_part2_answer = get_answer(test_path, part=2)
    assert test_part2_answer == 1707, f"got max pressure of {test_part2_answer} on {test_path}, should be 1707"
    # part2_answer = get_answer(input_path, part=2)

    print(
        f"Test Part 1 Answer: {test_part1_answer},",
        f"Part 1 Answer: {part1_answer},",
        f"Test Part 2 Answer: {test_part2_answer},",
        # f"Part 2 Answer: {part2_answer}"
    )