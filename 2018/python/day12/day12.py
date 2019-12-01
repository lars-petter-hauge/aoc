import unittest

def parse_data(input):
    parsed = []
    init = input[0][15:].split()[0]
    for line in input[2:]:
        rule = line[0:5]
        pot = True if line[9] == '#' else False
        parsed.append((rule, pot))
    return init, parsed


def read_input(fname):
    with open(fname) as f:
        input = f.readlines()
    return input


def will_get_pot(sequence, rules):
    for rule, pot in rules:
        if rule == sequence:
            return pot
    return False


def grow_plants(init, rules):
    plants = init.count('#')
    state = '..........' + init + '.'*1000 # provide som extra pots
    generations = []
    generations.append(state)
    stripped_generations = []
    for gen in range(200):
        new_state = []
        for i, x in enumerate(state):
            if i > len(state)-2 or i < 2:
                new_state.append('.')
                continue
            if will_get_pot(state[i-2:i+3], rules):
                new_state.append('#')
            else:
                new_state.append('.')
        new_state = ''.join(new_state)
        #if new_state.strip('.') in stripped_generations:
        #    print("generation {} already seen".format(gen)) #153
        #    break
        print("gen: {}, state: {}, value: {}".format(gen,state.strip('.'), add_numbered_pots(new_state)))
        generations.append(new_state)
        stripped_generations.append(new_state.strip('.'))
        plants += new_state.count('#')
        state = new_state
    return plants, generations

def add_numbered_pots(state, leftmost = -10):
    number = 0
    for i,x in enumerate(state):
        if x=='#':
            value = i + leftmost
            number += value
    return number


class Test(unittest.TestCase):
    def test(self):
        data = read_input('day12testinput')
        init, parsed = parse_data(data)
        plants, generations = grow_plants(init, parsed)
        with open('day12testfasit') as f:
            input = f.readlines()
        for i, line in enumerate(input):
            #print("gen {}: {} \ngen {}: {}\n".format(i,line.split()[0],i,generations[i]))
            assert line.split()[0] == generations[i]
        assert add_numbered_pots(generations[20]) == 325

    def test_jpb(self):
        data = read_input('day12_jpb')
        init, parsed = parse_data(data)
        plants, generations = grow_plants(init, parsed)
        print("jpb")
        for i, generation in enumerate(generations):
            print("gen: {}, pots: {}".format(i, add_numbered_pots(generation)))
        with open('day12_jpb_fasit') as f:
            input = f.readlines()
        for i, line in enumerate(input):
            print("gen {}: {} \ngen {}: {}\n".format(i+1,line.split()[0],i+1,generations[i+1]))
        print(add_numbered_pots(generations[20]))
        assert add_numbered_pots(generations[20]) == 3051



if __name__ == '__main__':
    #unittest.main()
    data = read_input('day12input')
    init, parsed = parse_data(data)
    plants, generations = grow_plants(init, parsed)
    print(add_numbered_pots(generations[170]))
    # 2842 is too high