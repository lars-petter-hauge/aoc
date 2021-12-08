import copy
from collections import deque
import networkx as nx

TEST_DATA = """16
10
15
5
1
11
7
19
6
12
4"""

TEST_DATA_TWO = """28
33
18
42
31
14
46
20
48
47
24
23
49
45
19
38
39
11
1
32
25
35
8
17
7
9
4
2
34
10
3"""

EXPECTED_TEST_DATA = [
    [0, 1, 4, 5, 6, 7, 10, 11, 12, 15, 16, 19, 22],
    [0, 1, 4, 5, 6, 7, 10, 12, 15, 16, 19, 22],
    [0, 1, 4, 5, 7, 10, 11, 12, 15, 16, 19, 22],
    [0, 1, 4, 5, 7, 10, 12, 15, 16, 19, 22],
    [0, 1, 4, 6, 7, 10, 11, 12, 15, 16, 19, 22],
    [0, 1, 4, 6, 7, 10, 12, 15, 16, 19, 22],
    [0, 1, 4, 7, 10, 11, 12, 15, 16, 19, 22],
    [0, 1, 4, 7, 10, 12, 15, 16, 19, 22],
]


def parse(lines):
    return [int(x) for x in lines]


def load(fname):
    with open(fname) as fh:
        lines = fh.readlines()
    return lines


def valid_adapters(adapter_values, current):
    return [a for a in adapter_values if current < a <= current + 3]


def count_ones_and_threes(adapter_values):
    queue = deque(adapter_values)
    ones, threes = 0, 0

    old_adapter = 0
    while queue:
        adapter = queue.popleft()
        if adapter - old_adapter == 1:
            ones += 1
        if adapter - old_adapter == 3:
            threes += 1
        old_adapter = adapter

    return ones, threes


def run(adapter_values):
    device_voltage = max(adapter_values) + 3
    adapter_values.extend([device_voltage])
    adapter_values = sorted(adapter_values)
    ones, threes = count_ones_and_threes(adapter_values)
    return ones * threes


def bfs(graph, start, stop):
    queue = deque()
    queue.append(start)
    seen = set()
    path = []

    while queue:
        parent = queue.popleft()
        if parent == stop:
            break

        seen.add(parent)
        for child in graph[parent]:
            queue.append(child)

    return path


def day_two(adapter_values):
    device_voltage = max(adapter_values) + 3
    adapter_values.extend([0, device_voltage])
    graph = generate_graph(adapter_values)
    g = nx.DiGraph(graph)

    return nx.all_simple_paths(g, 0, device_voltage)


def generate_graph(data):
    graph = {}
    for value in data:
        graph[value] = valid_adapters(data, value)
    return graph


if __name__ == "__main__":
    assert run(parse(TEST_DATA.split("\n"))) == 5 * 7
    assert run(parse(TEST_DATA_TWO.split("\n"))) == 22 * 10

    print(len(list(day_two(parse(TEST_DATA_TWO.split("\n"))))))
    print(run(parse(load("2020/python/day10/input.txt"))))
    n_path = 0
    for _ in day_two(parse(load("2020/python/day10/input.txt"))):
        n_path += 1
    print(n_path)
