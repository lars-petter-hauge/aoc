import unittest
from collections import Counter


def separate_input(a, b):
    instr = {}
    start, end = a[2:].split("..")
    instr[a[0]] = (int(start), int(end) + 1)
    instr[b[0]] = (int(b[2:]), int(b[2:]) + 1)
    return instr


def parsed_data(lines):
    instructions = []
    for l in lines:
        l = l.strip()
        l = l.replace(" ", "")
        a, b = l.split(",")
        if ".." in a:
            instr = separate_input(a, b)
        else:
            instr = separate_input(b, a)
        instructions.append(instr)
    return instructions


def populate_grid(instructions):
    xmin = min([k["x"][0] for k in instructions]) - 1
    xmax = max([k["x"][1] for k in instructions]) + 1
    ymin = min([k["y"][0] for k in instructions]) - 1
    ymax = max([k["y"][1] for k in instructions])

    grid = [["." for x in range(xmax - xmin)] for y in range(ymax - ymin)]

    for instr in instructions:
        for j in range(instr["y"][0] - ymin, instr["y"][1] - ymin):
            for i in range(instr["x"][0] - xmin, instr["x"][1] - xmin):
                grid[j][i] = "#"
    return grid


def print_grid(grid):
    for line in grid:
        print("".join(line))


def read_input(fname):
    with open(fname) as f:
        result = f.readlines()
    return result


def search_boundaries(grid, x, y):
    xl = x
    xr = x
    while grid[y][xr] != "#":
        xr += 1
        if xr == len(grid[y]):
            xr = None
            break
    while grid[y][xl - 1] != "#":
        xl -= 1
        if xl == 0:
            xl = None
            break
    return [xl, xr]


def fill_container(grid, x, y):
    """
    Takes a grid and an x, y position within the grid. Expects the position to
    be somewhere at the bottom of the container. Iterates upwards row by row,
    fills the 2D container bounded by # with ~. Any # that divides the
    container will mark a new limit. Whenever a boundary (#) is outside of the
    initial boundary, the function returns the grid and the position by the
    edge. If there are two edges, both will be announced.

    Parameters:
    grid: [[list]]
        A list of lists acting as a grid (see example for format)
    x: int
        x position in the list
    y: int
        y position in the list

    Returns:
    grid: [[list]]
        The grid now filled with ~.
    X: [list]
        List of positions at the edge. Note that the X is for visualization
        of the example and will not be in the modified grid.

    Example:
    Given the following grid input, X marks the spot

    Input:            Returns:
    ..........        ..........
    .#..#.....        .#..#|||X.
    .#..#..#..        .#..#~~#..
    .#..#..#..        .#..#~~#..
    .#.....#..        .#~~~~~#..
    .#...X.#..        .#~~~~~#..
    .#######..        .#######..

    Input:            Returns:
    ..........        ..........
    ..........        X|||||||X.
    .#.....#..        .#~~~~~#..
    .#.....#..        .#~~~~~#..
    .#.....#..        .#~~~~~#..
    .#...X.#..        .#~~~~~#..
    .#######..        .#######..
    """

    init_boundaries = search_boundaries(grid, x, y)
    edges = []
    edge_found = False

    if init_boundaries[0] is None:
        print("ohoi")
    if init_boundaries[1] is None:
        print("ohoi")
    while y > 0:
        boundaries = search_boundaries(grid, x, y)
        if boundaries[0] is None or boundaries[0] < init_boundaries[0]:
            boundaries[0] = init_boundaries[0] - 2
            edges.append([init_boundaries[0] - 2, y])
            edge_found = True

        if boundaries[1] is None or boundaries[1] > init_boundaries[1]:
            boundaries[1] = init_boundaries[1] + 2
            edges.append([init_boundaries[1] + 1, y])
            edge_found = True

        for i in range(boundaries[0], boundaries[1]):
            symbol = "|" if edge_found else "~"
            grid[y][i] = symbol

        if edge_found:
            break
        y -= 1

    return grid, edges


def water_flood(grid, x=0, y=0):
    while y < len(grid) - 1:
        cell = grid[y + 1][x]
        if cell == "#":
            # TODO investigate if we hit an egde, and if so, continue on both sides..
            grid, edges = fill_container(grid, x, y)
            for edge in edges:
                grid, y = water_flood(grid, edge[0], edge[1])
        if y >= len(grid) - 1:
            break
        grid[y + 1][x] = "|"
        y += 1
        if y > 300:
            print_grid(grid)
            print("\n\n\n\n\n\n")
            break
    return grid, y


def main():
    data = read_input("day17_input")
    instructions = parsed_data(data)
    grid = populate_grid(instructions)

    watered_grid, _ = water_flood(grid, x=9, y=0)
    flattened = [x for sub in watered_grid for x in sub]
    grid_count = Counter(flattened)
    print("total water tiles: {}".format(grid_count["|"] + grid_count["~"]))


class Test(unittest.TestCase):
    def test(self):
        data = read_input("day17_testinput")
        instructions = parsed_data(data)
        grid = populate_grid(instructions)

        watered_grid, _ = water_flood(grid, x=6, y=0)

        flattened = [x for sub in watered_grid for x in sub]
        grid_count = Counter(flattened)
        assert grid_count["|"] + grid_count["~"] == 57

    def test_fill_container_single_edge(self):
        grid = [
            [".........."],
            [".#..#....."],
            [".#..#..#.."],
            [".#..#..#.."],
            [".#.....#.."],
            [".#.....#.."],
            [".#######.."],
        ]
        grid = [[x for x in sub[0]] for sub in grid]

        result = [
            [".........."],
            [".#..#||||."],
            [".#..#~~#.."],
            [".#..#~~#.."],
            [".#~~~~~#.."],
            [".#~~~~~#.."],
            [".#######.."],
        ]
        result = [[x for x in sub[0]] for sub in result]

        grid, edges = fill_container(grid, 5, 5)
        assert len(edges) == 1
        assert edges[0][0] == 8
        assert edges[0][1] == 1
        for i, l in enumerate(grid):
            assert l == result[i]

    def test_fill_container_double_edge(self):
        grid = [
            ["..........."],
            ["..........."],
            ["..#.....#.."],
            ["..#.....#.."],
            ["..#.....#.."],
            ["..#.....#.."],
            ["..#######.."],
        ]
        grid = [[x for x in sub[0]] for sub in grid]

        result = [
            ["..........."],
            [".|||||||||."],
            ["..#~~~~~#.."],
            ["..#~~~~~#.."],
            ["..#~~~~~#.."],
            ["..#~~~~~#.."],
            ["..#######.."],
        ]
        result = [[x for x in sub[0]] for sub in result]

        grid, edges = fill_container(grid, 5, 5)
        assert len(edges) == 2
        assert edges[0][0] == 1
        assert edges[0][1] == 1
        assert edges[1][0] == 9
        assert edges[1][1] == 1
        for i, l in enumerate(grid):
            assert l == result[i]

    def test_fill_container_with_box(self):
        grid = [
            ["............."],
            ["..#.......#.."],
            ["..#.......#.."],
            ["..#..###..#.."],
            ["..#..#.#..#.."],
            ["..#..###..#.."],
            ["..#.......#.."],
            ["..#########.."],
        ]
        grid = [[x for x in sub[0]] for sub in grid]

        # not even sure how this should work..
        pass


if __name__ == "__main__":
    # unittest.main()
    main()
