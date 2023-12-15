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


TEST_DATA_PART_TWO = """LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)
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


def reduce_nodemap(nodemap):
    result = {}
    for key, val in nodemap.items():
        result[key[:2]] = {"L": val["L"][:2], "R": val["R"][:2]}
    return result


def solve(instructions, nodemap, key="AAA", goal=None):
    goal = goal or ["ZZZ"]
    n_steps = 0
    while True:
        instr = instructions[n_steps % len(instructions)]
        key = nodemap[key][instr]
        n_steps += 1
        if key in goal:
            break
    return n_steps


def solve_part_two(instructions, nodemap):
    start_keys = [key for key in nodemap.keys() if key.endswith("A")]
    goal_keys = [key for key in nodemap.keys() if key.endswith("Z")]
    iters = [solve(instructions, nodemap, key, goal_keys) for key in start_keys]
    lcm = math.lcm(*iters)
    return lcm


instructions, nodemap = parse_input(TEST_DATA_TWO.split("\n"))
print(solve(instructions, nodemap))

instructions, nodemap = parse_input(TEST_DATA_PART_TWO.split("\n"))
print(solve_part_two(instructions, nodemap))
instructions, nodemap = parse_input(load_input("input.txt"))

print(solve(instructions, nodemap))
print(solve_part_two(instructions, nodemap))
