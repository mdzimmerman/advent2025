from collections import deque, namedtuple

import aoc
import numpy as np
import sympy

def itersum(dim, nmax):
    if dim == 1:
        return itersum1(nmax)
    elif dim == 2:
        return itersum2(nmax)
    elif dim == 3:
        return itersum3(nmax)
    else:
        raise RuntimeError("can't iterate over 3 dimensions")

def itersum1(nmax):
    for x1 in range(nmax+1):
        yield (x1,)

def itersum2(nmax):
    for x1 in range(nmax+1):
        for x2 in range(nmax-x1+1):
            yield (x1, x2)

def itersum3(nmax):
    for x1 in range(nmax+1):
        for x2 in range(nmax-x1+1):
            for x3 in range(nmax-x1-x2+1):
                yield (x1, x2, x3)

class Machine:

    def __init__(self, s):
        #cls = type(self)
        ss = s.split(" ")
        self.slights = ss[0][1:-1]
        self.length = len(self.slights)
        self.init = self.parse_diagram(self.slights)

        self.joltage = [int(n) for n in ss[-1][1:-1].split(",")]

        self.sbuttons = list()
        for sb in ss[1:-1]:
            self.sbuttons.append(set(int(n) for n in sb[1:-1].split(",")))
        self.buttons = list()
        for sb in self.sbuttons:
            self.buttons.append(self.parse_list(sb))

    def parse_diagram(self, s):
        out = 0
        for i, c in enumerate(s):
            if c == "#":
                out |= 1 << i
        return out

    def parse_list(self, xs):
        out = 0
        for x in xs:
            out |= 1 << x
        return out

    def draw(self, n):
        out = ""
        for i in range(self.length):
            if (n & (1 << i)) != 0:
                out += "#"
            else:
                out += "."
        return out

    def find_part1(self):
        State = namedtuple("State", ["lights", "n", "pushed", "left"])

        left = set(range(len(self.buttons)))
        start = State(lights=0, n=0, pushed=set(), left=left)
        queue = deque()
        queue.append(start)

        while queue:
            state = queue.popleft()
            if state.lights == self.init:
                #print(state)
                return state.n
            for i in state.left:
                queue.append(State(state.lights ^ self.buttons[i], state.n+1, state.pushed|{i}, state.left-{i}))
        return None

    def rref(self, mat):
        rref_sympy, pivot_cols = sympy.Matrix(mat).rref()
        return np.array(rref_sympy, dtype=np.int32), pivot_cols

    def part2(self):
        #print(self.sbuttons)
        #print(self.buttons)
        nb = len(self.sbuttons)
        #print(self.length, nb)
        A = np.zeros((self.length, nb), dtype=np.int32)
        for i, sb in enumerate(self.sbuttons):
            for j in sb:
                A[j, i] = 1
        y = np.array(self.joltage, dtype=np.int32)[:, np.newaxis]
        #print(A)
        #print(y)
        Ay = np.concatenate((A, y), axis=1)
        print(Ay)
        Ay_rref, depvar = self.rref(Ay)
        print(Ay_rref)
        inpvar = list()
        for i in range(nb):
            if i not in depvar:
                inpvar.append(i)

        #print(inpvar, depvar)
        #x = np.array((1, 3, 0, 3, 1, 2), dtype=np.int32)
        #print(A @ x.T)

        nmax = sum(Ay_rref[:, -1])
        bmin = nmax
        if not inpvar:
            print(bmin)
            return bmin

        for xis in itersum(len(inpvar), nmax):
            x = np.zeros((nb), dtype=np.int32)
            z = Ay_rref[:, -1]
            for i, xi in zip(inpvar, xis):
                z = z - xi * Ay_rref[:, i]
                x[i] = xi
            for i, dv in enumerate(depvar):
                x[dv] = z[i]
            if np.all(x >= 0) and sum(x) <= bmin:
                bmin = sum(x)
                print(bmin, x, "=>", A @ x.T)
        return bmin


    def __repr__(self):
        return f'{type(self).__name__}(init={self.init} sbuttons={self.sbuttons} buttons={self.buttons} joltage={self.joltage})'

    @classmethod
    def from_file(cls, filename):
        return [cls(s) for s in aoc.read_lines(filename)]

def part1(machines, debug=False):
    count = 0
    for m in machines:
        mc = m.find_part1()
        if debug: print(mc, m)
        count += mc
    return count

def part2(machines, debug=False):
    count = 0
    for m in machines:
        mc = m.part2()
        if debug: print(mc, m)
        count += mc
    return count

if __name__ == '__main__':
    test = Machine.from_file("test.txt")
    #print(test[0])
    #print(part1(test))
    #test[0].part2()
    print(part2(test, debug=True))

    #for x in itersum(1, 10):
    #    print(x)

    #inp = Machine.from_file("input.txt")
    #print(part1(inp))
