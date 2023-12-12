TEST_DATA = """.....
.S-7.
.|.|.
.L-J.
....."""


def load(fname):
    with open(fname) as fh:
        return fh.readlines()


def symbol_connection(row, col, symbol):
    if symbol == "|":
        yield row - 1, col
        yield row + 1, col
    elif symbol == "F":
        yield row, col + 1
        yield row + 1, col
    elif symbol == "L":
        yield row - 1, col
        yield row, col + 1
    elif symbol == "7":
        yield row + 1, col
        yield row, col - 1
    elif symbol == "-":
        yield row, col - 1
        yield row, col + 1
    elif symbol == "J":
        yield row, col - 1
        yield row - 1, col
    else:
        raise NotImplementedError(f"Not implemented for {symbol}")


def parse_lines(lines, s_con):
    graph = {}
    start = None
    for row, line in enumerate(lines):
        for col, char in enumerate(line):
            if char == "S":
                char = s_con
                start = (row, col)
            if char == ".":
                continue
            graph[(row, col)] = list(symbol_connection(row, col, char.strip()))
    return start, graph


def run_pipe(graph, start):
    previous = start
    # just picking a direction.
    current = graph[start][0]
    i = 1
    while current != start:
        new_current = [
            neighbour for neighbour in graph[current] if neighbour != previous
        ][0]

        previous = current
        current = new_current
        i += 1
    return i / 2


start, graph = parse_lines(TEST_DATA.split("\n"), s_con="F")
print(run_pipe(graph, start))

start, graph = parse_lines([line.strip() for line in load("input.txt")], s_con="7")
print(run_pipe(graph, start))
