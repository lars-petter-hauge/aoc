import unittest

def addr(r,i):
    r[i[2]] = r[i[0]] + r[i[1]] 
    return r

def addi(r,i):
    r[i[2]] = r[i[0]] + i[1]
    return r

def mulr(r,i):
    r[i[2]] = r[i[0]] * r[i[1]] 
    return r

def muli(r,i):
    r[i[2]] = r[i[0]] * i[1]
    return r

def banr(r,i):
    r[i[2]] = r[i[0]] & r[i[1]] 
    return r

def bani(r,i):
    r[i[2]] = r[i[0]] & i[1]
    return r

def borr(r,i):
    r[i[2]] = r[i[0]] | r[i[1]] 
    return r

def bori(r,i):
    r[i[2]] = r[i[0]] | i[1]
    return r

def setr(r,i):
    r[i[2]] = r[i[0]]
    return r

def seti(r,i):
    r[i[2]] = i[0]
    return r

def gtir(r,i):
    r[i[2]] = int(i[0] > r[i[1]])
    return r

def gtri(r,i):
    r[i[2]] = int(r[i[0]] > i[1])
    return r

def gtrr(r,i):
    r[i[2]] = int(r[i[0]] > r[i[1]])
    return r

def eqir(r,i):
    r[i[2]] = int(i[0] == r[i[1]]) 
    return r

def eqri(r,i):
    r[i[2]] = int(r[i[0]] == i[1])
    return r

def eqrr(r,i):
    r[i[2]] = int(r[i[0]] == r[i[1]])
    return r

functions = { 'addr': addr,
              'addi': addi,
              'mulr': mulr,
              'muli': muli,
              'bani': bani,
              'banr': banr,
              'bori': bori,
              'borr': borr,
              'seti': seti,
              'setr': setr,
              'gtir': gtir,
              'gtri': gtri,
              'gtrr': gtrr,
              'eqrr': eqrr,
              'eqri': eqri,
              'eqir': eqir,
}

def parse_data(lines):
    ip = int(lines[0][4])
    instructions = []
    for line in lines[1:]:
        line = line.strip()
        result = [int(x) for x in line[5:].split(' ')]
        instr = [line[:4]]
        instr.extend(result)
        instructions.append(instr)
    return ip, instructions

def read_data(fname):
    with open(fname) as f:
        result = f.readlines()
    return result

def run(r_col, instructions, reg_one=0):
    reg = [0, 0, 0, 0, 0, 0]
    ip = 0
    i = 0
    while ip < len(instructions):
        instr = instructions[ip]
        reg = functions[instr[0]](reg, instr[1:])
        reg[r_col] = reg[r_col] + 1
        ip = reg[r_col]
        print(i)
        i += 1
    return reg

class Test(unittest.TestCase):
    def test_day19(self):
        data = read_data('day19_input')
        ip, instructions = parse_data(data)
        reg = run(ip, instructions)
        assert reg[0] == 1080

def main():
    data = read_data('day21_input')
    ip, instructions = parse_data(data)
    run(ip, instructions)

if __name__ == '__main__':
    #unittest.main()
    main()