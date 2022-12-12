import copy
from collections import deque
from dataclasses import dataclass
from functools import partial
from typing import Callable

TEST_INPUT = """noop
addx 3
addx -5"""


@dataclass
class Task:
    callback: Callable
    cycles: int


def noop(*args):
    return None


def add(a, b):
    a = int(a)
    return a + b


CB_MAPPING = {"noop": noop, "addx": add}
FUNC_COST = {noop: 1, add: 2}


def parse_lines(lines):
    tasks = deque()
    for line in lines:
        func_name, *value = line.split()
        func = CB_MAPPING[func_name]
        cb = partial(func, *value)
        tasks.append(Task(callback=cb, cycles=FUNC_COST[func]))
    return tasks


def load_input(fname):
    with open(fname) as fh:
        return [l.strip() for l in fh.readlines()]


def run(task, value):
    task.cycles -= 1
    if task.cycles == 0:
        return task.callback(value)


def render(cycle, value):
    pos = cycle-1 # CRT 0-indexed
    norm = pos - (pos // 40) * 40
    if norm in range(value - 1, value + 2):
        return "#"
    return "."


def program(tasks):
    cycle = 0
    current_task = None
    value = 1
    results = []
    pixels = []
    while tasks:
        cycle += 1
        if cycle == 20 or (cycle - 20) % 40 == 0:
            results.append(copy.copy(value) * cycle)

        pixels.append(render(cycle, value))
        if current_task is None or current_task.cycles == 0:
            current_task = tasks.popleft()

        return_val = run(current_task, value)
        if return_val is not None:
            value = return_val

    return results, pixels

def chunkify(iterable, length):
    for i in range(0, len(iterable), length):
        yield iterable[i:i+length]


tasks = parse_lines(load_input("test_input.txt"))
values, pixels=program(tasks)

print("\n".join(["".join(content) for content in chunkify(pixels, 40)]))

tasks = parse_lines(load_input("input.txt"))
values, pixels = program(tasks)

print("\n".join(["".join(content) for content in chunkify(pixels, 40)]))
