TEST_DATA = """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45"""


def load_input(fname):
    with open(fname) as fh:
        return fh.readlines()


def parse_input(lines):
    result = []
    for line in lines:
        result.append([int(c) for c in line.split()])
    return result


def solve_last_numb(sequence, append=True):
    if all([num == 0 for num in sequence]):
        return 0

    diff_sequence = [a - b for a, b in zip(sequence[1:], sequence)]
    if append:
        return sequence[-1] + solve_last_numb(diff_sequence, append)
    return sequence[0] - solve_last_numb(diff_sequence, append)


content = parse_input(TEST_DATA.split("\n"))

print([solve_last_numb(seq) for seq in content])
print([solve_last_numb(seq, append=False) for seq in content])


data = load_input("input.txt")
print(sum([solve_last_numb(seq) for seq in parse_input(data)]))
print(sum([solve_last_numb(seq, append=False) for seq in parse_input(data)]))
