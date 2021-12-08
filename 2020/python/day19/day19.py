from collections import defaultdict
import itertools
flatten = itertools.chain.from_iterable

TEST_DATA = """0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

ababbb
bababa
abbbab
aaabbb
aaaabbb"""

def load(fname):
    with open(fname) as fh:
        lines = fh.read()

    lines = lines.split("\n")
    return lines

def parse(lines, split_line=138):
    rules = defaultdict(list)
    for line in lines[:split_line]:
        split_on = line.find(":")
        name = line[:split_on]
        if line.endswith('"a"'):
            rules[name] = [['a']]
            continue
        if line.endswith('"b"'):
            rules[name] = [['b']]
            continue
        for possible_definition in line[split_on+2:].split("|"):
            rules[name].append(possible_definition.split())

    messages = lines[split_line+1:]

    return rules, messages

def evaluate_rules(rules, cached=None, current_rule=None):
    if current_rule is None:
        current_rule = list(rules.keys())[0]
    if cached is None:
        cached = {}

    options = rules[current_rule]

    if options == [['a']] or options == [['b']]:
        cached[current_rule] = options
        return options, cached

    acceptable_messages = []
    for option in options:
        sub_req = []
        for rule in option:
            evaluated = cached.get(rule)
            if evaluated is None:
                evaluated, _ = evaluate_rules(rules, cached=cached, current_rule=rule)
            sub_req.append(list(flatten(evaluated)))

        required = ["".join(m) for m in list(itertools.product(*sub_req))]
        acceptable_messages.append(["".join(m) for m in required])

    cached[current_rule] = acceptable_messages
    return acceptable_messages, cached

def run(rules, messages):
    accepted_messages, cached = evaluate_rules(rules, current_rule='0')
    accepted_messages = list(flatten(accepted_messages))
    return sum([1 for msg in messages if msg in accepted_messages])

if __name__ == "__main__":
    rules, message = parse(TEST_DATA.split("\n"), split_line=6)
    assert evaluate_rules(rules, current_rule='4')[0] == [['a']]
    assert evaluate_rules(rules, current_rule='5')[0] == [['b']]
    assert evaluate_rules(rules, current_rule='2')[0] == [['aa'], ['bb']]
    assert evaluate_rules(rules, current_rule='3')[0] == [['ab'], ['ba']]
    assert evaluate_rules(rules, current_rule='1')[0] == [['aaab', 'aaba', 'bbab', 'bbba'], ['abaa', 'abbb', 'baaa', 'babb']]
    assert evaluate_rules(rules, current_rule='0')[0] == [['aaaabb', 'aaabab', 'abbabb', 'abbbab', 'aabaab', 'aabbbb', 'abaaab', 'ababbb']]
    rules, messages = parse(load("2020/python/day19/input.txt"))
    print(run(rules, messages))
    rules['8'] = [['42'], ['42', '8']]
    rules['11'] = [['42', '31'], ['42', '11', '31']]
    run(rules, messages)

  # """ 8: 42 | 42 8
#11: 42 31 | 42 11 31
#"""