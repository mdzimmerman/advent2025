from collections import deque
import sys
import numpy as np

sys.path.append("..")
from aoc import Point

class CharArray:
    def __init__(self, filename):
        self.filename = filename

        with open(self.filename, 'r') as f:
            # Convert each line into a list of its characters
            data = [list(line.strip()) for line in f]
        self.grid = np.array(data, dtype='U1')

    def print_grid(self):
        for row in self.grid:
            for c in row:
                print(c, end='')
            print()

    def run_beam(self):
        self.active = 0
        self.inactive = 0
        for j in range(1, self.grid.shape[0]):
            for i in  range(self.grid.shape[1]):
                c = self.grid[j, i]
                above = self.grid[j-1, i]
                if c == '.':
                    if above == 'S' or above == '|':
                        self.grid[j, i] = '|'
                elif c == '^':
                    if above == '|':
                        self.active += 1
                        self.grid[j, i-1] = '|'
                        self.grid[j, i+1] = '|'
                    else:
                        self.inactive += 1

    def find_next(self, start: Point):
        p = Point(start.x, start.y)
        while True:
            if p.y == self.grid.shape[0]-1:
                return (p, 'E')
            elif self.grid[p.y, p.x] == '^':
                return (p, '^')
            p = Point(p.x, p.y+1)

    def part2(self, debug=False):
        count = 0
        y, x = np.where(self.grid == '^')
        start = Point(x[0], y[0])

        queue = deque()
        queue.append((start, '^'))

        while queue:
            p, typ = queue.popleft()
            if debug: print(p, typ)
            if typ == 'E':
                count += 1
            elif typ == '^':
                queue.append(self.find_next(Point(p.x-1, p.y)))
                queue.append(self.find_next(Point(p.x+1, p.y)))

        return count

if __name__ == '__main__':
    test = CharArray("test.txt")
    #print(test.grid)
    test.print_grid()
    print()
    #test.run_beam()
    #test.print_grid()
    #print(test.active)
    print(test.part2(debug=True))

    inp = CharArray("input.txt")
    #inp.run_beam()
    #print(inp.active)
    print(inp.part2())