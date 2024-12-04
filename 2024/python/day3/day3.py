
from pathlib import Path
import re
TEST_INPUT="xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"
PATTERN=r"(don't)|(do)|(mul)\((\d+),(\d+)\)"

def load():
    with open(Path(__file__).parent / "input.in") as fh:
        lines = fh.read()
    return lines

def parse_line(line):
    matches = re.findall(PATTERN,line)
    return matches

def solve(matches):
    part1 = 0
    part2 = 0
    should_do = True
    for entry in matches:
        dont, do, _, a, b = entry
        if do:
            should_do = True
        elif dont:
            should_do = False
        else:
            if should_do:
                part2 += int(a) * int(b)
            part1 += int(a) * int(b)
    return part1, part2

print(solve(parse_line(TEST_INPUT)))

print(solve(parse_line(load())))

