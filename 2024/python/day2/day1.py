from pathlib import Path
from copy import copy

TEST_INPUT="""7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9"""

def load():
    with open(Path(__file__).parent / "input.in") as fh:
        lines = fh.readlines()
    return lines

def parse_lines(lines):
    result = []
    for line in lines:
        result.append([int(x) for x in line.split()])
    return result

def check(report):

    # reports are either increasing or decreasing
    if report != sorted(report) and report != list(reversed(sorted(report))):
        return False

    # increase between levels should always be between 1 and 3
    deltas = [abs(a-b) for a,b in zip(report,report[1:])]
    if any([delta>3 or delta == 0 for delta in deltas]):
        return False

    return True

def solve(reports):
    return [report for report in reports if check(report)]

def solve2(reports):
    safe = []
    for report in reports:
        if check(report):
            safe.append(report)
            continue

        for idx in range(0,len(report)):
            modified = copy(report)
            modified.pop(idx)
            if check(modified):
                safe.append(report)
                break
    return safe

print(solve2(parse_lines(TEST_INPUT.split("\n"))))
content = parse_lines(load())
print(len(solve(content)))
print(len(solve2(content)))
