import numpy as np


def load_content(fname):
    with open(fname) as fh:
        return [l.strip() for l in fh.readlines()]


def parse_content(lines):
    return [[int(c) for c in l] for l in lines]


def most_common_per_position(array):
    result = []
    rows, cols = array.shape
    for i in range(cols):
        ones = sum(array[:, i])
        zeros = rows - ones
        if ones > zeros:
            result.append(1)
        else:
            result.append(0)
    return result


def inverse(array):
    return [0 if i == 1 else 1 for i in array]


def bit_criteria_filter(array, by_most=True):
    i = 0
    while len(array) > 1:
        rows, _ = array.shape
        ones = sum(array[:, i])
        zeros = rows - ones
        val = 1
        if by_most:
            if zeros > ones:
                val = 0
        else:
            if zeros <= ones:
                val = 0
        array = array[np.where(array[:, i] == val)]
        i += 1
    return array[0]


def bit_list_to_decimal(list_of_byte):
    byte_string = "".join([str(i) for i in list_of_byte])
    return int(byte_string, 2)


data = load_content("input.txt")
data = parse_content(data)
array = np.asarray(data)

gamma = most_common_per_position(array)
epsilon = inverse(gamma)
assert bit_list_to_decimal(gamma) * bit_list_to_decimal(epsilon) == 3923414

oxygen_generator = bit_criteria_filter(array, by_most=True)
co2_scrubber = bit_criteria_filter(array, by_most=False)
assert (
    bit_list_to_decimal(oxygen_generator) * bit_list_to_decimal(co2_scrubber) == 5852595
)
