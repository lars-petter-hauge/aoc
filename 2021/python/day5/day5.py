from itertools import chain
from collections import Counter

flatten = chain.from_iterable


def load_data(fname):
    with open(fname) as fh:
        return [l.strip() for l in fh.readlines()]


def string_point_to_int(str):
    x, y = str.split(",")
    return int(x.strip()), int(y.strip())


def parse_lines(lines):
    points = []
    for line in lines:
        start, stop = line.split("->")
        points.append((string_point_to_int(start), string_point_to_int(stop)))
    return points


def points_on_line(start, stop, diag=False):
    x1, y1 = start
    x2, y2 = stop
    ystep = 1
    xstep = 1
    points = None
    if y2 < y1:
        ystep = -1
    if x2 < x1:
        xstep = -1

    if x1 == x2:
        points = [(x1, y) for y in range(y1, y2 + ystep, ystep)]
    if y1 == y2:
        points = [(x, y1) for x in range(x1, x2 + xstep, xstep)]
    if diag:
        if abs(x2 - x1) == abs(y2 - y1):
            points = [
                (x, y)
                for x, y in zip(
                    range(x1, x2 + xstep, xstep), range(y1, y2 + ystep, ystep)
                )
            ]
    return points


def run(fname, diag=False):
    lines = load_data(fname)
    points = parse_lines(lines)
    points_from_lines = [
        points_on_line(start, stop, diag=diag) for start, stop in points
    ]
    points_from_lines = [p for p in points_from_lines if p is not None]
    points_from_lines = list(flatten(points_from_lines))
    counter = Counter(points_from_lines)
    double_covered = [p for p, n in counter.items() if n > 1]
    return len(double_covered)


assert run("test_input.txt") == 5
assert run("test_input.txt", diag=True) == 12

assert run("input.txt") == 4655
assert run("input.txt", diag=True) == 20500
