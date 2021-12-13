import numpy as np
import itertools


def load_content(fname):
    with open(fname) as fh:
        return fh.read()


def parse_content(content):
    coord_cont, fold_cont = content.split("\n\n")
    return parse_coords(coord_cont.split("\n")), parse_fold(fold_cont.split("\n"))


def parse_coords(lines):
    coords = []
    for line in lines:
        x, y = line.split(",")
        coords.append((int(x), int(y)))
    return coords


def parse_fold(lines):
    folds = []
    for line in lines:
        axis_info = line.split(" ")[-1]
        axis, n = axis_info.split("=")
        folds.append((axis, int(n)))
    return folds


def create_grid(coords):
    max_x = max([x for x, _ in coords]) + 1
    max_y = max([y for _, y in coords]) + 1
    grid = np.zeros((max_x, max_y))
    for x, y in coords:
        grid[x][y] = 1
    return grid


def fold_grid(grid, axis, n):
    if axis == "y":
        grid = grid[0:n, :] + np.flipud(grid[n + 1 :, :])
    if axis == "x":
        grid = grid[:, 0:n] + np.fliplr(grid[:, n + 1 :])
    return grid


TEST_DATA = """6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5"""

content = load_content("input.txt")
coords, folds = parse_content(content)

grid = create_grid(coords)
grid = grid.transpose()

for axis, n in folds:
    grid = fold_grid(grid, axis, n)

nx, ny = grid.shape
for i, j in itertools.product(range(nx), range(ny)):
    if grid[i][j] > 1:
        grid[i][j] = 1
print(grid)
