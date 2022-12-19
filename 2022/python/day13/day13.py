import math
from functools import cmp_to_key
from itertools import chain, zip_longest

flatten = chain.from_iterable

TEST_INPUT = """[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]"""

import json


def load_input(fname):
    with open(fname) as fh:
        return fh.read()


def parse_lines(paired_lines):
    result = []
    for pair in paired_lines:
        first, second = pair.split("\n")
        first = json.loads(first)
        second = json.loads(second)
        result.append((first, second))
    return result


def valid_packets(first, second):

    if isinstance(first, int):
        first = [first]
    if isinstance(second, int):
        second = [second]

    for a, b in zip_longest(first, second):
        if a is None:
            return 1
        if b is None:
            return -1
        if isinstance(a, int) and isinstance(b, int):
            if a < b:
                return 1
            if a > b:
                return -1
        else:
            val = valid_packets(a, b)
            if val != 0:
                return val
    return 0


def get_valid_packets(packet_pairs):
    result = []
    for idx, (first, second) in enumerate(packet_pairs, start=1):
        if valid_packets(first, second) == 1:
            result.append(idx)
    return result


def solve(packet_pairs):
    valid_indices = get_valid_packets(packet_pairs)
    p1 = sum(valid_indices)

    divider_packets = [[[2]], [[6]]]
    packets = list(flatten(packet_pairs))
    packets.extend(divider_packets)
    sorted_packets = sorted(packets, key=cmp_to_key(valid_packets), reverse=True)
    p2 = math.prod([sorted_packets.index(packet) + 1 for packet in divider_packets])
    return p1, p2


packet_pairs = parse_lines(TEST_INPUT.split("\n\n"))
assert get_valid_packets(packet_pairs) == [1, 2, 4, 6]

p1, p2 = solve(packet_pairs)
assert p1 == 13
assert p2 == 140


packet_pairs = parse_lines(load_input("input.txt").split("\n\n"))

p1, p2 = solve(packet_pairs)
print(f"Part1: {p1}, Part2: {p2}")
