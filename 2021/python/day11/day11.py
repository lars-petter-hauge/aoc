import itertools
import copy


def load_content(fname):
    with open(fname) as fh:
        return fh.readlines()


def print_grid(grid):
    print("\n".join("\t".join(str(c) for c in cells) for cells in grid))
    print("\n")


def neighbour_connections(i, j, rows, cols):
    if i > 0:
        yield i - 1, j
    if j > 0:
        yield i, j - 1
    if i < rows - 1:
        yield i + 1, j
    if j < cols - 1:
        yield i, j + 1
    if i > 0 and j > 0:
        yield i - 1, j - 1
    if i > 0 and j < cols - 1:
        yield i - 1, j + 1
    if i < rows - 1 and j > 0:
        yield i + 1, j - 1
    if i < rows - 1 and j < cols - 1:
        yield i + 1, j + 1


def flash_octopus(grid, flashed):
    rows = len(grid)
    cols = len(grid[0])
    len_prev_flashed = len(flashed)
    for i, j in itertools.product(range(rows), range(cols)):
        if grid[i][j] > 9:
            flashed.append((i, j))
            grid[i][j] = 0
            for i_n, j_n in neighbour_connections(i, j, rows, cols):
                if (i_n, j_n) not in flashed:
                    grid[i_n][j_n] += 1
    return len(flashed) != len_prev_flashed


def simulate_octopus(grid, days=2):
    grid = copy.deepcopy(grid)
    rows = len(grid)
    cols = len(grid[0])
    number_of_flashes = 0
    for day in range(days):
        # print_grid(grid)
        flashed = []
        for i, j in itertools.product(range(rows), range(cols)):
            grid[i][j] += 1

        while True:
            any_flashed = flash_octopus(grid, flashed)
            if not any_flashed:
                break
        if len(flashed) == rows * cols:
            print(f"All flashed on day {day+1}")
        number_of_flashes += len(flashed)
    return number_of_flashes


def grid_from_string(string):
    grid = [l.strip() for l in string.split()]
    return [[int(c) for c in line] for line in grid]


TEST_DATA = """5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526"""

TEST_DATA_SMALL = """11111
19991
19191
19991
11111"""

PUZZLE_INPUT = """6227618536
2368158384
5385414113
4556757523
6746486724
4881323884
4648263744
4871332872
4724128228
4316512167"""

grid = grid_from_string(TEST_DATA)
assert simulate_octopus(grid, days=10) == 204
assert simulate_octopus(grid, days=100) == 1656

grid = grid_from_string(PUZZLE_INPUT)
print(simulate_octopus(grid, days=10000))