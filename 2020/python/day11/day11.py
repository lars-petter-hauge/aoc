import itertools
import copy

TEST_DATA = """L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL"""

TEST_EYESIGHT_ONE_OC = """.............
.L.L.#.#.#.#.
............."""


TEST_EYESIGHT_NO_OC = """.##.##.
#.#.#.#
##...##
...L...
##...##
#.#.#.#
.##.##."""

TEST_EYESIGHT_EIGHT_OC = """.......#.
...#.....
.#.......
.........
..#L....#
....#....
.........
#........
...#....."""

def parse(lines):
    return [[x for x in l] for l in lines]


def load(fname):
    with open(fname) as fh:
        lines = fh.readlines()
    lines = [l.strip() for l in lines]
    return lines

def out_of_bounds(seating, i, j):
    if 0 > i or i >= len(seating[0]):
        return True
    if 0 > j or j >= len(seating):
        return True
    return False

def n_adjacent_occupied(seating, col, row):
    occupied_seats = 0
    for j, i in itertools.product(range(row - 1, row + 2), range(col - 1, col + 2)):
        if j == row and i == col:
            continue
        if out_of_bounds(seating, i, j):
            continue

        if seating[j][i] == "#":
            occupied_seats += 1

    return occupied_seats


def increment(direction, i, j):
    if direction == "N":
        return i, j-1
    elif direction == "NE":
        return i+1, j-1
    elif direction == "E":
        return i+1, j
    elif direction == "SE":
        return i+1, j+1
    elif direction == "S":
        return i, j+1
    elif direction == "SW":
        return i-1, j+1
    elif direction == "W":
        return i-1, j
    elif direction == "NW":
        return i-1, j-1
    raise NotImplementedError("Not a direction")


def n_eyesight_occupied(seating, col, row):
    occupied_seats = 0
    for direction in ["N", "S", "W", "E", "NE", "SE", "NW", "SW"]:
        i, j = col, row
        while True:
            i, j = increment(direction, i, j)
            if out_of_bounds(seating, i, j) or seating[j][i] == "L":
                break

            if seating[j][i] == "#":
                occupied_seats += 1
                break

    return occupied_seats

def step(seating, count_occupied_func, max_occupied_seats):
    old_seating = copy.deepcopy(seating)
    for j, i in itertools.product(range(len(seating)), range(len(seating[0]))):
        if old_seating[j][i] == "L":
            if count_occupied_func(old_seating, col=i, row=j) == 0:
                seating[j][i] = "#"
        if old_seating[j][i] == "#":
            if count_occupied_func(old_seating, col=i, row=j) >= max_occupied_seats:
                seating[j][i] = "L"
    return seating


def count_occupied(seating):
    occupied = 0
    for j, i in itertools.product(range(len(seating)), range(len(seating[0]))):
        if seating[j][i] == "#":
            occupied += 1
    return occupied


def simulate(seating, count_occupied_func, max_occupied_seats):
    changed = True
    while changed:
        old_seating = copy.deepcopy(seating)
        seating = step(seating, count_occupied_func, max_occupied_seats)
        changed = old_seating != seating
    return seating


if __name__ == "__main__":
    import time
    start = time.time()
    seating = simulate(parse(TEST_DATA.split("\n")), count_occupied_func=n_adjacent_occupied, max_occupied_seats=4)
    assert count_occupied(seating) == 37
    seating = simulate(parse(load("2020/python/day11/input.txt")), count_occupied_func=n_adjacent_occupied, max_occupied_seats=4)
    assert count_occupied(seating) == 2275

    assert n_eyesight_occupied(parse(TEST_EYESIGHT_NO_OC.split("\n")), row=3, col=3) == 0
    assert n_eyesight_occupied(parse(TEST_EYESIGHT_EIGHT_OC.split("\n")), row=4, col=3) == 8
    assert n_eyesight_occupied(parse(TEST_EYESIGHT_ONE_OC.split("\n")), row=1, col=3) == 1

    seating = simulate(parse(TEST_DATA.split("\n")), count_occupied_func=n_eyesight_occupied, max_occupied_seats=5)
    assert count_occupied(seating) == 26

    seating = simulate(parse(load("2020/python/day11/input.txt")), count_occupied_func=n_eyesight_occupied, max_occupied_seats=5)
    print(count_occupied(seating))
    print(time.time()-start)