def load_content(fname):
    with open(fname) as fh:
        content = fh.readlines()
    return [int(l.strip()) for l in content]


def evaluate_n_increase(measurements):
    increases = 0
    for i in range(len(measurements) - 1):
        current = measurements[i]
        next_n = measurements[i + 1]
        if next_n > current:
            increases += 1
    return increases


def evalute_n_sliding_increase(measurements):
    increases = 0
    for i in range(len(measurements) - 3):
        current = sum(measurements[i : i + 3])
        next_n = sum(measurements[i + 1 : i + 4])
        if next_n > current:
            increases += 1
    return increases


data = load_content("input.txt")
test_data = [
    199,
    200,
    208,
    210,
    200,
    207,
    240,
    269,
    260,
    263,
]
assert evaluate_n_increase(test_data) == 7
assert evalute_n_sliding_increase(test_data) == 5
print(evaluate_n_increase(data))
print(evalute_n_sliding_increase(data))
