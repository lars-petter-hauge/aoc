TEST_INPUT = """498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9"""
import time
from collections import deque


def parse_lines(lines):
    rocks = []
    for line in lines:
        coordinates = [coor.strip() for coor in line.split("->")]
        for start, end in zip(coordinates, coordinates[1:]):
            x1, y1 = start.split(",")
            x2, y2 = end.split(",")
            x1, x2, y1, y2 = map(int, [x1, x2, y1, y2])
            if x2 < x1:
                x1, x2 = x2, x1
            if y2 < y1:
                y1, y2 = y2, y1
            if x1 == x2:
                y_coords = range(int(y1), int(y2) + 1)
                x_coords = len(y_coords) * [int(x1)]
            else:
                x_coords = range(int(x1), int(x2) + 1)
                y_coords = len(x_coords) * [int(y1)]

            rocks.extend(zip(y_coords, x_coords))
    return rocks


def load_input(fname):
    with open(fname) as fh:
        return fh.readlines()


def possible_new_coords(coord):
    depth, width = coord
    possible_pos = [
        [
            depth + 1,
            width,
        ],
        [
            depth + 1,
            width - 1,
        ],
        [
            depth + 1,
            width + 1,
        ],
    ]
    return possible_pos


def apply_offset(coordinates, leftpad):
    offset = sorted(coordinates, key=lambda x: x[1])[0][1]
    offset -= leftpad
    result = []
    for i, j in coordinates:
        result.append([i, j - offset])
    return result


def print_grid(grid):
    print("\n".join(["".join(row) for row in grid]))


def simulate(rock_coords, starting_pos=500, fill_floor=False):
    sorted_by_width = sorted(rock_coords, key=lambda x: x[1])
    nx = max(sorted_by_width[-1][1] + 2, starting_pos * 2)
    max_depth = sorted(rock_coords)[-1][0]
    if fill_floor:
        max_depth += 1
    sand_coords = []
    grid = [["." for _ in range(nx + 1)] for _ in range(max_depth + 3)]
    previous_positions = deque()
    previous_positions.append([0, starting_pos])
    for i, j in rock_coordinates:
        grid[i][j] = "#"
    try:
        while True:
            if len(previous_positions) == 0:
                raise StopIteration

            next_pos = previous_positions.pop()

            sand_coord = None
            while sand_coord is None:
                valid_positions = [
                    pos
                    for pos in possible_new_coords(next_pos)
                    if pos not in rock_coords and pos not in sand_coords
                ]
                if fill_floor:
                    valid_positions = [
                        pos for pos in valid_positions if pos[0] <= max_depth
                    ]
                if valid_positions:
                    previous_positions.append(next_pos)
                    next_pos = valid_positions[0]
                else:
                    sand_coord = next_pos

                if next_pos[0] > max_depth and not fill_floor:
                    raise StopIteration

            # grid[next_pos[0]][next_pos[1]] = "o"
            # print_grid(grid)
            # time.sleep(0.1)
            print(f"Current depth: {next_pos[0]}, max_depth: {max_depth}")
            sand_coords.append(next_pos)
    except StopIteration:
        pass

    return sand_coords


rock_coordinates = parse_lines(TEST_INPUT.split("\n"))
min_width = sorted(rock_coordinates, key=lambda x: x[1])[0][1]
leftpad = 6
rock_coordinates = apply_offset(rock_coordinates, leftpad=leftpad)

assert len(simulate(rock_coordinates, starting_pos=500 - min_width + leftpad)) == 24
assert (
    len(
        simulate(
            rock_coordinates, starting_pos=500 - min_width + leftpad, fill_floor=True
        )
    )
    == 93
)

rock_coordinates = parse_lines(load_input("input.txt"))
min_width = sorted(rock_coordinates, key=lambda x: x[1])[0][1]
rock_coordinates = apply_offset(rock_coordinates, leftpad=leftpad)

sand_coords = simulate(
    rock_coordinates, starting_pos=500 - min_width + leftpad, fill_floor=True
)
print(len(sand_coords))
