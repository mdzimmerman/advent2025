import itertools
import re
import sys
from dataclasses import dataclass
from itertools import islice

sys.path.append("..")
import aoc

@dataclass
class Interval:
    start: int
    end: int

    PATTERN = re.compile(r"(\d+)-(\d+)")

    def iterrange(self):
        for i in range(self.start, self.end+1):
            yield i

    @classmethod
    def from_string(cls, s):
        m = cls.PATTERN.match(s)
        if m:
            return cls(int(m.group(1)), int(m.group(2)))

    @classmethod
    def list_from_file(cls, filename):
        return [cls.from_string(s) for s in aoc.read_lines(filename)[0].split(',')]

def doubled(n):
    s = str(n)
    slen = len(s)
    if (slen % 2) == 0:
        i = slen // 2
        if s[:i] == s[i:]:
            return True
    return False

def batched(xs, size=1):
    iterator = iter(xs)
    while batch := tuple(itertools.islice(iterator, size)):
        yield "".join(batch)

def duplicated(n):
    s = str(n)
    slen = len(s)
    for i in range(1, slen // 2 + 1):
        if slen % i == 0:
            ss = set(batched(s, i))
            #print(f"{ss} {len(set(ss))}")
            if len(ss) == 1:
                return True
    return False

def screen_file(filename, func, debug=False):
    sum = 0
    for interval in Interval.list_from_file(filename):
        if debug: print(interval)
        for i in interval.iterrange():
            if func(i):
                if debug: print(i)
                sum += i
    return sum

def part1(filename, debug=False):
    return screen_file(filename, doubled, debug=debug)

def part2(filename, debug=False):
    return screen_file(filename, duplicated, debug=debug)

def test(n, func):
    print(f"{n} {func(n)}")


def main():
    i1 = Interval.from_string("11-22")
    print(i1)
    print(list(i1.iterrange()))
    test(1212, doubled)
    test(1234, doubled)

    test("12312312312", duplicated)
    test("456456456", duplicated)

    print(part1("test.txt"))
    print(part1("input.txt"))

    print(part2("test.txt"))
    print(part2("input.txt"))


if __name__ == '__main__':
    main()