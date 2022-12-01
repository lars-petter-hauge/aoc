def load_input(fname):
    with open(fname) as fh:
        return fh.read()


def parse_input(string):
    paragraphs = string.split("\n\n")
    return [sum([int(v) for v in s.split("\n") if v != ""]) for s in paragraphs]


data = load_input("input.txt")
elves = parse_input(data)
print(max(elves))
print(sum(sorted(elves)[-3:]))
