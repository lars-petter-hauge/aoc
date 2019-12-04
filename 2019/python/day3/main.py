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
    distance_point = {}

    total_distance = 0
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
            total_distance += 1
            if (i,j) not in distance_point:
                distance_point[(i,j)] = total_distance
    return distance_point


def run(fname):
    data = load_input(fname)
    size = 20000
    mid = int(size/2)

    grid = np.zeros((size, size))
    distances = []
    for idx, directions in enumerate(parse_input(data)):
        distance = create_line([mid, mid], grid, directions, idx+1)
        distances.append(distance)

    intersections = set(distances[0].keys()).intersection(set(distances[1].keys()))
    path = 100000
    for intersection in intersections:
        path = min(path, distances[0][intersection] + distances[1][intersection])

    i_indexes, j_indexes = np.where(grid == -1)
    dist = 100000

    for i, j in zip(i_indexes, j_indexes):
        dist = min(dist, (abs(mid-i) + abs(mid-j)))
        assert (i,j) in intersections

    return dist, path


if __name__ == '__main__':
    dist, pathlength = run("input.txt")
    print("distance: {}, length: {}".format(dist, pathlength))
    # 14740 too low
