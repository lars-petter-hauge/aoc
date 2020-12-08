import copy
import itertools


def parse_input(fname):
    with open(fname) as f:
        data = f.readlines()
    return [int(x) for x in data[0].split(",")]


def run(data):
    i = 0
    while data[i] != 99:
        op, a, b, c = data[i : i + 4]
        if op == 1:
            data[c] = data[a] + data[b]
        elif op == 2:
            data[c] = data[a] * data[b]
        else:
            raise NotImplementedError
        i += 4
    return data


if __name__ == "__main__":
    original_data = parse_input("day2/input.txt")

    for x, y in itertools.permutations(range(99), 2):
        data = copy.copy(original_data)
        data[1] = x
        data[2] = y
        data = run(data)
        if data[0] == 19690720:
            break
    print("{},{}".format(data[1], data[2]))
