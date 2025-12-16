import operator
import sys
from functools import reduce

sys.path.append("..")
import aoc

class SquidMath:
    def __init__(self, filename):
        self.filename = filename
        self.lines = aoc.read_lines(filename)
        self.problems = self._get_problems()

    def _find_breaks(self):
        for i in range(min(len(l) for l in self.lines)):
            if all(l[i] == ' ' for l in self.lines):
                yield i

    def _get_problems(self):
        i = 0
        problems = []
        for j in self._find_breaks():
            problems.append([s[i:j] for s in self.lines])
            i = j+1
        problems.append([s[i:] for s in self.lines])

        # fix alignment of last problem
        smax = max(len(s) for s in problems[-1])
        for i, s in enumerate(problems[-1]):
            sdiff = smax - len(s)
            if sdiff > 0:
                problems[-1][i] = s + (" " * sdiff)

        return problems

    def _get_horiz_numbers(self, xs):
        return [int(n) for n in xs]

    def _get_vert_numbers(self, xs):
        width = len(xs[0])
        ns = [""] * width
        for r in xs:
            for i in range(len(xs[0])):
                ns[i] += r[i]
        return [int(n) for n in ns]

    def run(self, part=1, debug=False):
        sum = 0
        for p in self.problems:
            op = p[-1].strip()
            ns = None
            if part == 1:
                ns = self._get_horiz_numbers(p[:-1])
            elif part == 2:
                ns = self._get_vert_numbers(p[:-1])

            if op == "+":
                out = reduce(operator.add, ns)
            elif op == "*":
                out = reduce(operator.mul, ns)

            if debug: print(op, ns, out)
            sum += out
        return sum

    def part1(self, debug=False):
        return self.run(part=1, debug=debug)

    def part2(self, debug=False):
        return self.run(part=2, debug=debug)


def main():
    test = SquidMath("test.txt")
    print(test.lines)
    print(test.problems)
    print(test.part1(debug=True))
    print(test.part2(debug=True))

    inp = SquidMath("input.txt")
    print(inp.part1())
    print(inp.part2())

if __name__ == '__main__':
    main()
