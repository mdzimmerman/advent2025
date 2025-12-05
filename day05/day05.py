from dataclasses import dataclass
import re
import sys
from typing import List

sys.path.append('..')
import aoc

@dataclass
class Interval:
    start: int
    end: int

    PATTERN = re.compile(r"(\d+)-(\d+)")

    def contains(self, n):
        return self.start <= n <= self.end

    def length(self):
        return self.end - self.start + 1

    @classmethod
    def from_string(cls, s):
        m = Interval.PATTERN.match(s)
        if m:
            start = int(m.group(1))
            end = int(m.group(2))
            return cls(start, end)

class FreshList:
    intervals: List[Interval]
    ingredients: List[int]

    def __init__(self, intervals, ingredients):
        self.intervals = intervals
        self.ingredients = ingredients

    def __repr__(self):
        return f"FreshList({self.intervals}, {self.ingredients})"

    def merge_intervals(self):
        merged = []
        for curr in sorted(self.intervals, key=lambda x: x.start):
            if not merged or curr.start > merged[-1].end:
                merged.append(curr)
            else:
                newstart = merged[-1].start
                newend = max(merged[-1].end, curr.end)
                merged[-1] = Interval(newstart, newend)
        return merged

    @classmethod
    def from_file(cls, filename):
        xs1, xs2 = aoc.split_xs(aoc.read_lines(filename), "")
        intervals = [Interval.from_string(s) for s in xs1]
        ingredients = [int(s) for s in xs2]
        return cls(intervals, ingredients)

    def part1(self):
        fresh = 0
        for ingr in self.ingredients:
            for intr in self.intervals:
                if intr.contains(ingr):
                    fresh += 1
                    break
        return fresh

    def part2(self):
        total = 0
        for m in self.merge_intervals():
            total += m.length()
        return total

if __name__ == '__main__':
    i0 = Interval.from_string("11-22")
    print(i0)
    print(i0.contains(10))
    print(i0.contains(15))
    print(i0.contains(30))

    test = FreshList.from_file("test.txt")
    print(test.part1())
    print(test.merge_intervals())
    print(test.part2())

    inp = FreshList.from_file("input.txt")
    print(inp.part1())
    print(inp.part2())
