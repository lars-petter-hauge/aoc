TEST_INPUT = """30373
25512
65332
33549
35390"""

import itertools
import math
from collections.abc import Iterable
from functools import singledispatch

flatten = itertools.chain.from_iterable


def load_input(fname):
    with open(fname) as fh:
        return [l.strip() for l in fh.readlines()]


def rotate_grid(grid, reverse=False):
    """Rotating clockwise"""
    if reverse:
        return list(reversed([list(row) for row in zip(*grid)]))
    return [list(row) for row in zip(*reversed(grid))]


def visible_indices(grid, rotate=True):
    mask = [[False for _ in range(len(grid))] for _ in range(len(grid[0]))]
    for _ in range(4):
        # Rotating at the end.
        for i in range(0, len(grid)):
            current_height = -1
            for j in range(0, len(grid[0])):
                if grid[i][j] > current_height:
                    mask[i][j] = True
                    current_height = grid[i][j]
                elif grid[i][j] == 9:
                    break
        if not rotate:
            break
        grid = rotate_grid(grid)
        mask = rotate_grid(mask)

    return mask


@singledispatch
def indices(i, j):
    pass


@indices.register
def _(i_indices: Iterable, j_indices: int):
    for i in i_indices:
        yield i, j_indices


@indices.register
def _(i_indices: int, j_indices: Iterable):
    for j in j_indices:
        yield i_indices, j


def scenic_score(grid, i_start, j_start):
    """
    Calculates the scenic score from a starting point.


    Consider the following 5x5 grid.
    .....
    .....
    .....
    .....
    .....
    Given position
    of (2,2), this function will go through
    the following:
    ..#..
    ..#..
    ##X##
    ..#..
    ..#..
    """
    ni = len(grid)
    nj = len(grid[0])
    view_distances = []
    max_height = grid[i_start][j_start]
    for sequence in [
        (indices(reversed(range(0, max(i_start, 1))), j_start)),  # Up
        (indices(range(min(i_start + 1, ni), ni), j_start)),  # Down
        (indices(i_start, reversed(range(0, max(j_start, 1))))),  # Left
        (indices(i_start, range(min(j_start + 1, nj), nj))),  # Right
    ]:
        view_distance = 0
        for i, j in sequence:
            view_distance += 1
            if grid[i][j] >= max_height:
                break
        view_distances.append(view_distance)
    return math.prod(view_distances)


def max_scenic_score(grid):
    max_score = 0
    for i, j in itertools.product(range(len(grid)), range(len(grid[0]))):
        score = scenic_score(grid, i, j)
        if score > max_score:
            max_score = score
    return max_score


content = load_input("input.txt")
grid = [[int(c) for c in line] for line in content]

mask = visible_indices(grid)
print(sum(flatten([[1 for boolean in row if boolean] for row in mask])))
import time

start = time.time()
print(max_scenic_score(grid))
print(time.time() - start)


def test():
    orig_grid = [[int(c) for c in line] for line in TEST_INPUT.split("\n")]
    grid = [[int(c) for c in line] for line in TEST_INPUT.split("\n")]

    assert scenic_score(grid, 1, 2) == 4
    assert scenic_score(grid, 3, 2) == 8
    assert max_scenic_score(grid) == 16

    # From left
    mask = visible_indices(grid, rotate=False)
    expected_mask = [
        [True, False, False, True, False],
        [True, True, False, False, False],
        [True, False, False, False, False],
        [True, False, True, False, True],
        [True, True, False, True, False],
    ]
    assert mask == expected_mask

    # From Bottom
    grid = rotate_grid(grid)
    mask = visible_indices(grid, rotate=False)
    mask = rotate_grid(mask, reverse=True)
    expected_mask = [
        [False, False, False, False, False],
        [False, False, False, False, False],
        [True, False, False, False, False],
        [False, False, True, False, True],
        [True, True, True, True, True],
    ]
    assert mask == expected_mask

    # From Right
    grid = rotate_grid(grid)
    mask = visible_indices(grid, rotate=False)
    mask = rotate_grid(mask, reverse=True)
    mask = rotate_grid(mask, reverse=True)
    expected_mask = [
        [False, False, False, True, True],
        [False, False, True, False, True],
        [True, True, False, True, True],
        [False, False, False, False, True],
        [False, False, False, True, True],
    ]
    assert mask == expected_mask

    # From Top
    grid = rotate_grid(grid)
    mask = visible_indices(grid, rotate=False)
    mask = rotate_grid(mask)
    expected_mask = [
        [True, True, True, True, True],
        [False, True, True, False, False],
        [True, False, False, False, False],
        [False, False, False, False, True],
        [False, False, False, True, False],
    ]
    assert mask == expected_mask

    # All combinations:
    grid = rotate_grid(grid)
    assert grid == orig_grid
    mask = visible_indices(grid)
    expected_mask = [
        [True, True, True, True, True],
        [True, True, True, False, True],
        [True, True, False, True, True],
        [True, False, True, False, True],
        [True, True, True, True, True],
    ]
    assert mask == expected_mask
    assert sum(flatten([[1 for boolean in row if boolean] for row in mask])) == 21


test()
