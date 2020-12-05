import math


def parse(fname):
    with open(fname) as f:
        lines = f.readlines()
        lines = [l.strip() for l in lines]

    return lines


def binary_search(instructions, lower_bound, upper_bound):
    instr = instructions[0]
    forward = instr == "F" or instr == "L"

    if len(instructions) == 1:
        if forward:
            return lower_bound
        else:
            return upper_bound

    half = math.ceil((upper_bound - lower_bound) / 2)
    if forward:
        return binary_search(
            instructions[1:], lower_bound=lower_bound, upper_bound=upper_bound - half
        )
    else:
        return binary_search(
            instructions[1:], lower_bound=lower_bound + half, upper_bound=upper_bound
        )


def calc_seat_id(line, n_seats):
    row_index = binary_search(line[:7], 0, n_seats)
    column_index = binary_search(line[-3:], 0, 7)
    return row_index * 8 + column_index


def part_one():
    lines = parse("input.txt")
    maximum = 0
    for line in lines:
        ID = calc_seat_id(line, 127)
        if ID > maximum:
            maximum = ID
    return maximum


def part_two():
    lines = parse("input.txt")
    occupied_seats = []
    for line in lines:
        occupied_seats.append(calc_seat_id(line, 127))
    possible_seats = set(range(max(occupied_seats))) - set(occupied_seats)

    correct_seat = 0
    for seat_id in possible_seats:
        if seat_id == 0 or seat_id == max(occupied_seats):
            continue
        if (seat_id - 1) in occupied_seats and (seat_id + 1) in occupied_seats:
            correct_seat = seat_id
            break

    return correct_seat


if __name__ == "__main__":
    assert binary_search("FBFBBFF", 0, 127) == 44
    assert binary_search("RLR", 0, 7) == 5
    assert calc_seat_id("BFFFBBFRRR", 127) == 567
    assert calc_seat_id("FFFBBBFRRR", 127) == 119
    assert calc_seat_id("BBFFBBFRLL", 127) == 820
    print(part_one())
    print(part_two())
