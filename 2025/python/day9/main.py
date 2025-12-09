import sys
import itertools
from shapely.geometry.polygon import Polygon

TEST = """7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3"""

content = TEST
content = sys.stdin.read()

indices = []

for line in content.splitlines():
    x, y = line.split(",")
    indices.append((int(x), int(y)))

# such a cheat...
bounding_area = Polygon(indices)


def calc_area(x, y):
    return (abs(x[0] - y[0]) + 1) * (abs(x[1] - y[1]) + 1)


def rectangle_corners(x, y):
    return x, (x[0], y[1]), y, (y[0], x[1])


p1 = 0
p2 = 0

for first, second in itertools.combinations(indices, 2):
    area = calc_area(first, second)
    if bounding_area.contains(Polygon(rectangle_corners(first, second))):
        p2 = max(p2, area)
    p1 = max(area, p1)

print(p1)
print(p2)
