import itertools
from collections import deque
import numpy


def load_file(fname):
    with open(fname) as fh:
        return fh.readlines()


def parse_content(content):
    return [[int(c) for c in line.strip()] for line in content]


def neighbour_connections(i, j, rows, cols):
    if i > 0:
        yield i - 1, j
    if j > 0:
        yield i, j - 1
    if i < rows - 1:
        yield i + 1, j
    if j < cols - 1:
        yield i, j + 1


def find_lowpoints(grid):
    lowpoints = {}
    rows = len(grid)
    cols = len(grid[0])
    for i, j in itertools.product(range(rows), range(cols)):
        cell = grid[i][j]
        is_lowpoint = True
        for i_n, j_n in neighbour_connections(i, j, rows, cols):
            if cell >= grid[i_n][j_n]:
                is_lowpoint = False
                break

        if is_lowpoint:
            lowpoints[(i, j)] = cell
    return lowpoints


def find_basins(grid, lowpoints):
    basins = []
    rows = len(grid)
    cols = len(grid[0])
    for i, j in lowpoints.keys():
        basin = {(i, j): grid[i][j]}
        visited = [(i, j)]
        cells_to_visit = deque()
        cells_to_visit.extend(list(neighbour_connections(i, j, rows, cols)))

        while cells_to_visit:
            x, y = cells_to_visit.pop()
            visited.append((x, y))
            value = grid[x][y]
            if value < 9:
                basin[(x, y)] = value
                neighbour_cells = neighbour_connections(x, y, rows, cols)
                cells_to_visit.extend([c for c in neighbour_cells if c not in visited])
        basins.append(basin)
    return basins


test_data = """2199943210
3987894921
9856789892
8767896789
9899965678"""

test_data = test_data.split("\n")
test_data = parse_content(test_data)

points = find_lowpoints(test_data)
assert sum([v + 1 for v in points.values()]) == 15

basins = find_basins(test_data, points)

data = load_file("input.txt")
data = parse_content(data)

points = find_lowpoints(data)
print(sum([v + 1 for v in points.values()]))

basins = find_basins(data, points)
basin_sizes = [len(basin.values()) for basin in basins]
basin_sizes.sort()

print(numpy.prod(basin_sizes[-3:]))
