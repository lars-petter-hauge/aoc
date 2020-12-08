import unittest
from collections import Counter
import matplotlib.pyplot as plt


def parse_data(lines):
    parsed = []
    for l in lines:
        l = l.strip()
        parsed.append([x for x in l])
    return parsed


def read_input(fname):
    with open(fname) as f:
        data = f.readlines()
    return data


def whats_around(field, i, j):
    surrounding = []
    for x in range(-1, 2):
        for y in range(-1, 2):
            if i + x < 0 or i + x > len(field) - 1:
                continue
            if j + y < 0 or j + y > len(field[0]) - 1:
                continue
            if x == 0 and y == 0:
                continue
            surrounding.append(field[i + x][j + y])
    return Counter(surrounding)


def evalute_field(field):
    old_state = [x[:] for x in field]
    for i in range(len(field)):
        for j in range(len(field[0])):
            surroundings = whats_around(old_state, i, j)
            if field[i][j] == "." and surroundings["|"] >= 3:
                field[i][j] = "|"
            elif field[i][j] == "|" and surroundings["#"] >= 3:
                field[i][j] = "#"
            elif field[i][j] == "#" and (
                surroundings["#"] < 1 or surroundings["|"] < 1
            ):
                field[i][j] = "."
    return field


def print_field(field):
    for f in field:
        print("".join(f))


class Test(unittest.TestCase):
    def test(self):
        data = read_input("day18test_input")
        field = parse_data(data)
        for i in range(10):
            field = evalute_field(field)
        answer = read_input("day18_test_answer")
        answer = parse_data(answer)
        assert answer == field
        flatten = [x for sub in field for x in sub]
        count_field = Counter(flatten)
        assert 1147 == (count_field["#"] * count_field["|"])


def main():
    data = read_input("day18_input")
    field = parse_data(data)
    x = []
    y = []
    for i in range(600):
        field = evalute_field(field)
        flatten = [k for sub in field for k in sub]
        count_field = Counter(flatten)
        x.append(i)
        y.append(count_field["#"] * count_field["|"])
    sublist = y[470:497]
    n = sublist[(10000000 - 471) % len(sublist)]


if __name__ == "__main__":
    # unittest.main()
    main()
