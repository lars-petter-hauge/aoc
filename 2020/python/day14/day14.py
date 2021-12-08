import numpy as np
import re

TEST_DATA="""mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0"""


def test():
    mask = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X"
    assert apply_mask(11, mask) == 73
    assert apply_mask(101, mask) == 101
    assert apply_mask(0, mask) == 64

def parse(lines):
    comp = re.compile("\[(.*?)\]|(\d+)(?!.*\d)")
    all_instructions = []
    mask = ""
    instructions = []
    for i, line in enumerate(lines):
        if line.startswith("mask"):
            if i !=0:
                all_instructions.append((mask, instructions))
            instructions = []
            mask = line[7:]
            continue

        matches = comp.findall(line)
        instructions.append({"addr": int(matches[0][0]), "value": int(matches[1][1])})
        if i == len(lines)-1:
            all_instructions.append((mask, instructions))
    return all_instructions


def load(fname):
    with open(fname) as fh:
        lines = fh.readlines()
    lines = [l.strip() for l in lines]
    return lines


def apply_mask(value, mask):
    value = [x for x in np.binary_repr(value)]
    value = [0]*(len(mask)-len(value)) + value
    value = [int(v) if m == "X" else int(m) for v, m in zip(value, mask) ]
    return int("".join([str(x) for x in value]), 2)

def run(array, instruction_set):
    for mask, instructions in instruction_set:
        for instruction in instructions:
            array[instruction["addr"]] = apply_mask(instruction["value"], mask)
    return array



if __name__ == "__main__":
    test()
    instruction_set = parse(TEST_DATA.split("\n"))
    print(run(array=[0]*10, instruction_set=instruction_set))
    instruction_set = parse(load("2020/python/day14/input.txt"))
    print(sum(run(array=[0]*100000, instruction_set=instruction_set)))


