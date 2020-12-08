import unittest


def read_input(fname):
    with open(fname) as f:
        result = f.readlines()
    return result


def parse_data(lines):
    start = int(lines[0][4])  # ip register number
    instructions = []
    for l in lines[1:]:
        l = l.strip()
        instructions.append([l[:4]] + [int(x) for x in l[5:].split(" ")])
    return start, instructions


def addr(r, i):
    r[i[2]] = r[i[0]] + r[i[1]]
    return r


def addi(r, i):
    r[i[2]] = r[i[0]] + i[1]
    return r


def mulr(r, i):
    r[i[2]] = r[i[0]] * r[i[1]]
    return r


def muli(r, i):
    r[i[2]] = r[i[0]] * i[1]
    return r


def banr(r, i):
    r[i[2]] = r[i[0]] & r[i[1]]
    return r


def bani(r, i):
    r[i[2]] = r[i[0]] & i[1]
    return r


def borr(r, i):
    r[i[2]] = r[i[0]] | r[i[1]]
    return r


def bori(r, i):
    r[i[2]] = r[i[0]] | i[1]
    return r


def setr(r, i):
    r[i[2]] = r[i[0]]
    return r


def seti(r, i):
    r[i[2]] = i[0]
    return r


def gtir(r, i):
    r[i[2]] = int(i[0] > r[i[1]])
    return r


def gtrr(r, i):
    r[i[2]] = int(r[i[0]] > r[i[1]])
    return r


def gtri(r, i):
    r[i[2]] = int(r[i[0]] > i[1])
    return r


def eqir(r, i):
    r[i[2]] = int(i[0] == r[i[1]])
    return r


def eqrr(r, i):
    r[i[2]] = int(r[i[0]] == r[i[1]])
    return r


def eqri(r, i):
    r[i[2]] = int(r[i[0]] == i[1])
    return r


functions = {
    "addr": addr,
    "addi": addi,
    "mulr": mulr,
    "muli": muli,
    "bani": bani,
    "banr": banr,
    "borr": borr,
    "bori": bori,
    "setr": setr,
    "seti": seti,
    "gtir": gtir,
    "gtri": gtri,
    "gtrr": gtrr,
    "eqir": eqir,
    "eqri": eqri,
    "eqrr": eqrr,
}


def run_program(ip_idx, instructions):
    reg = [0, 0, 0, 0, 0, 0]
    i = 1
    ip = 0
    while ip < len(instructions):
        instr = instructions[ip]
        reg[ip_idx] = ip
        # print("itr: {}, reg: {}, instr: {}".format(i, reg, instr))
        reg = functions[instr[0]](reg, instr[1:])
        ip = reg[ip_idx] + 1
        # print("itr: {}, reg: {}, instr: {}".format(i, reg, instr))
        i += 1
        print(i)
    return reg


def main():

    #   data = read_input('day19_input')
    data = read_input("day19_aasmund")
    start, operations = parse_data(data)
    register = run_program(start, operations)
    print("register: {}".format(register))
    # [3, 256, 1003, 3, 1, 3]
    # [1080, 256, 1003, 1004, 1, 1004]
    # tested with 3
    # sum([x for x in range(1,1004) if 1004%x==0]) + 1004 = 1764 <-- too low


class Test(unittest.TestCase):
    def test_basic_functions(self):
        reg = [3, 2, 1, 1]
        instr = [2, 1, 2]
        check_val = [3, 2, 2, 1]
        works = []
        for name, f in functions.items():
            test = reg.copy()
            test = f(test, instr)
            if test == check_val:
                works.append(name)
        assert len(works) == 3
        assert "mulr" in works
        assert "addi" in works
        assert "seti" in works

    def test(self):
        data = read_input("day19_testinput")
        start, operations = parse_data(data)
        register = run_program(start, operations)
        assert register == [6, 5, 6, 0, 0, 9]

    def test_simple(self):
        reg = [3, 2, 1, 1]
        reg = functions["addr"](reg, [1, 0, 1])
        print(reg)


if __name__ == "__main__":
    # unittest.main()
    main()
