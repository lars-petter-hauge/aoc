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


def search_closing(path):
    brackets = 0
    end = 0
    for i, char in enumerate(path):
        if char == "(":
            brackets += 1
        if char == ")":
            brackets -= 1
        if brackets == 0:
            return i
        end = i
    return end


def order_paths(path):
    print("ordering paths")
    paths = []
    for i, char in enumerate(path):
        path_options = []
        if char in ["E", "N", "S", "W"]:
            paths.append(char)
        elif char == "(":
            idx = search_closing(path[i:])
            path_options = order_paths(path[i + 1 : i + idx])
        elif char == "|":
            path_options = order_paths(path[i + 1 :])
        # elif char == ')':
        #    #if i != len(path):
        #    #    #TODO this will be the option if |) is encountered..
        #    #    print('found breaking bracket before end at: {}'.format(i))
        #    #    raise NotImplementedError
        #    pass
        # else:
        #    print('No operator for: {}'.format(char))
        #    raise NotImplementedError
        if path_options:
            new_paths = []
            new_paths.append(paths)
            for option in path_options:
                new_paths.append(option)
            paths = [paths.extend(option) for option in path_options]
        print(paths)
    print("returning: {}".format(paths))
    return paths


def main():
    pass


class Test(unittest.TestCase):
    def test(self):
        reg_path = "^ENWWW(NEEE|SSE(EE|N))$"
        path = [x for x in reg_path]
        paths = order_paths(path[1 : (len(path) - 1)])

        reg_path = "^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$"

        reg_path = "^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$"

        reg_path = "^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$"


if __name__ == "__main__":
    unittest.main()
    main()
