def load_input(fname):
    with open(fname) as fh:
        return [l.strip() for l in fh.readlines()]


def sliding_window(iterable, size=1, step=1):
    for idx in range(0, len(iterable) + 1, step):
        yield iterable[idx : idx + size]


def find_unique_substring(string, size):
    for idx, slide in enumerate(sliding_window(string, size=size)):
        if len(slide) == len(set(slide)):
            return idx


assert find_unique_substring("mjqjpqmgbljsphdztnvjfqwrcgsmlb", size=4) == 7 - 4

assert find_unique_substring("mjqjpqmgbljsphdztnvjfqwrcgsmlb", size=14) == 19 - 14

content = load_input("input.txt")

assert find_unique_substring(content[0], size=14) == 3605 - 14
