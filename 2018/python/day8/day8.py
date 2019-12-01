import unittest
 
def parse_data(data):
    data = [int(i) for i in data[0].split()]
    return data

def read_input(fname):
    with open(fname) as f:
        data=f.readlines()
    return data

def evaluate_node(data):
    children = data[0]
    metadata = data[1]
    offset = 2
    value = 0
    for child in range(children):
        skips, val = evaluate_node(data[offset:])
        offset += skips
        value += val

    for meta in range(metadata):
        value += data[offset]
        offset += 1

    return offset, value

def evaluate_node_part2(data):
    children = data[0]
    metadata = data[1]
    offset = 2
    value = 0
    values = []
    for child in range(children):
        skips, val = evaluate_node_part2(data[offset:])
        offset += skips
        values.append(val)

   # if data == [2, 3, 0, 3, 10, 11, 12, 1, 1, 0, 1, 99, 2, 1, 1, 2]:
    #    import pdb; pdb.set_trace()
    for meta in range(metadata):
        if children == 0:
            value += data[offset]
        else:
            idx = data[offset] - 1
            if idx<len(values):
                value += values[idx]
        offset += 1
    return offset, value

class Test(unittest.TestCase):
    def test(self):
        sequence = '2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2'
        sequence = [int(s) for s in sequence.split()]

        offset, value = evaluate_node(sequence)
        print("offset: {}, value: {}".format(offset, value))
        assert value == 138
        offset, value = evaluate_node_part2(sequence)
        print("part two")
        print("offset: {}, value: {}".format(offset, value))
        assert value == 66

if __name__ == '__main__':
    #unittest.main()
    data = read_input('day8input')
    parsed = parse_data(data)
    offset, value = evaluate_node_part2(parsed)
    print("Value: {}".format(value))

    #main(data)
