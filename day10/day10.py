import aoc

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
            self.sbuttons.append([int(n) for n in sb[1:-1].split(",")])
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

    def __repr__(self):
        return f'{type(self).__name__}(init={self.init} buttons={self.buttons} joltage={self.joltage})'

    @classmethod
    def from_file(cls, filename):
        return [cls(s) for s in aoc.read_lines(filename)]

if __name__ == '__main__':
    test = Machine.from_file("test.txt")
    test0 = test[0]
    print(test0.draw(0))
    print(test0.draw((0 ^ test0.buttons[4]) ^ test0.buttons[5]))
    print(test0.draw((0 ^ test0.buttons[5]) ^ test0.buttons[4]))
    print(test0.draw(test0.init))