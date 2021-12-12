from collections import deque, Counter


class SyntaxError(KeyError):
    def __init__(self, error_symbol, message="Salary is not in (5000, 15000) range"):
        self.error_symbol = error_symbol
        self.message = message
        super().__init__(self.message)


def load_content(fname):
    with open(fname) as fh:
        return fh.readlines()


BRACKET_MAP = {"(": ")", "[": "]", "{": "}", "<": ">"}


def parse_line(line):
    """Returns remaining brackets that were not closed"""
    brackets_parsed = deque()
    for symbol in line:
        if symbol in BRACKET_MAP.keys():
            brackets_parsed.append(symbol)
        elif symbol in BRACKET_MAP.values():
            opening = brackets_parsed.pop()
            if BRACKET_MAP[opening] != symbol:
                raise SyntaxError(
                    symbol,
                    f"Error parsing {line}: Expected {BRACKET_MAP[opening]}, found {symbol}",
                )
        else:
            raise NotImplementedError(f"Missing symbol {symbol}")
    return brackets_parsed


def parse_lines(lines):
    valid_lines = []
    error_symbols = []
    remaining_symbols = []
    for line in lines:
        try:
            remaining_symbols.append(parse_line(line))
            valid_lines.append(line)
        except SyntaxError as e:
            error_symbols.append(e.error_symbol)
    return valid_lines, error_symbols, remaining_symbols


SCORE_MAP_ERROR = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
}
SCORE_MAP_REMAINING = {
    ")": 1,
    "]": 2,
    "}": 3,
    ">": 4,
}


def calculate_score(symbols):
    score = 0
    for symbol in symbols:
        score = score * 5
        score += SCORE_MAP_REMAINING[symbol]
    return score


def invert_symbols(symbols):
    inverted = []
    while symbols:
        inverted.append(BRACKET_MAP[symbols.pop()])
    return inverted


lines = load_content("input.txt")
lines = [l.strip() for l in lines]

TEST_DATA = """[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]"""

# valid_lines, error_symbols, remaining_symbols = parse_lines(TEST_DATA.split("\n"))
valid_lines, error_symbols, remaining_symbols = parse_lines(lines)
counter = Counter(error_symbols)

a = 4
score = sum([SCORE_MAP_ERROR[key] * val for key, val in counter.items()])
print(score)

TEST = ["]", ")", "}", ">"]
assert calculate_score(TEST) == 294
all_scores = [calculate_score(invert_symbols(symbols)) for symbols in remaining_symbols]

all_scores.sort()
print(all_scores[int(len(all_scores) / 2 - 0.5)])
