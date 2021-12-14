from collections import Counter, defaultdict
from re import sub
from scipy.optimize import curve_fit
import plotly.graph_objects as go
import numpy as np


def load_content(fname):
    with open(fname) as fh:
        return [l.strip() for l in fh.readlines()]


def parse_content(content):
    template = [i for i in content[0]]
    subst = {}
    for line in content[2:]:
        pattern, inject = line.split("->")
        subst[pattern.strip()] = inject.strip()
    return template, subst


def naive_insert_polymer(template, subst):
    result = []
    for a, b in zip(template, template[1:]):
        result.append(a)
        result.append(subst[a + b])
    result.append(template[-1])

    return result


def count_constituents_after_n_turns(polymer, substitutions, turns):
    constituents = Counter(polymer)
    pairs = Counter([a + b for a, b in zip(polymer, polymer[1:])])

    for _ in range(turns):
        pairs, old_pairs = Counter(), pairs

        for (a, b), inject in substitutions.items():
            pairs[a + inject] += old_pairs[a + b]
            pairs[inject + b] += old_pairs[a + b]
            constituents[inject] += old_pairs[a + b]

    return constituents


TEST_DATA = """NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C"""


def run_test():
    template, subst = parse_content(TEST_DATA.split("\n"))
    constituents = count_constituents_after_n_turns(template, subst, 10)
    assert constituents["B"] == 1749

    for _ in range(4):
        template = naive_insert_polymer(template, subst)
    counter = Counter(template)
    assert counter["B"] == 23


run_test()

data = load_content("input.txt")
template, subst = parse_content(data)
result = count_constituents_after_n_turns(template, subst, 40)
