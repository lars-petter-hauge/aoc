import math
from collections import Counter
from functools import partial


def load_input(fname):
    with open(fname) as fh:
        return [l.strip() for l in fh.readlines()]


def square(a):
    return a ** 2


def multiply(a, b):
    return a * b


def add(a, b):
    return a + b


def is_divisible_by(a, b=1):
    return a % b == 0


def parse(lines):
    monkeys = {}
    items = None
    operation = None
    check = None
    cond_true = None
    cond_false = None
    name = None
    for line in lines:
        if line == "":
            monkeys[name] = {
                "items": items,
                "inspect": operation,
                "check": check,
                "cond_true": cond_true,
                "cond_false": cond_false,
            }
        if line.startswith("M"):
            name = int(line[-2:-1])
            continue
        if line.startswith("S"):
            items = [int(item) for item in line[16:].split(",")]
            continue
        if line.startswith("O"):
            a, oper, b = line[17:].split()
            if a == "old" and b == "old":
                operation = square
                continue
            elif oper == "*":
                operation = partial(multiply, int(b))
                continue
            elif oper == "+":
                operation = partial(add, int(b))
                continue
            raise NotImplementedError()
        if line.startswith("T"):
            check = partial(is_divisible_by, b=int(line.split()[-1]))
        if line.startswith("If true"):
            cond_true = int(line[-1])
        if line.startswith("If false"):
            cond_false = int(line[-1])
    # Add last monkey:
    monkeys[name] = {
        "items": items,
        "inspect": operation,
        "check": check,
        "cond_true": cond_true,
        "cond_false": cond_false,
    }
    return monkeys


def throw_time(monkeys, rounds=1):
    counter = Counter()
    for _ in range(rounds):
        for monkey, content in monkeys.items():
            while content["items"]:
                item_level = content["items"].pop(0)
                item_level = content["inspect"](item_level)
                item_level = int(item_level / 3)  # int rounds down
                if content["check"](item_level):
                    receiver = content["cond_true"]
                else:
                    receiver = content["cond_false"]
                monkeys[receiver]["items"].append(item_level)
                counter.update([monkey])
    return counter


lines = load_input("test_input.txt")
monkeys = parse(lines)
counter = throw_time(monkeys, rounds=20)
print(math.prod([val for m, val in counter.most_common()[:2]]))


lines = load_input("input.txt")
monkeys = parse(lines)
counter = throw_time(monkeys, rounds=20)
print(math.prod([val for m, val in counter.most_common()[:2]]))
