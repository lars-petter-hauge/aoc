def load_input(fname):
    with open(fname) as fh:
        return fh.read()


def parse_input(string):
    res = []
    for character in string:
        try:
            res.append(int(character))
        except:
            pass

    return res


NUMBERS = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]


def parse_input_two(string):
    res = []
    for idx in range(len(string)):
        try:
            res.append(int(string[idx]))
            continue
        except:
            pass
        for NUMBER in NUMBERS:
            if string[idx:].startswith(NUMBER):
                res.append(NUMBERS.index(NUMBER) + 1)
                continue
    return res


data = load_input("input.txt")
content = [parse_input(line) for line in data.split("\n")]
content = content[:-1]  # drop empty line
print(sum([int(f"{number[0]}{number[-1]}") for number in content]))
content = [parse_input_two(line) for line in data.split("\n")]
content = content[:-1]  # drop empty line
print(sum([int(f"{number[0]}{number[-1]}") for number in content]))
