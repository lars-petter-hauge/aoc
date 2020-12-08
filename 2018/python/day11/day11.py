import unittest
import numpy as np
import time


def power(serial, x, y):
    rack_id = x + 10
    pwr_lvl = rack_id * y
    pwr_lvl = pwr_lvl + serial
    pwr_lvl = pwr_lvl * rack_id
    pwr_lvl = pwr_lvl // 100 % 10
    pwr_lvl = pwr_lvl - 5
    return pwr_lvl


def populate_grid(serial):
    grid = np.zeros((300, 300))
    for i in range(300):
        for j in range(300):
            grid[i][j] = power(serial, i + 1, j + 1)
    return grid


def max_region(grid, size):
    max_power = (0, 0, 0)

    for i in range(0, 300 - size):
        for j in range(0, 300 - size):
            pwr = grid[i : i + size, j : j + size].sum()
            if pwr > max_power[0]:
                max_power = (pwr, i, j)
    return max_power


def max_region_any_size(grid, max_size=None):
    max_power_region = (0, 0, 0, 0)
    max_size = max_size or 299
    start = time.time()
    last_round = time.time()
    for i in range(5, max_size):
        pwr, x, y = max_region(grid, i)
        if pwr > max_power_region[0]:
            max_power_region = (pwr, x, y, i)
        print(
            "checked size: {}, took: {}, total elapsed: {}".format(
                i, time.time() - last_round, time.time() - start
            )
        )
        last_round = time.time()
    print("all in all: {} minutes".format((time.time() - start) / 60))
    return max_power_region


class Test(unittest.TestCase):
    def test_power(self):
        assert power(57, 122, 79) == -5
        assert power(39, 217, 196) == 0
        assert power(71, 101, 153) == 4

    def test_pop_grid(self):
        grid = populate_grid(18)
        assert False
        assert grid[32][44] == 4
        assert max_region(grid, 3) == (29, 32, 44)

        grid2 = populate_grid(42)
        assert max_region(grid2, 3) == (30, 20, 60)

        assert max_region_any_size(grid, 20) == (113, 89, 268, 16)


if __name__ == "__main__":
    # unittest.main()
    grid = populate_grid(9005)
    print(max_region_any_size(grid))
