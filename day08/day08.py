import math
from dataclasses import dataclass

import pandas as pd

import aoc

@dataclass(frozen=True)
class Point:
    x: int
    y: int
    z: int

    def __repr__(self):
        return f"Point({self.x} {self.y} {self.z})"

    def dist(self, other):
        return math.sqrt(abs(self.x - other.x) ** 2 + abs(self.y - other.y) ** 2 + abs(self.z - other.z) ** 2)

    @classmethod
    def from_string(cls, s):
        return cls(*(int(x) for x in s.split(",")[:3]))


class Junctions:
    def __init__(self, filename):
        self.filename = filename
        self.boxes = self._read_boxes(filename)
        self.dist = self._calculate_distances()

    def _read_boxes(self, filename):
        boxes = [Point.from_string(s) for s in aoc.read_lines(filename)]
        return boxes

    def _calculate_distances(self):
        data = {'i': [], 'j': [], 'dist': []}
        for i in range(len(self.boxes)):
            for j in range(i+1, len(self.boxes)):
                data['i'].append(i)
                data['j'].append(j)
                data['dist'].append(self.boxes[i].dist((self.boxes[j])))
        return pd.DataFrame(data)

    def find_group(self, i, subgroups):
        for gi, group in subgroups.items():
            if i in group:
                return gi

    def part1(self, n=10):
        subgroups = dict()
        for i in range(len(self.boxes)):
            subgroups[i] = set()
            subgroups[i].add(i)

        for row in self.dist.sort_values(by='dist')[:n].itertuples():
            i, j = row.i, row.j
            gi = self.find_group(i, subgroups)
            gj = self.find_group(j, subgroups)
            if gi != gj:
                subgroups[gi] = subgroups[gi] | subgroups[gj]
                del subgroups[gj]

        lengths = []
        for groups in subgroups.values():
            lengths.append(len(groups))

        return math.prod(sorted(lengths, reverse=True)[0:3])

    def part2(self):
        subgroups = dict()
        for i in range(len(self.boxes)):
            subgroups[i] = set()
            subgroups[i].add(i)

        for row in self.dist.sort_values(by='dist').itertuples():
            i, j = row.i, row.j
            gi = self.find_group(i, subgroups)
            gj = self.find_group(j, subgroups)
            if gi != gj:
                subgroups[gi] = subgroups[gi] | subgroups[gj]
                del subgroups[gj]
                if len(subgroups) == 1:
                    boxi = self.boxes[i]
                    boxj = self.boxes[j]
                    print(boxi, boxj)
                    return boxi.x * boxj.x


if __name__ == "__main__":
    test = Junctions("test.txt")
    for b in test.boxes:
        print(b)
    print(test.part1(n=10))
    print(test.part2())

    inp = Junctions("input.txt")
    print(inp.part1(n=1000))
    print(inp.part2())