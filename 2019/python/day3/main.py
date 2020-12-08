import numpy as np
import copy
import pprint


def load_input(fname):
    with open(fname) as f:
        lines = f.readlines()
    return lines


def parse_input(lines):
    for line in lines:
        data = ((conf[0], int(conf[1:])) for conf in line.split(","))
        yield data


dir_map = {
    "D": (1, 0),
    "U": (-1, 0),
    "L": (0, -1),
    "R": (0, 1),
}


def distance_to_points(directions):
    i, j = 0, 0
    distance_point = {}
    total_distance = 0

    for direction, distance in directions:
        for _ in range(distance):
            i += dir_map[direction][0]
            j += dir_map[direction][1]
            total_distance += 1
            if (i, j) not in distance_point:
                distance_point[(i, j)] = total_distance
    return distance_point


def run(fname):
    data = load_input(fname)

    distances = []
    for directions in parse_input(data):
        distance = distance_to_points(directions)
        distances.append(distance)

    intersections = set(distances[0].keys()).intersection(set(distances[1].keys()))
    path = 100000
    dist = 100000
    for (i, j) in intersections:
        path = min(path, distances[0][(i, j)] + distances[1][(i, j)])
        dist = min(dist, (abs(i) + abs(j)))

    return dist, path


if __name__ == "__main__":
    dist, pathlength = run("day3/input.txt")
    print("distance: {}, length: {}".format(dist, pathlength))
