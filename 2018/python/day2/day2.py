from collections import Counter
from itertools import product
import difflib


def parse_input(input):
    result = [x.split()[0] for x in input]
    return result


def read_input(fname):
    with open(fname) as f:
        input = f.readlines()
    return input


def part_one(input):
    doubles = 0
    triples = 0
    for line in input:
        c = Counter(line)
        if 2 in c.values():
            doubles += 1
        if 3 in c.values():
            triples += 1
    print(doubles * triples)


def part_two(input):
    products = product(input, input)
    closest_match = 9999
    for prod in products:
        if prod[0] == prod[1]:
            continue
        a = prod[0]
        b = prod[1]
        length = len(a) if len(a) < len(b) else len(b)
        matching = [a[i] for i in range(length) if a[i] == b[i]]

        check = length - len(matching)
        if check < closest_match:
            closest_match = check
            print(
                "Closest match: {} and {}, only {} differences.\n"
                "Removing the differences leaves: {}".format(
                    a, b, check, "".join(matching)
                )
            )


if __name__ == "__main__":
    input = read_input("day2input")
    parsed = parse_input(input)
    part_two(parsed)
