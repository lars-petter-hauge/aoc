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

    if len(second) == 0:
        return False
    if len(first) == 0:
        return True

    for a, b in zip(first, second):
        if isinstance(a, int) and isinstance(b, int):
            if a == b:
                continue
            return a < b
        else:
            try:
                return valid_packets(a, b)
            except ValueError:
                # Could not determine validity, continue
                pass
    # No decision yet, compare list lengths to determine validation
    if len(first) == len(second):
        raise ValueError("Indeterminate")
    return len(first) < len(second)


def get_valid_packets(packet_pairs):
    result = []
    for idx, (first, second) in enumerate(packet_pairs):
        if valid_packets(first, second):
            result.append(idx + 1)
    return result


packet_pairs = parse_lines(TEST_INPUT.split("\n\n"))
for first, second in packet_pairs:
    valid_packets(first, second)
print(get_valid_packets(packet_pairs))
assert get_valid_packets(packet_pairs) == [1, 2, 4, 6]
packet_pairs = parse_lines(load_input("input.txt").split("\n\n"))
print(sum(get_valid_packets(packet_pairs)))
# 10621 too high
# 5321 too low
# Task incomplete.
