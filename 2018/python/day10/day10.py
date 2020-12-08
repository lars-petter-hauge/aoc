import unittest
import string
import numpy as np
import matplotlib.pyplot as plt
from operator import itemgetter
import time


def parse_data(lines):
    parsed = []
    for line in lines:
        x = int(line[10:16])
        y = int(line[18:24])
        dx = int(line[36:38])
        dy = int(line[40:42])
        parsed.append(((x, y), (dx, dy)))
    return parsed


def read_input(fname):
    with open(fname) as f:
        data = f.readlines()
    return data


def draw(parsed):
    minimal_maxi = 1000000
    minimal_maxj = 1000000
    minimal_mini = -1000000
    minimal_minj = -1000000
    for i in range(10500):
        new = []
        for point in parsed:
            x, y = point[0]
            dx, dy = point[1]
            new.append(((x + dx, y + dy), point[1]))
        parsed = new
        coordinates = [x[0] for x in parsed]
        maxi = max(coordinates, key=itemgetter(0))[0]
        if i > 10450:
            print("second: {}".format(i))
            grid = np.zeros((300, 300))
            for p in coordinates:
                grid[p[1], p[0]] = 1
            plt.matshow(grid, cmap="Blues")
            plt.show()


if __name__ == "__main__":
    data = read_input("day10input")
    parsed = parse_data(data)
    # print(parsed)
    # import pdb; pdb.set_trace()
    draw(parsed)
