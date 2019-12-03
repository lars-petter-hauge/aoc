import numpy as np
import copy
import pprint

def load_input(fname):
    with open(fname) as f:
        lines = f.readlines()
    return lines


def parse_input(lines):
    for line in lines:
        data = ((conf[0], int(conf[1:])) for conf in line.split(','))
        yield data


dir_map = {
    "D": (1, 0),
    "U": (-1, 0),
    "L": (0, -1),
    "R": (0, 1),
}

def create_line(start, grid, directions, value):
    stop = copy.copy(start)
    i, j = stop

    for direction, distance in directions:
        for _ in range(distance):
            i += dir_map[direction][0]
            j += dir_map[direction][1]
            content = grid[i][j]
            if content == value or content == -1:
                continue
            elif content == 0:
                grid[i][j] = value
            elif content != value:
                grid[i][j] = -1
            else:
                raise NotImplementedError


def run(fname):
    data = load_input(fname)
    size = 20000
    mid = int(size/2)

    grid = np.zeros((size, size))

    for idx, directions in enumerate(parse_input(data)):
        create_line([mid, mid], grid, directions, idx+1)
    i_indexes, j_indexes = np.where(grid == -1)
    dist = 100000

    for i, j in zip(i_indexes, j_indexes):
        dist = min(dist, (abs(mid-i) + abs(mid-j)))

    return dist



if __name__ == '__main__':
    print(run("input.txt"))
