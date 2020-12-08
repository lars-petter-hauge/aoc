import re
import numpy as np
import unittest


def parse_data(input):
    parsed = {}
    for line in input:
        splitted = re.split("#|@ |,|: |x|\n|", line)
        parsed[int(splitted[1])] = {
            "i": int(splitted[2]),
            "j": int(splitted[3]),
            "ni": int(splitted[4]),
            "nj": int(splitted[5]),
        }
    return parsed


def read_input(fname):
    with open(fname) as f:
        input = f.readlines()
    return input


def coordinates(instr):
    ibeg = instr["i"]
    iend = ibeg + instr["ni"]
    jbeg = instr["j"]
    jend = jbeg + instr["nj"]
    return ibeg, iend, jbeg, jend


def populate(array, instructions):
    for id, instr in instructions.items():
        ibeg, iend, jbeg, jend = coordinates(instr)
        for i in range(ibeg, iend):
            for j in range(jbeg, jend):
                array[i][j] = array[i][j] + 1
    return array


def overlaps(array, instr):
    ibeg, iend, jbeg, jend = coordinates(instr)
    for i in range(ibeg, iend):
        for j in range(jbeg, jend):
            if array[i][j] > 1:
                return True
    return False


def verify_overlap(array, instructions):
    for id, instr in instructions.items():
        if not overlaps(array, instr):
            return id
    return None


def main(data):
    array = np.zeros(shape=(1000, 1000))
    array = populate(array, data)
    print("number of overlapping: {}".format((array > 1).sum()))
    print("Following does not overlap: {}".format(verify_overlap(array, data)))


class Test(unittest.TestCase):
    def test(self):
        array = np.zeros(shape=(8, 8))
        input = read_input("day3_testinput")
        parsed = parse_data(input)
        array = populate(array, parsed)

        self.assertEqual((array > 1).sum(), 4)
        self.assertEqual(verify_overlap(array, parsed), 3)


if __name__ == "__main__":
    # unittest.main()
    input = read_input("day3input")
    parsed = parse_data(input)
    main(parsed)
