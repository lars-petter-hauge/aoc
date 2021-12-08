from itertools import chain

flatten = chain.from_iterable


def load(fname):
    with open(fname) as fh:
        return [l.strip() for l in fh.readlines()]


def settify_strings(str):
    result = []
    for word in str.split():
        result.append({c for c in word})
    return result


def parse_content(content):
    return [
        (
            settify_strings(line.split("|")[0]),
            settify_strings(line.split("|")[1]),
        )
        for line in content
    ]


def amount_of_simple_numbers(data):
    lengths = [len(val) for line in data for val in line[1]]
    lengths = [val for val in lengths if val in [2, 3, 4, 7]]
    return len(lengths)


blank_guess = {
    "a": {"a", "b", "c", "d", "e", "f", "g"},
    "b": {"a", "b", "c", "d", "e", "f", "g"},
    "c": {"a", "b", "c", "d", "e", "f", "g"},
    "d": {"a", "b", "c", "d", "e", "f", "g"},
    "e": {"a", "b", "c", "d", "e", "f", "g"},
    "f": {"a", "b", "c", "d", "e", "f", "g"},
    "g": {"a", "b", "c", "d", "e", "f", "g"},
}


def numbers_at_character(guess):
    return {
        0: set.union(
            guess["a"], guess["b"], guess["c"], guess["e"], guess["f"], guess["g"]
        ),
        1: set.union(guess["c"], guess["f"]),
        2: set.union(guess["a"], guess["c"], guess["d"], guess["g"], guess["e"]),
        3: set.union(
            guess["a"],
            guess["c"],
            guess["d"],
            guess["f"],
            guess["g"],
        ),
        4: set.union(
            guess["b"],
            guess["c"],
            guess["d"],
            guess["f"],
        ),
        5: set.union(
            guess["a"],
            guess["b"],
            guess["d"],
            guess["f"],
            guess["g"],
        ),
        6: set.union(
            guess["a"],
            guess["b"],
            guess["d"],
            guess["e"],
            guess["f"],
            guess["g"],
        ),
        7: set.union(
            guess["a"],
            guess["c"],
            guess["f"],
        ),
        8: set.union(
            guess["a"],
            guess["b"],
            guess["c"],
            guess["d"],
            guess["e"],
            guess["f"],
            guess["g"],
        ),
        9: set.union(
            guess["a"],
            guess["b"],
            guess["c"],
            guess["d"],
            guess["f"],
            guess["g"],
        ),
    }


def update_values(update_dict, keys, pattern):
    for key in keys:
        update_dict[key] = update_dict[key].intersection(pattern)


def remove_determined(guess):
    old_length = len(list(flatten(guess.values())))
    determined = {k: v for (k, v) in guess.items() if len(v) == 1}
    for k, vals in guess.items():
        if k in determined:
            continue
        guess[k] = vals.difference(set(flatten(determined.values())))

    if len(list(flatten(guess.values()))) < old_length:
        remove_determined(guess)


def key_at_matching_value(guess, value):
    for key, val in guess.items():
        if value == val:
            return key
    raise ValueError(f"Did not match {value} in any of {guess.values()}")


def evaluate_connections(content):
    result = 0
    for signal_patterns, output_values in content:
        guess = blank_guess.copy()
        all_patterns = signal_patterns + output_values
        all_patterns.sort(key=len)
        for pattern in all_patterns:
            if len(pattern) == 2:  # 1
                update_values(guess, keys=["c", "f"], pattern=pattern)
                continue
            if len(pattern) == 3:  # 7
                update_values(guess, keys=["a", "c", "f"], pattern=pattern)
                continue
            if len(pattern) == 4:  # 4
                update_values(guess, keys=["b", "c", "d", "f"], pattern=pattern)
                continue
            if (len(guess["c"]) <= 2) and (
                len(guess["f"]) <= 2
            ):  # applies only if we have narrowed down c and f to two possibilites
                guess["a"] = guess["a"].difference((guess["c"].union(guess["f"])))
            break
        # top row must be in all numbers except for 1 and 4
        one_four = [val for val in all_patterns if len(val) in [2, 4]]
        the_rest = [val for val in all_patterns if val not in one_four]
        guess["a"] = guess["a"].intersection(
            set(flatten(the_rest)).difference(set(flatten(one_four)))
        )
        remove_determined(guess)

        # If we know connections in one and seven, b and d from four can _not_ have those
        one_seven = set(flatten([val for val in all_patterns if len(val) in [2, 3]]))
        if len(one_seven) == 3:
            guess["b"] = guess["b"].difference(one_seven)
            guess["d"] = guess["b"].difference(one_seven)

        remove_determined(guess)
        # we hopefully have narrowed down numbers to use for a,b,c,d and f.
        # we can remove those from e and g
        a_b_c_d_f = set.union(
            guess["a"],
            guess["b"],
            guess["c"],
            guess["d"],
            guess["f"],
        )
        if len(a_b_c_d_f) == 5:
            guess["g"] = guess["g"].difference(a_b_c_d_f)
            guess["e"] = guess["e"].difference(a_b_c_d_f)
        remove_determined(guess)

        # We try to find the middle rows
        two_three_five = [val for val in all_patterns if len(val) == 5]
        a_d_g = set.intersection(*two_three_five)

        # likely a is already determined, but just in case..
        guess["a"] = guess["a"].intersection(a_d_g)
        if len(guess["a"]) == 1:
            d_g = a_d_g.difference(guess["a"])
        else:
            d_g = a_d_g

        guess["d"] = guess["d"].intersection(d_g)
        guess["g"] = guess["g"].intersection(d_g)
        remove_determined(guess)

        # f must be in all of zero, six, nine
        zero_six_nine_common = set.intersection(
            *[val for val in all_patterns if len(val) == 6]
        )
        guess["f"] = guess["f"].intersection(zero_six_nine_common)
        remove_determined(guess)

        assert all(len(val) == 1 for _, val in guess.items())
        numbers_at_chars = numbers_at_character(guess)
        values = [key_at_matching_value(numbers_at_chars, val) for val in output_values]
        values = [str(v) for v in values]
        values = "".join([str(i) for i in values])
        result += int(values)

    return result


def initial_guess(all_patterns):
    guess = {}
    guess[0] = [p for p in all_patterns if len(all_patterns) == 5]
    guess[2] = [p for p in all_patterns if len(all_patterns) == 5]
    return guess


def evaluate_connections_properly(content):
    result = 0
    for i, (signal_patterns, output_values) in enumerate(content):
        all_patterns = signal_patterns + output_values
        all_patterns.sort(key=len)
        guess = initial_guess(all_patterns)


test_data = """be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce"""

test_data = parse_content(test_data.split("\n"))
assert evaluate_connections(test_data) == 61229

data = load("input.txt")
data = parse_content(data)
assert evaluate_connections(data) == 973499
