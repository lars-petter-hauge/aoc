import string

SCORE = {
    **{char: i + 1 for i, char in enumerate(string.ascii_lowercase)},
    **{char: i + 27 for i, char in enumerate(string.ascii_uppercase)},
}


TEST_DATA = """vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw"""


def load_input(fname):
    with open(fname) as fh:
        return [l.strip() for l in fh.readlines()]


def parse_input(lines):
    result = []
    for line in lines:
        mid = int(len(line) / 2)
        result.append((line[:mid], line[mid:]))
    return result


def collect_duplicates(rucksacks):
    duplicates = []
    for rucksack in rucksacks:
        a, b = rucksack
        duplicates.append(set(a).intersection(set(b)))
    return duplicates


def per_chunk(content, n):
    i = 0
    while i < len(content):
        yield content[i : i + n]
        i += n


def collect_badges(rucksacks):
    badges = []
    for group_sacks in per_chunk(rucksacks, 3):
        compartments = set(SCORE.keys())
        for sack in group_sacks:
            first, second = sack
            compartments = compartments.intersection(set(first).union(second))
        assert len(compartments) == 1
        badges.append(compartments)
    return badges


def score_items(items):
    items = items.copy()
    return [SCORE[item.pop()] for item in items]


rucksacks = parse_input(TEST_DATA.split("\n"))
duplicates = collect_duplicates(rucksacks)
print(sum(score_items(duplicates)))
badges = collect_badges(rucksacks)
print(sum(score_items(badges)))

content = load_input("input.txt")
rucksacks = parse_input(content)
duplicates = collect_duplicates(rucksacks)
print(sum(score_items(duplicates)))
badges = collect_badges(rucksacks)
print(sum(score_items(badges)))
