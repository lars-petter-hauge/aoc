from statistics import geometric_mean
from collections import deque

from scipy.stats.mstats import gmean
import numpy as np


def load_content(fname):
    with open(fname) as fh:
        return fh.readlines()


def parse_content(lines):
    content = lines[0].strip()
    return [int(c) for c in content.split(",")]


def euclidean_distance(point, points):
    return (sum([(point - p) ** 2 for p in points])) ** 1 / 2


def geometric_median(points):
    arr = np.array(points)
    return arr.prod() ** (1 / len(arr))


def extrapolated_point(a, b):
    if a > b:
        return b - 1
    elif a < b:
        return b + 1
    else:
        raise ValueError()


def fuel_cost(point, points):
    return sum([abs(point - p) for p in points])


def fuel_cost_expo(origin, points):
    cost = 0
    for point in points:
        cost += sum(range(int(abs(point - origin)) + 1))
    return cost


def center_of_mass(points, expo=False):
    best_guess = geometric_median(points)
    possibles = deque([best_guess - 1, best_guess + 1])
    if expo:
        cost_func = fuel_cost_expo
    else:
        cost_func = fuel_cost
    min_fuel_cost = cost_func(best_guess, points)
    while len(possibles):
        next_guess = possibles.pop()
        next_fuel_cost = cost_func(next_guess, points)
        if next_fuel_cost < min_fuel_cost:
            possibles.append(extrapolated_point(best_guess, next_guess))
            best_guess = next_guess
            min_fuel_cost = next_fuel_cost

    return (best_guess, min_fuel_cost)


def center_of_mass_two(points):
    min_fuel_cost = fuel_cost(points[0], points)
    best_pos = points[0]
    for p in points:
        current_fuel_cost = fuel_cost(p, points)
        if current_fuel_cost <= min_fuel_cost:
            min_fuel_cost = current_fuel_cost
            best_pos = p
        else:
            break
    return best_pos, min_fuel_cost


test_data = [16, 1, 2, 0, 4, 2, 7, 1, 2, 14]

print(center_of_mass(test_data, expo=True))

data = load_content("input.txt")
data = [int(c) for c in data[0].strip().split(",")]
data.sort()

print(center_of_mass_two(data))
print(center_of_mass(data))
print(center_of_mass(data, expo=True))