import itertools
import numpy as np
import copy

TEST_DATA = """.#.
..#
###"""

TASK_INPUT = """#......#
##.#..#.
#.#.###.
.##.....
.##.#...
##.#....
#####.#.
##.#.###"""


def neighbour_cells(i, j, k, grid):
    xs = [i - 1, i, i + 1]
    ys = [j - 1, j, j + 1]
    zs = [k - 1, k, k + 1]

    for x, y, z in itertools.product(xs, ys, zs):
        if x < 0 or j < 0 or k < 0:
            continue
        if x == i and j == y and k == z:
            continue
        if x >= grid.shape[2] - 1 or y >= grid.shape[1] - 1 or k >= grid.shape[0] - 1:
            continue
        yield grid[z][y][x]


def neighbour_cells_4D(i, j, k, l, grid):
    xs = [i - 1, i, i + 1]
    ys = [j - 1, j, j + 1]
    zs = [k - 1, k, k + 1]
    ws = [l - 1, l, l + 1]

    for x, y, z, w in itertools.product(xs, ys, zs, ws):
        if x < 0 or j < 0 or k < 0 or w < 0:
            continue
        if x == i and j == y and k == z and w == l:
            continue
        if (
            x >= grid.shape[3] - 1
            or y >= grid.shape[2] - 1
            or k >= grid.shape[1] - 1
            or l >= grid.shape[0] - 1
        ):
            continue
        yield grid[w][z][y][x]


def populate_grid_with_lines(lines, grid, start=(5, 5, 5)):
    k, j, i = start

    for l in lines:
        i = start[2]
        for symbol in l:
            if symbol == "#":
                grid[k][j][i] = 1
            i += 1
        j += 1


def populate_4D_grid_with_lines(lines, grid, start=(5, 5, 5, 5)):
    w, k, j, i = start

    for l in lines:
        i = start[3]
        for symbol in l:
            if symbol == "#":
                grid[w][k][j][i] = 1
            i += 1
        j += 1


def print_grid(grid, k=0):
    for row in grid[k]:
        print(" ".join(["#" if c == 1 else "." for c in row]))

def print_4D_grid(grid, k=0, w=0):
    for row in grid[w][k]:
        print(" ".join(["#" if c == 1 else "." for c in row]))


def simulate_step(grid):
    old_grid = copy.deepcopy(grid)
    nz, ny, nx = grid.shape

    for x, y, z in itertools.product(range(nx), range(ny), range(nz)):
        active = grid[z][y][x] == 1
        num_active_neighbours = sum(neighbour_cells(x, y, z, old_grid))

        if active and not (2 <= num_active_neighbours <= 3):
            grid[z][y][x] = 0
        if not active and num_active_neighbours == 3:
            grid[z][y][x] = 1

    return grid


def simulate_step_4D(grid):
    old_grid = copy.deepcopy(grid)
    nw, nz, ny, nx = grid.shape

    for x, y, z, w in itertools.product(range(nx), range(ny), range(nz), range(nw)):
        active = grid[w][z][y][x] == 1
        num_active_neighbours = sum(neighbour_cells_4D(x, y, z, w, old_grid))

        if active and not (2 <= num_active_neighbours <= 3):
            grid[w][z][y][x] = 0
        if not active and num_active_neighbours == 3:
            grid[w][z][y][x] = 1

    return grid


def run_simulations(grid, steps=1):
    for _ in range(steps):
        print("simulates")
        simulate_step(grid)

def run_simulations_4D(grid, steps=1):
    for _ in range(steps):
        print("simulates")
        simulate_step_4D(grid)


if __name__ == "__main__":
    grid = np.zeros(shape=(20, 20, 20))
    populate_grid_with_lines(TEST_DATA.split("\n"), grid, start=(10, 6, 6))
    # run_simulations(grid, steps=6)
    # assert np.sum(grid) == 112
    #grid = np.zeros(shape=(20, 20, 20))
    #populate_grid_with_lines(TASK_INPUT.split("\n"), grid, start=(10, 6, 6))
    #run_simulations(grid, steps=6)
    #print(np.sum(grid))
    grid = np.zeros(shape=(20, 20, 20, 20))
    populate_4D_grid_with_lines(TASK_INPUT.split("\n"), grid, start=(10, 10, 6, 6))
    run_simulations_4D(grid, steps=6)
    #1410 is too low
    print(np.sum(grid))
