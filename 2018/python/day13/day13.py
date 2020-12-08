import unittest
import itertools
from collections import Counter
import time
import os

intersection = {
    (">", "L"): "^",
    (">", "R"): "v",
    ("<", "R"): "^",
    ("<", "L"): "v",
    ("^", "L"): "<",
    ("^", "R"): ">",
    ("v", "L"): ">",
    ("v", "R"): "<",
}

corner = {
    (">", "\\"): "v",
    ("^", "\\"): "<",
    ("<", "\\"): "^",
    ("v", "\\"): ">",
    ("v", "/"): "<",
    (">", "/"): "^",
    ("<", "/"): "v",
    ("^", "/"): ">",
}


class Train(object):
    def __init__(self, idx, path, direction):
        self.idx = idx
        self.path = path
        self.direction = direction
        self.last_intersect_dir = "R"
        self.crashed = False

    @property
    def idx(self):
        return self._idx

    @idx.setter
    def idx(self, number):
        self._idx = number

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, symbol):
        self._path = symbol

    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, direction):
        self._direction = direction

    @property
    def crashed(self):
        return self._crashed

    @crashed.setter
    def crashed(self, crashed):
        self._crashed = crashed

    def next_intersect_dir(self):
        directions = ["L", "S", "R"]
        i = directions.index(self.last_intersect_dir) + 1
        self.last_intersect_dir = directions[i % len(directions)]
        return self.last_intersect_dir

    def move(self, grid, idx):
        next_path = grid["flat_grid"][idx]
        if next_path == "\\" or next_path == "/":
            self.direction = corner[(self.direction, next_path)]

        if next_path == "+":
            turn = self.next_intersect_dir()
            if turn != "S":
                self.direction = intersection[(self.direction, turn)]

        self.idx = idx
        self.path = next_path


def read_input(fname):
    with open(fname) as f:
        result = f.readlines()
    return result


def parse_input(data):
    grid = {}
    data = [x.strip("\n") for x in data]
    grid["nx"] = len(data[0])
    grid["ny"] = len(data)
    grid["flat_grid"] = list(itertools.chain.from_iterable(data))
    return grid


def xy_from_idx(idx, nx, ny):
    y = idx // nx
    x = idx % nx
    return x, y


def idx_from_xy(x, y, nx):
    return y * nx + x


def locate_trains(grid):
    trains = []
    for i, symbol in enumerate(grid["flat_grid"]):
        if symbol in ["<", ">"]:
            trains.append(Train(i, "-", symbol))
            grid["flat_grid"][i] = "-"
        if symbol in ["v", "^"]:
            trains.append(Train(i, "|", symbol))
            grid["flat_grid"][i] = "|"
    return trains


def new_coordinates(direction, x, y):
    if direction == "<":
        x -= 1
    elif direction == ">":
        x += 1
    elif direction == "^":
        y -= 1
    elif direction == "v":
        y += 1
    return x, y


def identify_crashes(trains):
    positions = Counter([t.idx for t in trains if t.crashed == False])
    crashed_idx = [idx for idx, count in positions.items() if count > 1]

    for t in trains:
        if t.idx in crashed_idx:
            # print("Setting Crashed to True for train: {}".format(t.idx))
            t.crashed = True

    return set(crashed_idx)


def move_trains(grid, trains):
    nx = grid["nx"]
    ny = grid["ny"]
    crashes = []
    for train in trains:
        avail_trains = [t for t in trains if t.crashed == False]
        if len(avail_trains) == 1:
            break
        # print("Moving train in idx: {}".format(train.idx))
        # print("Current direction: {}".format(train.direction))
        if train.crashed == True:
            continue

        x, y = xy_from_idx(train.idx, nx, ny)
        x, y = new_coordinates(train.direction, x, y)

        idx = idx_from_xy(x, y, nx)
        # print("train moved to idx: {}".format(idx))

        train.move(grid, idx)
        # print("New dir: {}".format(train.direction))

        crashed = identify_crashes(trains)
        if crashed:
            assert len(crashed) == 1
            assert list(crashed)[0] == idx
            crashes.append((x, y))

    return crashes


def print_grid(grid, trains):
    assert len(grid["flat_grid"]) == grid["ny"] * grid["nx"]
    flat_grid = grid["flat_grid"].copy()
    time.sleep(1)
    os.system("clear")
    for train in trains:
        if train.crashed == False:
            flat_grid[train.idx] = train.direction
    for i in range(grid["ny"]):
        start = i * grid["nx"]
        stop = i * grid["nx"] + grid["nx"]
        line = "".join(flat_grid[start:stop])
        print(line)


class Test(unittest.TestCase):
    def test(self):
        data = read_input("day13_testinput")
        grid = parse_input(data)
        trains = locate_trains(grid)
        indexes = [x.idx for x in trains]
        assert indexes == [2, 48]
        crashes = []
        i = 0
        while [t for t in trains if t.crashed == False]:
            crashed = move_trains(grid, trains)
            if crashed:
                crashed = [(i, x, y) for x, y in crashed]
                crashes.extend(crashed)
            print_grid(grid, trains)
        _, x, y = crashes[0]
        assert (x, y) == (7, 3)

    # def test_jpb(self):
    #    data = read_input('day13_jpb_input')
    #    # Iterasjoner 30 siste posisjon (6, 2)
    #    grid = parse_input(data)
    #    trains = locate_trains(grid)
    #    crashes = []
    #    i = 0
    #    while [t for t in trains if t.crashed == False]:
    #        crashed = move_trains(grid, trains)
    #        if crashed:
    #            crashed = [(i,x,y) for x,y in crashed]
    #            crashes.extend(crashed)
    #        #print_grid(grid, trains)
    #        if i >35:
    #            print ("Remaining trains: {}".format(len([t for t in trains if t.crashed == False])))
    #            break
    #        i+=1

    #    _, x, y = crashes[-1]
    #    print(crashes)
    #    assert (x,y) == (6,2)


def main():
    data = read_input("day13input")
    # data = read_input('day13birkeland')
    grid = parse_input(data)
    all_trains = locate_trains(grid)
    crashes = []
    i = 0
    trains = all_trains.copy()
    while trains:
        trains = [t for t in trains if t.crashed == False]
        if len(trains) == 1:
            break
        trains = sorted(trains, key=lambda x: x.idx)
        crashed = move_trains(grid, trains)
        if crashed:
            crashed = [(i, x, y) for x, y in crashed]
            crashes.extend(crashed)
        # print_grid(grid, trains)
    _, x, y = crashes[0]
    assert len(trains) == 1
    avail_train = trains[0]

    x, y = xy_from_idx(avail_train.idx, grid["nx"], grid["ny"])
    print(
        "available train: {}, idx: {}, x: {}, y:{}".format(
            avail_train, avail_train.idx, x, y
        )
    )
    # Answer could be off by one..


if __name__ == "__main__":
    # unittest.main()
    main()
