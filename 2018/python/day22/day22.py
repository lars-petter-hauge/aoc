import unittest


def erosion(i, j, grid, depth, target):
    if grid[i][j] <= 0:
        return (geo_index(i, j, grid, depth, target) + depth) % 20183
    return (grid[i][j] + depth) % 20183


def geo_index(i, j, grid, depth, target=(0, 0)):
    if i == 0 and j == 0:
        return 0
    if i == target[1] and j == target[0]:
        return 0
    if i == 0:
        return j * 16807
    if j == 0:
        return i * 48271
    return erosion(i - 1, j, grid, depth, target) * erosion(
        i, j - 1, grid, depth, target
    )


def populate_geo(depth, target=(0, 0)):
    """
    populates a grid with geo-indexes
    """
    grid = [[-1 for i in range(target[0] + 1)] for j in range(target[1] + 1)]
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            grid[i][j] = geo_index(i, j, grid, depth, target)
    return grid


def geo_type(i, j, grid, depth, target):
    """
    Takes coordinates within a grid
    Requires a grid populated with erosion levels
    """
    return erosion(i, j, grid, depth, target) % 3


def populate_type(grid, depth, target):
    type_grid = [[-1 for i in range(len(grid[0]))] for j in range(len(grid))]
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            type_grid[i][j] = geo_type(i, j, grid, depth, target)
    return type_grid


def print_type_grid(grid):
    for i in range(len(grid)):
        line = []
        for j in range(len(grid[0])):
            if grid[i][j] == 0:
                line.append(".")
            elif grid[i][j] == 1:
                line.append("=")
            elif grid[i][j] == 2:
                line.append("|")
            else:
                raise NotImplementedError
        print("".join(line))


def assess_risk(grid):
    risk = 0
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            risk += grid[i][j]
    return risk


def main(depth, target):
    print("populating geomodel")
    geo_grid = populate_geo(depth, target)
    print("populating type grid")
    type_grid = populate_type(geo_grid, depth, target)
    print("assessing grid")
    print(assess_risk(type_grid))


class Test(unittest.TestCase):
    def test(self):
        geo_grid = populate_geo(510, (10, 10))
        type_grid = populate_type(geo_grid, 510, (10, 10))
        print_type_grid(type_grid)
        print(assess_risk(type_grid))
        assert assess_risk(type_grid) == 114


if __name__ == "__main__":
    # unittest.main()
    main(3066, (13, 726))
