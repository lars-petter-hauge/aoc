from collections import deque, namedtuple
from copy import deepcopy
from itertools import zip_longest

TEST_STOCK = [
    [
        " ",
        "D",
        " ",
    ],
    [
        "N",
        "C",
        " ",
    ],
    [
        "Z",
        "M",
        "P",
    ],
]

TEST_PROCEDURES = """move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2"""

TASK_STOCK = [
    ["T", "V", " ", " ", " ", " ", " ", "W", " "],
    ["V", "C", "P", "D", " ", " ", " ", "B", " "],
    ["J", "P", "R", "N", "B", " ", " ", "Z", " "],
    ["W", "Q", "D", "M", "T", " ", "L", "T", " "],
    ["N", "J", "H", "B", "P", "T", "P", "L", " "],
    ["R", "D", "F", "P", "R", "P", "R", "S", "G"],
    ["M", "W", "J", "R", "V", "B", "J", "C", "S"],
    ["S", "B", "B", "F", "H", "C", "B", "N", "L"],
]


def load_input(fname):
    with open(fname) as fh:
        return [l.strip() for l in fh.readlines()]


Procedure = namedtuple("Procedure", ["amount", "source", "target"])


def parse_content(lines):
    result = []
    for line in lines:
        _, n, _, source, _, target = line.split(" ")
        result.append(Procedure(int(n), int(source), int(target)))
    return result


def create_stock(list_of_lists):
    return {
        i + 1: crates
        for i, crates in enumerate(
            map(deque, map(reversed, zip_longest(*list_of_lists)))
        )
    }


def remove_empty_crates(stock):
    for crate in stock.values():
        while crate[-1] == " ":
            crate.pop()


def move_crates(stock, source, target, amount, one_at_a_time=True):

    crates_to_move = [stock[source].pop() for _ in range(amount)]
    if one_at_a_time:
        stock[target].extend(crates_to_move)
    else:
        stock[target].extend(reversed(crates_to_move))


def run(stock_input, procedure_input):

    original_stock = create_stock(stock_input)
    remove_empty_crates(original_stock)

    procedures = parse_content(procedure_input)

    stock = deepcopy(original_stock)
    for procedure in procedures:
        move_crates(stock, procedure.source, procedure.target, procedure.amount)

    print("".join([crate[-1] for crate in stock.values()]))

    stock = deepcopy(original_stock)
    for procedure in procedures:
        move_crates(
            stock,
            procedure.source,
            procedure.target,
            procedure.amount,
            one_at_a_time=False,
        )
    print("".join([crate[-1] for crate in stock.values()]))


run(TEST_STOCK, TEST_PROCEDURES.split("\n"))

run(TASK_STOCK, load_input("input.txt"))
