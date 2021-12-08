from collections import Counter

def load_content(fname):
    with open(fname) as fh:
        return fh.readlines()


def parse_content(lines):
    content = lines[0].strip()
    return [int(c) for c in content.split(",")]


def simulate_lanterns(lanterns, days):
    counter = Counter(lanterns)
    state = dict(counter)
    for _ in range(days):
        new_state = {}
        for i in [0, 1, 2, 3, 4, 5, 7]:
            new_state[i] = state.get(i + 1, 0)
        new_state[6] = state.get(7, 0) + state.get(0, 0)
        new_state[8] = state.get(0, 0)
        state.update(new_state)

    return state


assert sum(simulate_lanterns(lanterns=[3, 4, 3, 1, 2], days=18).values()) == 26
assert sum(simulate_lanterns(lanterns=[3, 4, 3, 1, 2], days=80).values()) == 5934
assert (
    sum(simulate_lanterns(lanterns=[3, 4, 3, 1, 2], days=256).values()) == 26984457539
)

data = load_content("input.txt")
lanterns = parse_content(data)
print(simulate_lanterns(lanterns=lanterns, days=256))
