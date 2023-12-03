from aoc_tools.grid import neighbour_indices, grid_indices
import numpy as np
import math

TEST_INPUT = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598.."""


def load_input(fname):
    with open(fname) as fh:
        return fh.readlines()


def is_special_symbol(symbol):
    if symbol == ".":
        return False
    if symbol.isnumeric():
        return False
    return True


def part_one(grid):
    seen = set()
    numbers_indices = []
    # Not a very elegant way to solve this day..

    # Loop through grid and find all collection of indices that contains a number
    for row, col in grid_indices(grid):
        if (row, col) in seen:
            continue
        if grid[row][col].isnumeric():
            end_col = col
            while end_col < grid.shape[1] and grid[row][end_col].isnumeric():
                end_col += 1
            number_indices = [(row, val) for val in range(col, end_col)]
            numbers_indices.append(number_indices)
            seen.update(number_indices)
    # Loop through the collection of indices with numbers and validate
    # all that has a special symbol as neighbour
    valid_number_indices = []
    for number_indices in numbers_indices:
        for row, col in number_indices:
            if any(
                [
                    is_special_symbol(grid[i][j])
                    for i, j in neighbour_indices(
                        row, col, grid.shape[0], grid.shape[1]
                    )
                ]
            ):
                valid_number_indices.append(number_indices)
                break
    # Loop through all valid sets of indices to get the number
    values = []
    for indices in valid_number_indices:
        numbah = "".join([str(grid[row][col]) for row, col in indices])
        values.append(int(numbah))
    # Finally sum the numbers.
    return sum(values)


def part_two(grid):
    seen = set()
    numbers_indices = []
    for row, col in grid_indices(grid):
        if (row, col) in seen:
            continue
        if grid[row][col].isnumeric():
            end_col = col
            while end_col < grid.shape[1] and grid[row][end_col].isnumeric():
                end_col += 1
            number_indices = [(row, val) for val in range(col, end_col)]
            numbers_indices.append(number_indices)
            seen.update(number_indices)

    gear_ratio = []
    for row, col in grid_indices(grid):
        if grid[row][col] != "*":
            continue
        surrounding_indices = []
        for i, j in neighbour_indices(row, col, grid.shape[0], grid.shape[1]):
            for indices in numbers_indices:
                if (i, j) in indices:
                    if indices not in surrounding_indices:
                        surrounding_indices.append(indices)
                    break
        values = []
        if len(surrounding_indices) == 2:
            for indices in surrounding_indices:
                numbah = "".join([str(grid[row][col]) for row, col in indices])
                values.append(int(numbah))
            gear_ratio.append(math.prod(values))
    return sum(gear_ratio)


grid = np.asarray([[c for c in line.strip()] for line in TEST_INPUT.split("\n")])
print(part_one(grid))
print(part_two(grid))

grid = np.asarray([[c for c in line.strip()] for line in load_input("input.txt")])
print(part_one(grid))
print(part_two(grid))
