from collections import defaultdict
from math import prod

TEST_DATA = """class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12"""

TEST_DATA_TWO = """class: 0-1 or 4-19
row: 0-5 or 8-19
seat: 0-13 or 16-19

your ticket:
11,12,13

nearby tickets:
3,9,18
15,1,5
5,14,9"""


def load(fname):
    with open(fname) as fh:
        lines = fh.read()
    lines = [l for l in lines.split("\n")]
    return lines


def parse(lines, last_rule_line=20, first_ticket_line=25):
    # parse rules
    rules = {}
    for l in lines[:last_rule_line]:
        key, ranges = l.split(":")
        ranges = [r.strip() for r in ranges.split("or")]
        ranges = [list(map(int, r.split("-"))) for r in ranges]
        rules[key] = ranges

    # parse tickes
    nearby_tickes = [list(map(int, l.split(","))) for l in lines[first_ticket_line:]]

    return rules, nearby_tickes


def is_valid_number_given_ranges(ranges, number):
    return any([(minimum <= number <= maximum) for minimum, maximum in ranges])


def is_valid_number(rules, number):
    for ranges in rules.values():
        if is_valid_number_given_ranges(ranges, number):
            return True
    return False


def is_valid_ticket(rules, ticket):
    return all([is_valid_number(rules, number) for number in ticket])


def part_one(rules, nearby_tickets):
    invalid_numbers = []
    for ticket in nearby_tickets:
        invalid_numbers.extend([n for n in ticket if not is_valid_number(rules, n)])
    return invalid_numbers


def determine_field(rules, tickets):
    possible_fields = defaultdict(list)
    for idx in range(len(nearby_tickets[0])):
        field_numbers = [ticket[idx] for ticket in nearby_tickets]
        for key, ranges in rules.items():
            if all(
                [
                    is_valid_number_given_ranges(ranges, number)
                    for number in field_numbers
                ]
            ):
                possible_fields[key].append(idx)

    fields = {}
    for key, indexes in sorted(possible_fields.items(), key=lambda x: len(x[1])):
        for idx in indexes:
            if idx not in fields.values():
                fields[key] = idx
    return fields


def part_two(rules, nearby_tickets):
    valid_tickets = [
        ticket for ticket in nearby_tickets if is_valid_ticket(rules, ticket)
    ]
    fields = determine_field(rules, valid_tickets)
    return fields


if __name__ == "__main__":
    rules, nearby_tickets = parse(
        TEST_DATA.split("\n"), last_rule_line=3, first_ticket_line=8
    )
    assert sum(part_one(rules, nearby_tickets)) == 71
    assert [ticket for ticket in nearby_tickets if is_valid_ticket(rules, ticket)] == [
        [7, 3, 47]
    ]

    rules, nearby_tickets = parse(
        TEST_DATA_TWO.split("\n"), last_rule_line=3, first_ticket_line=8
    )
    assert part_two(rules, nearby_tickets) == {"seat": 2, "class": 1, "row": 0}

    rules, nearby_tickets = parse(load("input.txt"))
    assert sum(part_one(rules, nearby_tickets)) == 22073

    print(part_two(rules, nearby_tickets))
