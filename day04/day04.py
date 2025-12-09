import collections.abc
import sys
from typing import Set

sys.path.append("..")
import aoc
from aoc import Point

class GridSet(collections.abc.MutableSet):
    _points: Set[Point]
    width: int
    height: int

    def __init__(self, points, width, height):
        self._points = points
        self.width = width
        self.height = height

    def __contains__(self, point):
        return point in self._points

    def __len__(self):
        return len(self._points)

    def __iter__(self):
        return iter(self._points)

    def add(self, p: Point):
        self._points.add(p)

    def discard(self, p: Point):
        self._points.discard(p)

    def __repr__(self):
        return f"GridSet({list(self._points)}, w={self.width}, h={self.height})"

    def print_grid(self):
        for j in range(self.height):
            for i in range(self.width):
                p = Point(i, j)
                if p in self._points:
                    print("@", end="")
                else:
                    print(".", end="")
            print()

    @classmethod
    def from_file(cls, filename):
        points = set()
        width = 0
        height = 0
        for j, line in enumerate(aoc.read_lines(filename)):
            height += 1
            if len(line) > width:
                width = len(line)
            for i, c in enumerate(line):
                p = Point(i, j)
                if c == '@':
                    points.add(p)
        return cls(points, width, height)

def find_removable(grid: GridSet):
    out = list()
    for p in grid:
        n = len([pn for pn in p.neighbors() if pn in grid])
        if n < 4:
            out.append(p)
    return out

def part1(grid: GridSet):
    return len(find_removable(grid))

def part2(grid: GridSet, debug=False):
    nremoved = 0
    rem = find_removable(grid)
    if debug: grid.print_grid()
    while len(rem) > 0:
        for r in rem:
            grid.remove(r)
        nremoved += len(rem)
        if debug:
            print()
            grid.print_grid()
        rem = find_removable(grid)
    return nremoved

if __name__ == "__main__":
    test = GridSet.from_file("test.txt")
    print(part1(test))
    print(part2(test, debug=True))

    inp = GridSet.from_file("input.txt")
    print(part2(inp))