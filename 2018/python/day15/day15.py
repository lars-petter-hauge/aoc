import unittest


def read_data(fname):
    with open(fname) as f:
        result = f.readlines()
    return result


def parse_data(lines):
    return [[x for x in sub.strip()] for sub in lines]


def bfs(graph):
    pass


def idx_from_point(i, j, ni):
    return ni * j + i


def create_graph(grid):
    k = -1
    graph = {}
    for j in range(len(grid)):
        for i in range(len(grid[0])):
            k += 1
            if grid[j][i] != ".":
                continue
            neighbours = []
            ni = len(grid[0])
            # Checking neighbours, this really could get a facelift..
            if i != 0 and grid[j][i - 1] == ".":
                neighbours.append(idx_from_point(i - 1, j, ni))
            if i != len(grid[0]) and grid[j][i + 1] == ".":
                neighbours.append(idx_from_point(i + 1, j, ni))
            if j != 0 and grid[j - 1][i] == ".":
                neighbours.append(idx_from_point(i, j - 1, ni))
            if j != len(grid) and grid[j + 1][i] == ".":
                neighbours.append(idx_from_point(i, j + 1, ni))
            graph[k] = set(neighbours)
    return graph


class Test(unittest.TestCase):
    def test(self):
        data = [
            "#######",
            "#.G...#",
            "#...EG#",
            "#.#.#G#",
            "#..G#E#",
            "#.....#",
            "#######",
        ]
        grid = parse_data(data)
        graph = create_graph(grid)
        print(graph)


if __name__ == "__main__":
    data = read_data("day15_input.txt")
    unittest.main()
