from collections import deque
import sys
from dataclasses import dataclass

import numpy as np

sys.path.append("..")

@dataclass(frozen=True)
class Node:
    x: int
    y: int
    type: str

    def __repr__(self):
        return f"Node({self.x} {self.y} {self.type})"

class Splitters:
    def __init__(self, filename, debug=False):
        self.filename = filename
        self.debug = debug

        with open(self.filename, 'r') as f:
            # Convert each line into a list of its characters
            data = [list(line.strip()) for line in f]
        self.grid = np.array(data, dtype='U1')
        self.height = self.grid.shape[0]
        self.width = self.grid.shape[1]
        self.graph = self._build_graph()

    def print_grid(self):
        for row in self.grid:
            for c in row:
                print(c, end='')
            print()

    def find_where(self, char):
        y, x = np.where(self.grid == char)
        for j, i in zip(y, x):
            yield Node(i, j, char)

    def find_next_node(self, sx, sy):
        x, y = sx, sy
        while True:
            if y == self.height - 1:
                return Node(x, y, 'E')
            elif self.grid[y, x] == '^':
                return Node(x, y, '^')
            y += 1

    def _build_graph(self):
        visited = set()
        queue = deque()
        graph = dict()

        start = next(self.find_where("S"))
        queue.append(start)

        while queue:
            node = queue.popleft()
            if node in visited:
                continue

            visited.add(node)
            if self.debug: print(node)

            if node.type == 'E':
                graph[node] = None
            elif node.type == 'S':
                nnode = self.find_next_node(node.x, node.y)
                graph[node] = [nnode]
                queue.append(nnode)
            elif node.type == '^':
                nnode1 = self.find_next_node(node.x-1, node.y)
                nnode2 = self.find_next_node(node.x+1, node.y)
                graph[node] = [nnode1, nnode2]
                queue.append(nnode1)
                queue.append(nnode2)
        return graph

    def count_paths(self, source, dest, memo={}):
        """ This is a simplified memoized counting implementation that assumes that
            self.graph is a DAG (which it is)"""

        if source == dest:
            return 1
        if source in memo:
            return memo[source]

        count = 0
        if self.graph[source] is not None:
            for child in self.graph[source]:
                count += self.count_paths(child, dest, memo)

        memo[source] = count
        return count

    def part1(self):
        return len(list(filter(lambda n: n.type == '^', self.graph.keys())))

    def part2(self, debug=False):
        start = next(self.find_where("S"))
        count = 0
        for end in filter(lambda n: n.type == 'E', self.graph.keys()):
            count += self.count_paths(start, end, memo={})
        return count

if __name__ == '__main__':
    test = Splitters("test.txt")
    test.print_grid()

    print(list(test.find_where("S")))
    print(list(test.find_where("^")))
    for k, v in test.graph.items():
        print(k, v)
    print(test.part1())
    print(test.part2())

    inp = Splitters("input.txt")
    print(inp.part1())
    print(inp.part2())