import pandas as pd
import shapely

class Tiles:
    def __init__(self, filename):
        self.tiles = pd.read_csv(filename, header=None, names=["x", "y"])
        data = {"x1": [], "y1": [], "x2": [], "y2": []}
        for p1 in self.tiles.itertuples():
            for p2 in list(self.tiles.itertuples())[p1.Index + 1:]:
                data["x1"].append(p1.x)
                data["y1"].append(p1.y)
                data["x2"].append(p2.x)
                data["y2"].append(p2.y)
        self.areas = pd.DataFrame(data=data)
        self.areas["area"] = ((self.areas.x2 - self.areas.x1).abs() + 1) * ((self.areas.y2 - self.areas.y1).abs() + 1)

    def part1(self):
        return max(self.areas["area"])

    def part2(self):
        full = shapely.Polygon((t.x, t.y) for t in self.tiles.itertuples())
        areamax = 0
        for a in self.areas.itertuples():
            if a.x1 != a.x2 and a.y1 != a.y2:
                xmin = min(a.x1, a.x2)
                xmax = max(a.x1, a.x2)
                ymin = min(a.y1, a.y2)
                ymax = max(a.y1, a.y2)
                box = shapely.box(xmin, ymin, xmax, ymax)
                if full.contains(box) and a.area > areamax:
                    #print(box)
                    areamax = a.area
        return areamax

if __name__ == "__main__":
    print("-- test --")
    test = Tiles("test.txt")
    print(test.areas)
    print(test.part1())
    print(test.part2())


    print("-- input --")
    inp = Tiles("input.txt")
    print(inp.part1())
    print(inp.part2())