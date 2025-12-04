import argparse
import itertools
import sys
from collections import deque

sys.path.append("..")
import aoc

def joltage(s=""):
    nmax = 0
    for i in range(len(s)-1):
        for j in range(i+1, len(s)):
            n = int(s[i] + s[j])
            if n > nmax:
                nmax = n
    return nmax

def joltage_n(s="", n=2, debug=False):
    nmax = 0
    for ids in itertools.combinations(range(len(s)), r=n):
        n = int("".join(s[i] for i in ids))
        if debug: print(ids, n)
        if n > nmax:
            nmax = n
    return nmax

def get_max_indexes(s, start=0, end=None):
    if end == None:
        end = len(s)
    s_sub = s[start:end]
    c_max = max(s_sub)
    out = [i for i, c in enumerate(s) if i >= start and i < end and c == c_max]
    return out

def joltage_eff(s, totallevel=2):
    queue = deque()

    slen = len(s)
    for i in get_max_indexes(s, 0, slen-(totallevel-1)):
        queue.append([i])

    nmax = 0
    while queue:
        current = queue.popleft()
        #print(current)
        level = len(current)
        if level == totallevel:
            n = int("".join(s[i] for i in current))
            #print(current, n)
            if nmax < n:
                nmax = n
        else:
            i = current[-1]
            for j in get_max_indexes(s, i+1, slen-(totallevel-level-1)):
                cnext = current + [j]
                #print(cnext)
                queue.append(cnext)
    return nmax

def test_func(func, **args):
    print(f"{args} {func(**args)}")

def scan_input(filename, n=2, debug=False):
    sum = 0
    for l in aoc.read_lines(filename):
        j = joltage_eff(l, n)
        if debug: print(l, j)
        sum += j
    return sum

def main(args):
    #test_func(joltage, s="987654321111111")
    #test_func(joltage_n, s="987654321111111", n=12, debug=True)

    print("-- part 1 --")
    print(scan_input("test.txt", n=2, debug=True))
    print(scan_input("input.txt", n=2))

    print("-- part 2 --")
    print(scan_input("test.txt", n=12, debug=True))
    print(scan_input("input.txt", n=12))
    #input = aoc.read_lines("input.txt")
    #print(len(input[0]))
    #print(max(input[0]))
    #print(scan_input("input.txt", n=12, debug=True))


if __name__ == '__main__':
    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--log', '-l', choices=["debug", "info", "warning"])
    args = parser.parse_args()

    main(args)