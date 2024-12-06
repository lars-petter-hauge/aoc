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


def parse_line(lines):
    obstructions = []
    guard = None
    for i, line in enumerate(lines):

        for idx, char in enumerate(line):
            if char == "#":
                obstructions.append((i, idx))
            if char == "^":
                guard = (i, idx)
    return guard, obstructions


DIR = [(0, 1), (0, -1), (1, 0), (-1, 0)]
direction = DIR[0]
while True:
    if direction[0] != 0:
        if direction[0] < 0:
            pass
        else:
            pass
    else:
        if direction[1] < 0:
            pass
        else:
            pass


content = parse_line(TEST_INPUT.split("\n"))
