from pathlib import Path

TEST_INPUT = """....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#..."""


def load():
    with open(Path(__file__).parent / "input.in") as fh:
        lines = fh.readlines()
    return lines


def solve(grid):

    NR = len(grid)
    NC = len(grid[0])
    print(NR, NC)
    guard = [0, 0]
    for r in range(NR):
        for c in range(NC):
            if grid[r][c] == "^":
                guard = (r, c)

    DIR = [(-1, 0), (0, 1), (1, 0), (0, -1)]

    visited = set([guard])

    direction = DIR[0]
    while True:
        dr = guard[0] + direction[0]
        dc = guard[1] + direction[1]
        if dr >=NR or dc>=NC or dc<0 or dr < 0:
            break
        if grid[dr][dc] == "#":
            direction = DIR[(DIR.index(direction)+1)%len(DIR)]
            continue
        guard = (dr,dc)
        visited.update(set([guard]))

    return visited


print(len(solve(TEST_INPUT.split("\n"))))
print(len(solve(load())))
