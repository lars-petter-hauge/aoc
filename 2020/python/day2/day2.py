from collections import namedtuple, Counter


def parse_input(fname, information):
    with open(fname) as f:
        lines = f.readlines()

    data = []
    for l in lines:
        min_max, symbol, pw_string = l.split()
        s_min, s_max = min_max.split("-")
        info = information(symbol.strip(":"), int(s_min), int(s_max))
        data.append((info, pw_string))

    return data


def valid_passwords_part_one(data):
    result = []
    for info, pw_string in data:
        counter = Counter(pw_string)
        if info.min <= counter[info.symbol] <= info.max:
            result.append(pw_string)
    return result


def valid_passwords_part_two(data):
    result = []
    for info, pw_string in data:
        if (
            sum(
                [
                    pw_string[info.pos_one - 1] == info.symbol,
                    pw_string[info.pos_two - 1] == info.symbol,
                ]
            )
            == 1
        ):
            result.append(pw_string)
    return result


def main():

    part_one_info = namedtuple("info", ["symbol", "min", "max"])
    data = parse_input("input.txt", part_one_info)
    result = valid_passwords_part_one(data)
    print(len(result))

    part_two_info = namedtuple("info", ["symbol", "pos_one", "pos_two"])
    data = parse_input("input.txt", part_two_info)
    result = valid_passwords_part_two(data)
    print(len(result))


if __name__ == "__main__":
    main()
