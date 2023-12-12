from collections import defaultdict
import math

TEST_DATA = """RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)"""

TEST_DATA_TWO = """LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)
"""


def load_input(fname):
    with open(fname) as fh:
        return fh.readlines()


def parse_input(lines):
    instructions = [c for c in lines[0].strip()]
    nodemap = {}
    for line in lines[2:]:
        key = line[:3]
        left = line[7:10]
        right = line[12:15]
        nodemap[key] = {"L": left, "R": right}
    return instructions, nodemap


def solve(instructions, nodemap):
    n_steps = 0
    key = "AAA"
    while True:
        instr = instructions[n_steps % len(instructions)]
        key = nodemap[key][instr]
        n_steps += 1
        if key == "ZZZ":
            break
    return n_steps


instructions, nodemap = parse_input(TEST_DATA.split("\n"))
print(solve(instructions, nodemap))

instructions, nodemap = parse_input(TEST_DATA_TWO.split("\n"))
print(solve(instructions, nodemap))

instructions, nodemap = parse_input(load_input("input.txt"))

print(solve(instructions, nodemap))
