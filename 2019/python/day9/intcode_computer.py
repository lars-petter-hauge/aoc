import copy
import itertools
from functools import partial


class ExpandingList(list):
    def __setitem__(self, index, value):
        if index >= len(self):
            self.extend([0] * (index + 1 - len(self)))
        list.__setitem__(self, index, value)

    def __getitem__(self, index):
        if isinstance(index, int):
            if index >= len(self):
                self.extend([0] * (index + 1 - len(self)))
            if index < 0:
                raise IndexError
        else:
            if index.stop and index.stop >= len(self):
                self.extend([0] * (index.stop + 1 - len(self)))
            if index.start and index.start < 0:
                raise IndexError

        return list.__getitem__(self, index)


def parse_input(fname):
    with open(fname) as f:
        data = f.readlines()
    return ExpandingList([int(x) for x in data[0].split(",")])


def add(intcodes, pos, read_a_method, read_b_method, set_c_method, value=None):
    a, b, c = intcodes[pos : pos + 3]
    value = read_a_method(intcodes, a) + read_b_method(intcodes, b)
    set_c_method(intcodes, c, value)


def multiply(intcodes, pos, read_a_method, read_b_method, set_c_method, value=None):
    a, b, c = intcodes[pos : pos + 3]
    value = read_a_method(intcodes, a) * read_b_method(intcodes, b)
    set_c_method(intcodes, c, value)


def save(intcodes, pos, read_a_method, read_b_method, set_c_method, value=None):
    pos = read_a_method(intcodes, pos)
    set_c_method(intcodes, pos, value)


def output(intcodes, pos, read_a_method, read_b_method, set_c_method, value=None):
    pos = read_a_method(intcodes, pos)
    return intcodes[pos]


def jump_if_true(intcodes, pos, read_a_method, read_b_method, set_c_method, value=None):
    a, b = intcodes[pos : pos + 2]
    a = read_a_method(intcodes, a)
    b = read_b_method(intcodes, b)
    if a:
        return b


def jump_if_false(
    intcodes, pos, read_a_method, read_b_method, set_c_method, value=None
):
    a, b = intcodes[pos : pos + 2]
    a = read_a_method(intcodes, a)
    b = read_b_method(intcodes, b)
    if not a:
        return b


def less_than(intcodes, pos, read_a_method, read_b_method, set_c_method, value=None):
    a, b, c = intcodes[pos : pos + 3]
    a = read_a_method(intcodes, a)
    b = read_b_method(intcodes, b)
    if a < b:
        set_c_method(intcodes, c, 1)
    else:
        set_c_method(intcodes, c, 0)


def equals(intcodes, pos, read_a_method, read_b_method, set_c_method, value=None):
    a, b, c = intcodes[pos : pos + 3]
    a = read_a_method(intcodes, a)
    b = read_b_method(intcodes, b)
    if a == b:
        set_c_method(intcodes, c, 1)
    else:
        set_c_method(intcodes, c, 0)


def get_base(intcodes, pos, read_a_method, read_b_method, set_c_method, value=None):
    pos = read_a_method(intcodes, pos)
    return intcodes[pos]


def from_position(intcodes, pos, base):
    return intcodes[pos]


def from_relative_pos(intcodes, pos, base):
    return intcodes[pos + base]


def from_memory(intcodes, pos, base):
    return pos


def to_position(intcodes, pos, value, base):
    intcodes[pos] = value


def to_relative_pos(intcodes, pos, value, base):
    intcodes[pos + base] = value


def parse_opcode(code):
    code = str(code)

    if len(code) == 5:
        c = int(code[0])
        if c !=0:
            # just see if this ever happens
            raise KeyError
        code = code[1:]
    else:
        c = 0

    if len(code) == 4:
        b = int(code[0])
        code = code[1:]
    else:
        b = 0

    if len(code) == 3:
        a = int(code[0])
        code = code[1:]
    else:
        a = 0

    return c, b, a, int(code)


read_mode = {
    0: from_position,
    1: from_memory,
    2: from_relative_pos,
}

set_mode = {
    0: to_position,
    2: to_relative_pos,
}

