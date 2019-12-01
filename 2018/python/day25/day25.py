import unittest

def read_data(fname):
    with open(fname) as f:
        lines = f.readlines()
    result = [[int(x) for x in l.split(',')] for l in lines]
    return result

def inrange(x, y):
    return (abs(x[0]-y[0])+abs(x[1]-y[1])+abs(x[2]-y[2])+abs(x[3]-y[3])) <= 3

def inrange_of_const(star, consts):
    inrange_consts = []
    for const in consts.keys():
        for check_star in consts[const]:
            if inrange(star, check_star):
                inrange_consts.append(const)
                break
    return inrange_consts

def collapse_consts(consts, collapse):
    for i in range(1,len(collapse)):
        consts[collapse[0]] = consts[collapse[0]] + consts[collapse[i]]
        consts.pop(collapse[i])
    return consts

def verify_constellations(consts, stars):
    for star in stars:
        inrange_consts = inrange_of_const(star, consts)
        if len(inrange_consts) > 1:
            consts = collapse_consts(consts, inrange_consts)
    return consts

def constellations(data):
    consts = {}
    i = 0
    for star in data:
        inrange_consts = inrange_of_const(star, consts)
        if len(inrange_consts) == 0:
            consts[i] = [star]
            i += 1
            continue
        if len(inrange_consts) == 1:
            consts[inrange_consts[0]] = consts[inrange_consts[0]] + [star]
            continue
        consts = collapse_consts(consts, inrange_consts)
        consts[inrange_consts[0]] = consts[inrange_consts[0]] + [star]
    return consts


def nelems(d):
    n = 0
    for k, v in d.items():
        n += len(v)
    return n

class Test(unittest.TestCase):
    def test1(self):
        data = [[-1,2,2,0],
        [0,0,2,-2],
        [0,0,0,-2],
        [-1,2,0,0],
        [-2,-2,-2,2],
        [3,0,2,-1],
        [-1,3,2,2],
        [-1,0,-1,0],
        [0,2,1,-2],
        [3,0,0,0]]
        assert len(constellations(data)) == 4

    def test2(self):
        data = [[1,-1,0,1],
        [2,0,-1,0],
        [3,2,-1,0],
        [0,0,3,1],
        [0,0,-1,-1],
        [2,3,-2,0],
        [-2,2,0,0],
        [2,-2,0,-1],
        [1,-1,0,-1],
        [3,2,0,2]]
        assert len(constellations(data)) == 3

    def test3(self):
        data = [[1,-1,-1,-2],
        [-2,-2,0,1],
        [0,2,1,3],
        [-2,3,-2,1],
        [0,2,3,-2],
        [-1,-1,1,-2],
        [0,-2,-1,0],
        [-2,2,3,-1],
        [1,2,2,0],
        [-1,-2,0,-2]]
        assert len(constellations(data)) == 8

if __name__ == '__main__':
    #unittest.main()
    data = read_data('day25_input.txt')

    consts = constellations(data)
    cur_len = len(consts)
    consts = verify_constellations(consts, data)
    while len(consts) != cur_len:
        cur_len = len(consts)
        consts = verify_constellations(consts, data)

    print(len(consts))