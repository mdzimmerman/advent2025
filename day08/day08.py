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

if __name__ == "__main__":
    test = Junctions("test.txt")
    for b in test.boxes:
        print(b)
    for row in test.dist.sort_values(by='dist')[:20].itertuples():
        i, j = row.i, row.j
        print(i, test.boxes[i], j, test.boxes[j], row.dist)
    #print(test.dist.sort_values(by='dist')[:20])