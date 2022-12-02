SYMBOL_BEATS = {"ROCK": "SCISSOR", "SCISSOR": "PAPER", "PAPER": "ROCK"}
TRANSLATE = {"ROCK": ["A", "X"], "PAPER": ["B", "Y"], "SCISSOR": ["C", "Z"]}
MIN_SCORE = {"ROCK": 1, "PAPER": 2, "SCISSOR": 3}


def load_input(fname):
    with open(fname) as fh:
        return fh.readlines()


def translate(symbol):
    for key, vals in TRANSLATE.items():
        if symbol in vals:
            return key
    raise NotImplementedError(f"Did not find {symbol}")


def parse_input(lines):
    result = []
    for line in lines:
        first, second = line.strip().split(" ")
        result.append([translate(first), translate(second)])
    return result


def key_at_value(value):
    for key, val in SYMBOL_BEATS.items():
        if val == value:
            return key


def parse_input_second(lines):
    result = []
    for line in lines:
        first, second = line.strip().split(" ")
        first = translate(first)
        if second == "X":
            second = SYMBOL_BEATS[first]
        elif second == "Y":
            second = first
        elif second == "Z":
            second = key_at_value(first)

        result.append([first, second])
    return result


def score(player, opponent):
    if player == opponent:
        return 3

    if SYMBOL_BEATS[player] == opponent:
        return 6
    return 0


def sum_score(rounds):
    return sum([score(player=r[1], opponent=r[0]) + MIN_SCORE[r[1]] for r in rounds])


content = load_input("input.txt")
rounds = parse_input(content)

print(sum_score(rounds))

rounds = parse_input_second(content)
print(sum_score(rounds))
