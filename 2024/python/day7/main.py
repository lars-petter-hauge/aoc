from pathlib import Path
from itertools import product, zip_longest
TEST_INPUT = """190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20"""

def load():
    with open(Path(__file__).parent / "input.in") as fh:
        lines = fh.readlines()
    return lines

def combinations(iters, length):
    for i in range(length):
        if length == 1:
            yield iters[i]
        else:
            yield [iters[i]] + list(combinations(iters, length-1))

def solve(lines):
    results =[]
    for line in lines:
        answer, args = line.split(":")
        args = args.strip().split()
        for operators in product("+*", repeat=len(args)-1):
            result = args[0]
            for arg, oper in zip_longest(args[1:], operators, fillvalue=" "):
                result = eval(str(result)+oper+arg) 
            if str(result) == answer:
                results.append(result)
                break



    return results

# print(solve(TEST_INPUT.split("\n")))
print(sum(solve(load())))

