import math


def parse_input(fname):
    with open(fname) as f:
        data = f.readlines()

    data = [int(d) for d in data]
    return data


def calc_fuel_amount(mass):
    return math.floor((mass / 3)) - 2


def calc_fuel_amount_recursive(mass):
    if mass <= 5:
        return 0
    fuel_req = math.floor((mass / 3)) - 2
    return fuel_req + calc_fuel_amount_recursive(fuel_req)


def main():
    masses = parse_input("day1_input.txt")
    fuel_amount = [calc_fuel_amount_recursive(m) for m in masses]
    print(sum((fuel_amount)))


if __name__ == "__main__":
    main()
