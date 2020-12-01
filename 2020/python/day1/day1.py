import itertools


def parse_input(fname):
    with open(fname) as f:
        data = f.readlines()

    data = [int(d) for d in data]
    return data


def find_sum_equal_to(data, number=2020):
    for a, b, c in itertools.combinations(data, 3):
        if a + b + c == number:
            return a * b * c
    raise


def main():
    data = parse_input("input.txt")
    print(find_sum_equal_to(data))


if __name__ == "__main__":
    main()