operations = {
    1: add,
    2: multiply,
    3: save,
    4: output,
    5: jump_if_true,
    6: jump_if_false,
    7: less_than,
    8: equals,
    9: get_base,
}

step_length = {
    1: 3,
    2: 3,
    3: 1,
    4: 1,
    5: 2,
    6: 2,
    7: 3,
    8: 3,
    9: 1,
}


def run(intcodes, value=1, base=0):
    if isinstance(intcodes, list):
        intcodes = ExpandingList(intcodes)
    pos = 0
    results = []
    while intcodes[pos] != 99:
        c, b, a, op = parse_opcode(intcodes[pos])
        print(
            "code: {code}, Performing operation: {oper}, mode c: {mode_c}, mode b: {mode_b}, mode a: {mode_a}".format(
                code=intcodes[pos],
                oper=operations[op].__name__,
                mode_c=set_mode[c].__name__,
                mode_b=read_mode[b].__name__,
                mode_a=read_mode[a].__name__,
            )
        )
        pos += 1
        output = operations[op](
            intcodes,
            pos,
            partial(read_mode[a], base=base),
            partial(read_mode[b], base=base),
            partial(set_mode[c], base=base),
            value=value,
        )

        if op == 4:
            value = output
            print(
                "op code: {} parameter modes: {}{}{} Output: {}".format(
                    op, c, b, a, output
                )
            )
            results.append(output)
        if op == 9:
            base = output

        # Set if jumper changes value
        if op in [5, 6] and output is not None:
            pos = output
        else:
            pos += step_length[op]
    return intcodes, results


def run_tests():

    prog_input = [
        109,
        1,
        204,
        -1,
        1001,
        100,
        1,
        100,
        1008,
        100,
        16,
        101,
        1006,
        101,
        0,
        99,
    ]
    #assert prog_input == run(ExpandingList(prog_input))[1]

    assert 1125899906842624 == run(ExpandingList([104, 1125899906842624, 99]))[1][-1]
    assert (
        1219070632396864
        == run(ExpandingList([1102, 34915192, 34915192, 7, 4, 7, 99, 0]))[1][-1]
    )

    assert [1002, 4, 3, 4, 99] == run([1002, 4, 3, 4, 33])[0][:5]
    assert [1101, 100, -1, 4, 99] == run([1101, 100, -1, 4, 0])[0][:5]

    for value in range(-10, 10):
        # Positional mode
        assert (value == 8) == run([3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8], value=value)[
            1
        ][-1]

        assert (value < 8) == run([3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8], value=value)[1][
            -1
        ]

        # Immediate mode
        assert (value == 8) == run([3, 3, 1108, -1, 8, 3, 4, 3, 99], value=value)[1][-1]
        assert (value < 8) == run([3, 3, 1107, -1, 8, 3, 4, 3, 99], value=value)[1][-1]

        # Jump mode
        assert (value != 0) == run(
            [3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9], value=value
        )[1][-1]
        assert (value != 0) == run(
            [3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1], value=value
        )[1][-1]

        # Larger example
        program = [
            3,
            21,
            1008,
            21,
            8,
            20,
            1005,
            20,
            22,
            107,
            8,
            21,
            20,
            1006,
            20,
            31,
            1106,
            0,
            36,
            98,
            0,
            0,
            1002,
            21,
            125,
            20,
            4,
            20,
            1105,
            1,
            46,
            104,
            999,
            1105,
            1,
            46,
            1101,
            1000,
            1,
            20,
            4,
            20,
            1105,
            1,
            46,
            98,
            99,
        ]
        output = run(program, value=value)[1][-1]

        if value < 8:
            assert output == 999
        elif value == 8:
            assert output == 1000
        else:
            assert output == 1001

    original_data = parse_input("day5/input.txt")
    _, value = run(original_data)
    assert value[-1] == 13210611

    original_data = parse_input("day5/input.txt")
    _, value = run(original_data, value=5)
    assert value[-1] == 584126


if __name__ == "__main__":
    #run_tests()
    original_data = parse_input("day9/input.txt")
    _, value = run(original_data)
    print(value[-1])
