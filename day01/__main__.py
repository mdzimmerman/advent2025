from dataclasses import dataclass
import sys

sys.path.append("..")
import aoc

def read_instructions(filename):
    out = list()
    for s in aoc.read_lines(filename):
        d = s[:1]
        n = int(s[1:])
        if d == 'L':
            out.append(-1 * n)
        else:
            out.append(n)
    return out

def run(instructions, start = 50):
    curr = start
    count = 0
    for instr in instructions:
        curr = (curr + instr) % 100
        if curr == 0:
            count += 1
    return count

def run2(instructions, start = 50, debug = False):
    curr = start
    count = 0
    for instr in instructions:
        ncurr = (curr + instr)
        dcount = 0
        if ncurr <= 0:
            dcount = abs(ncurr // 100)
            if curr == 0:
                dcount -= 1
            elif ncurr % 100 == 0:
                dcount += 1
        elif ncurr >= 100:
            dcount = (ncurr // 100)
        if debug:
            print(f"{curr} -({instr})-> {ncurr % 100}, {dcount}")
        count += dcount
        curr = ncurr % 100
    return count

if __name__ == '__main__':
    xs = read_instructions('test.txt')
    print(xs)
    print(run(xs))
    print(run2(xs, debug=True))

    xs = read_instructions("input.txt")
    print(run(xs))
    print(run2(xs, debug=True))