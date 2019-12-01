import unittest
from itertools import compress
import time

def parse_data(data):
    parsed = [x for x in data]
    return parsed


def read_input(fname):
    with open(fname) as f:
        data = f.readlines()
    return data

def pop_char(data, char):
    i = 0
    while i < len(data)-1:
        if data[i].lower() == char.lower():
            data.pop(i)
            i += -1
        i += 1
    return data

def pop_polars(indata):
    i = 0
    while i < len(indata)-1:
        if _is_polar(indata[i], indata[i+1]):
            indata.pop(i)
            indata.pop(i)
            i += -2
        i += 1
    return indata

def _is_polar(x,y):
    return x.upper() == y.upper() and x != y

def main(data):
    chars = set(data)
    chars = set([x.lower() for x in data])
    lowest_score = 999999
    for char in chars:
        print('checking char: {}'.format(char))
        new_data = pop_char(data.copy(), char)
        result = pop_polars(new_data)
        if len(result) < lowest_score:
            lowest_char = char
            lowest_score = len(result)
    print('lowest char: {}, with score: {}'.format(lowest_char, lowest_score))

class Test(unittest.TestCase):
    def test(self):
        mystr= 'dabAcCaCBAcCcaDA'
        parsed = parse_data(mystr)
        assert "".join(pop_polars(parsed.copy())) == 'dabCBAcaDA'

        new_data = pop_char(parsed.copy(), 'b')
        result = pop_polars(new_data)
        assert 'daCAcaDA'== "".join(result)

        new_data = pop_char(parsed.copy(), 'c')
        result = pop_polars(new_data)
        assert 'daDA'== "".join(result)

        new_data = pop_char(parsed.copy(), 'd')
        result = pop_polars(new_data)
        assert 'daDA'== "".join(result)

        new_data = pop_char(parsed.copy(), 'a')
        result = pop_polars(new_data)
        assert 'dbCBcD' == "".join(result)

if __name__ == '__main__':
   # unittest.main()
    data = read_input('day5input')
    start = time.time()
    parsed = parse_data(data[0])
    result = main(parsed)
    print('took: {} seconds'.format(time.time()-start))
