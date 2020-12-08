import unittest


def strip_me(l):
    if l[0] == "A" or l[0] == "B":
        result = l[9:19].split(",")
    else:
        result = l.split()
    return [int(s) for s in result]


def parse_input(lines):
    idx = 0
    operations = []
    while idx < len(lines):
        l = lines[idx].strip()
        if not l:
            idx += 1
            continue
        pre = strip_me(l)
        oper = strip_me(lines[idx + 1].strip())
        post = strip_me(lines[idx + 2].strip())
        idx += 3
        operations.append([pre, oper, post])
    return operations


def parse_input_two(lines):
    result = []
    for l in lines:
        result.append(strip_me(l.strip()))
    return result


def read_input(fname):
    with open(fname) as f:
        result = f.readlines()
    return result


def addr(reg, instr):
    reg[instr[2]] = reg[instr[0]] + reg[instr[1]]
    return reg


def addi(reg, instr):
    reg[instr[2]] = reg[instr[0]] + instr[1]
    return reg


def mulr(reg, instr):
    reg[instr[2]] = reg[instr[0]] * reg[instr[1]]
    return reg


def muli(reg, instr):
    reg[instr[2]] = reg[instr[0]] * instr[1]
    return reg


def banr(reg, instr):
    reg[instr[2]] = reg[instr[0]] & reg[instr[1]]
    return reg


def bani(reg, instr):
    reg[instr[2]] = reg[instr[0]] & instr[1]
    return reg


def borr(reg, instr):
    reg[instr[2]] = reg[instr[0]] | reg[instr[1]]
    return reg


def bori(reg, instr):
    reg[instr[2]] = reg[instr[0]] | instr[1]
    return reg


def setr(reg, instr):
    reg[instr[2]] = reg[instr[0]]
    return reg


def seti(reg, instr):
    reg[instr[2]] = instr[0]
    return reg


def gtir(reg, instr):
    reg[instr[2]] = int(instr[0] > reg[instr[1]])
    return reg


def gtri(reg, instr):
    reg[instr[2]] = int(reg[instr[0]] > instr[1])
    return reg


def gtrr(reg, instr):
    reg[instr[2]] = int(reg[instr[0]] > reg[instr[1]])
    return reg


def eqir(reg, instr):
    reg[instr[2]] = int(instr[0] == reg[instr[1]])
    return reg


def eqri(reg, instr):
    reg[instr[2]] = int(reg[instr[0]] == instr[1])
    return reg


def eqrr(reg, instr):
    reg[instr[2]] = int(reg[instr[0]] == reg[instr[1]])
    return reg


def evaluate_input(situations):
    functions = [
        addr,
        addi,
        mulr,
        muli,
        banr,
        bani,
        borr,
        bori,
        setr,
        seti,
        gtir,
        gtri,
        gtrr,
        eqir,
        eqri,
        eqrr,
    ]
    possibilities = {func: list(range(16)) for func in functions}
    samples = 0
    for pre, instr, post in situations:
        nvalidopcodes = 0
        for func in functions:
            test_pre = pre.copy()
            test_post = func(test_pre, instr[1:])
            if test_post == post:
                nvalidopcodes += 1
            if test_post != post:
                if instr[0] in possibilities[func]:
                    idx = possibilities[func].index(instr[0])
                    possibilities[func].pop(idx)
        if nvalidopcodes >= 3:
            samples += 1
    print("{} samples are valid for 3 or more opcodes".format(samples))
    return possibilities


def evaluate_opcodes(possibilities):
    opcodes = {}
    while possibilities:
        codes = {key: val[0] for key, val in possibilities.items() if len(val) == 1}
        for k, val in codes.items():
            opcodes[k] = val
            for _, possibles in possibilities.items():
                if val in possibles:
                    idx = possibles.index(val)
                    possibles.pop(idx)

        possibilities = {key: val for key, val in possibilities.items() if len(val) > 0}
    return opcodes


def run_prog(reg, codes_def, instructions):
    for instr in instructions:
        print()
        reg = codes_def[instr[0]](reg, instr[1:])
    return reg


class Test(unittest.TestCase):
    def test(self):
        data = read_input("day16testinput")
        parsed = parse_input(data)
        assert len(parsed) == 1
        possibilities = evaluate_input(parsed)
        possibles = [k for k, val in possibilities.items() if len(val) == 15]
        assert len(possibles) == 3
        assert mulr in possibles
        assert addi in possibles
        assert seti in possibles


def main():
    data = read_input("day16input")
    part_one = data[:3297]
    part_two = data[3298:]
    parsed = parse_input(part_one)
    possibilities = evaluate_input(parsed)
    opcodes = evaluate_opcodes(possibilities)
    opcodes = {val: key for key, val in opcodes.items()}
    parsed_two = parse_input_two(part_two)
    register = run_prog([0, 0, 0, 0], opcodes, parsed_two)
    print("final register: {}".format(register))


if __name__ == "__main__":
    # unittest.main()
    main()
