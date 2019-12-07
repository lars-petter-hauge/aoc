import copy
import itertools

def parse_input(fname):
    with open(fname) as f:
        data = f.readlines()
    return [int(x) for x in data[0].split(",")]


def add(intcodes, i, read_a_method, read_b_method, value=None):
    a, b, c = intcodes[i:i+3]
    value = read_a_method(intcodes, a) + read_b_method(intcodes, b)
    intcodes[c] = value


def multiply(intcodes, i, read_a_method, read_b_method, value=None):
    a, b, c = intcodes[i:i+3]
    value = read_a_method(intcodes, a) * read_b_method(intcodes, b)
    intcodes[c] = value


def save(intcodes, i, read_a_method, read_b_method, value=None):
    pos = intcodes[i]
    intcodes[pos] = value


def output(intcodes, i, read_a_method, read_b_method, value=None):
    pos = read_a_method(intcodes, i)
    return intcodes[pos]


def jump_if_true(intcodes, i, read_a_method, read_b_method, value=None):
    a, b, c = intcodes[i:i+3]
    a = read_a_method(intcodes, a)
    b = read_b_method(intcodes, b)
    if a:
        return b


def jump_if_false(intcodes, i, read_a_method, read_b_method, value=None):
    a, b, c = intcodes[i:i+3]
    a = read_a_method(intcodes, a)
    b = read_b_method(intcodes, b)
    if not a:
        return b


def less_than(intcodes, i, read_a_method, read_b_method, value=None):
    a, b, c = intcodes[i:i+3]
    a = read_a_method(intcodes, a)
    b = read_b_method(intcodes, b)
    if a<b:
        intcodes[c] = 1
    else:
        intcodes[c] = 0


def equals(intcodes, i, read_a_method, read_b_method, value=None):
    a, b, c = intcodes[i:i+3]
    a = read_a_method(intcodes, a)
    b = read_b_method(intcodes, b)
    if a==b:
        intcodes[c] = 1
    else:
        intcodes[c] = 0


def from_position(intcodes, i):
    return intcodes[i]


def from_memory(intcodes, i):
    return i


def parse_opcode(code):
    code = str(code)

    if len(code)==5:
        a = int(code[0])
        code = code[1:]
    else:
        a = 0

    if len(code)==4:
        b = int(code[0])
        code = code[1:]
    else:
        b = 0

    if len(code)==3:
        c = int(code[0])
        code = code[1:]
    else:
        c = 0

    return a, b, c, int(code)

mode = {
    0: from_position,
    1: from_memory
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
}

def run(intcodes, values=None):
    i = 0
    if values is None:
        raise NotImplementedError

    if not isinstance(values, list):
        values = [values, values]

    first, second = values
    value = first
    while intcodes[i] != 99:
        _, b, c, op = parse_opcode(intcodes[i])
        #print("code: {}, Performing operation: {}, mode: {}, mode: {}".format(intcodes[i], operations[op].__name__, mode[c].__name__, mode[b].__name__))
        i += 1
        output = operations[op](intcodes, i, mode[c], mode[b], value)
        if op == 3:
            value = second
        if op == 4:
            value = output
        if op in [5, 6] and output is not None:
            i = output
        else:
            i += step_length[op]

    return value

def run_tests():

    for value in range(-10,10):
        # Positional mode
        assert (value == 8) == run([3,9,8,9,10,9,4,9,99,-1,8], values=value)
        assert (value < 8) == run([3,9,7,9,10,9,4,9,99,-1,8], values=value)

        # Immediate mode
        assert (value == 8) == run([3,3,1108,-1,8,3,4,3,99], values=value)
        assert (value < 8) == run([3,3,1107,-1,8,3,4,3,99], values=value)

        # Jump mode
        assert (value != 0) == run([3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9], values=value)
        assert (value != 0) == run([3,3,1105,-1,9,1101,0,0,12,4,12,99,1], values=value)

        # Larger example
        program = [3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
                   1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
                   999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99]
        output = run(program, values=value)

        if value < 8:
            assert output == 999
        elif value == 8:
            assert output == 1000
        else:
            assert output == 1001

    original_data = parse_input("day5/input.txt")
    value = run(original_data, values=1)
    assert value == 13210611

    original_data = parse_input("day5/input.txt")
    value = run(original_data, values=5)
    assert value == 584126

if __name__ == '__main__':
    run_tests()
