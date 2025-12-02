import heapq
from dataclasses import dataclass
import datetime
from enum import Enum

class Logger:
    LEVELS = {"WARN": 0, "INFO": 1, "DEBUG": 2}
    WARN =  None
    INFO = None
    DEBUG = None

    def __init__(self, levelname: str="WARN"):
        self.object_level = self._get_nlevel(levelname)

    def _get_nlevel(self, levelname):
        if levelname in type(self).LEVELS:
            return type(self).LEVELS[levelname]
        else:
            return -1

    def _print_message(self, *xs, levelname: str="WARN"):
        msg_level = self._get_nlevel(levelname)
        if msg_level <= self.object_level:
            now = datetime.datetime.now()
            print(f"{now} [{levelname}]", *xs)

    def warn(self, *xs):
        self._print_message(*xs, levelname="WARN")

    def info(self, *xs):
        self._print_message(*xs, levelname="INFO")

    def debug(self, *xs):
        self._print_message(*xs, levelname="DEBUG")

Logger.DEBUG = Logger("DEBUG")
Logger.INFO = Logger("INFO")
Logger.WARN = Logger("WARN")

class Dir:
    ALL = ["N", "E", "S", "W"]

    _CW  = {"N": "E", "E": "S", "S": "W", "W": "N"}
    _CCW = {"N": "W", "W": "S", "S": "E", "E": "N"}

    @classmethod
    def rot_cw(cls, d):
        return cls._CW[d]

    @classmethod
    def rot_ccw(cls, d):
        return cls._CCW[d]

class DirDiag:
    ALL = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]

@dataclass(frozen=True)
class Point:
    x: int
    y: int


    DELTAS = dict(
        N =( 0, -1),
        NE=( 1, -1),
        E =( 1,  0),
        SE=( 1,  1),
        S =( 0,  1),
        SW=(-1,  1),
        W =(-1,  0),
        NW=(-1, -1))

    def __add__(self, other):
        if isinstance(other, Point):
            return Point(self.x + other.x, self.y + other.y)
        elif isinstance(other, tuple):
            return Point(self.x + other[0], self.y + other[1])
        else:
            raise TypeError

    def __sub__(self, other):
        if isinstance(other, Point):
            return Point(self.x - other.x, self.y - other.y)
        else:
            raise TypeError

    def __mul__(self, other):
        if isinstance(other, int):
            return Point(self.x * other, self.y * other)
        else:
            raise TypeError

    def __repr__(self):
        return f"Point({self.x} {self.y})"

    def dist(self, other) -> int:
        """
        Calculate Manhattan distance between two points
        :param other: second Point to calculate distance too
        :return: distance between self and other
        """

        if isinstance(other, Point):
            return abs(self.x - other.x) + abs(self.y - other.y)
        else:
            raise TypeError


    def move(self, dir):
        if dir in type(self).DELTAS:
            return self + type(self).DELTAS[dir]
        else:
            raise Exception(f"bad direction '{dir}'")

    def move_n(self, dir, n):
        if dir in type(self).DELTAS:
            curr = self
            for _ in range(n):
                curr = curr.move(dir)
                yield curr

class CharArray:
    def __init__(self, data, loglevel: str = "WARN"):
        self.logger = Logger(loglevel)
        self.data = data
        self.width = len(self.data[0])
        self.height = len(self.data)

    @classmethod
    def from_file(cls, filename, loglevel: str = "WARN"):
        out = []
        with open(filename, "r") as fh:
            for l in fh:
                l = l.strip()
                out.append(l)
        return cls(out, loglevel=loglevel)

    @classmethod
    def from_file_int(cls, filename, loglevel: str = "WARN"):
        out = []
        with open(filename, "r") as fh:
            for l in fh:
                out.append([int(x) for x in l.strip()])
        return cls(out, loglevel=loglevel)

    def debug_array(self, overset=frozenset, overchar="#"):
        self.logger.debug("\n", *self.render(overset=overset, overchar=overchar))

    def print(self, overset=frozenset(), overchar="#"):
        print("", *self.render(overset=overset, overchar=overchar),)

    def render(self, overset=frozenset(), overchar="#"):
        out = []
        for j, row in enumerate(self.data):
            out.append("")
            for i, c in enumerate(row):
                p = Point(i, j)
                if p in overset:
                    out[-1] += overchar
                else:
                    out[-1] += str(c)
            out[-1] += "\n"
        return out

    def in_bounds(self, p):
        return 0 <= p.y < self.height and 0 <= p.x < self.width

    def get(self, p: Point, default: str = None):
        if self.in_bounds(p):
            return self.data[p.y][p.x]
        else:
            return default

    def enumerate(self):
        for j in range(self.height):
            for i in range(self.width):
                yield Point(i, j), self.data[j][i]

    def find(self, target):
        for j, row in enumerate(self.data):
            for i, c in enumerate(row):
                if c == target:
                    yield Point(i, j)

class PriorityQueue():
    def __init__(self):
        self.heap = []

    def __len__(self):
        return len(self.heap)

    def append(self, item):
        heapq.heappush(self.heap, item)

    def popleft(self):
        return heapq.heappop(self.heap)

@dataclass
class Interval:
    start: int
    end: int

    def __len__(self):
        return self.end - self.start

    def intersect(self, other):
        if self.end <= other.start or other.end <= self.start:
            return None
        else:
            start = max(self.start, other.start)
            end = min(self.end, other.end)
            return Interval(start, end)


def read_lines(filename):
    """Read in each line of a file as an element in a list"""

    lines = []
    with open(filename, "r") as fh:
        for l in fh:
            lines.append(l.rstrip())
    return lines

def read_string(filename):
    return "".join(read_lines(filename))

def split_xs(xs, sep):
    """Split the iterable xs on the separator sep"""
    out = [[]]
    for x in xs:
        if x == sep:
            out.append([])
        else:
            out[-1].append(x)
    return out
