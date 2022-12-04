def load_input(fname):
    with open(fname) as fh:
        return [l.strip() for l in fh.readlines()]


def completely_overlapping_sections(listofpair):
    return [
        [first, second]
        for first, second in listofpair
        if (first[0] <= second[0] and first[1] >= second[1])
        or (second[0] <= first[0] and second[1] >= first[1])
    ]


def partly_lapping_sections(listofpair):
    return [
        [first, second]
        for first, second in listofpair
        if (first[1] >= second[0] and first[0] <= second[0])
        or (first[0] <= second[1] and first[1] >= second[0])
    ]


def parse_input(lines):
    result = []
    for line in lines:
        a, b = line.split(",")
        first = [int(c) for c in a.split(",")[0].split("-")]
        second = [int(c) for c in b.split(",")[0].split("-")]
        result.append([first, second])
    return result


content = load_input("input.txt")
elves_sections = parse_input(content)
print(len(completely_overlapping_sections(elves_sections)))
print(len(partly_lapping_sections(elves_sections)))
