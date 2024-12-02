from pathlib import Path

TEST_INPUT="""3   4
4   3
2   5
1   3
3   9
3   3"""

def load():
    with open(Path(__file__).parent / "input.txt") as fh:
        lines = fh.readlines()
    return lines


def parse_lines(lines):
    first, second = [],[]
    for line in lines:
        a,b = line.split()
        first.append(int(a))
        second.append(int(b))
    return first, second

def part_one(first, second):
    result = 0
    first = sorted(first)
    second = sorted(second)
    for i,j in zip(first, second):
        result += abs(j-i)

    return result

def part_two(first,second):
    result = 0
    for number in first:
        result += number * second.count(number)
    return result

def test():
    first, second = parse_lines(TEST_INPUT.split("\n"))
    assert part_one(first, second) == 11

test()
assert part_one(*parse_lines(load())) == 2580760
print(part_two(*parse_lines(load())))


