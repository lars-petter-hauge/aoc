from collections import deque

# graphviz
import networkx as nx


def parse(lines):
    all_bags = {}
    for l in lines:
        record = {}
        sep_idx = l.find("contain")
        key = l[: sep_idx - 6]
        assert key not in all_bags
        if "no other bags" in l:
            all_bags[key] = record
            continue

        contents = l[sep_idx + 7 :]
        for content in contents.split(","):
            # parse everything but the number and split bag/bags
            bag = content[3:].rsplit(" ", 1)[0]
            record[bag] = int(content[1])
        all_bags[key] = record
    return all_bags


def load(fname):
    with open(fname) as fh:
        lines = fh.readlines()
    lines = [l.strip() for l in lines]

    return lines


def dfs(data, start, possible_bags):
    queue = deque()
    queue.append(start)
    seen = set()
    while queue:
        bag = queue.pop()
        if bag in seen:
            remaining_keys = data.keys() - seen
            if remaining_keys:
                queue.append(remaining_keys.pop())
            continue

        seen.add(bag)
        for key in data[bag].keys():
            queue.append(key)
            if key in possible_bags:
                possible_bags.add(bag)

        if not queue:
            remaining_keys = data.keys() - seen
            if remaining_keys:
                queue.append(remaining_keys.pop())
    return possible_bags


def count_bags(data, key):
    total_count = 1
    for bag, count in data[key].items():
        if len(data[bag]) == 0:
            total_count += count
        else:
            total_count += count_bags(data, bag) * count
    return total_count


def count_possible_bags(data):
    key = list(data.keys())[0]
    possible_bags = {"shiny gold"}
    length = 0
    while len(possible_bags) > length:
        length = len(possible_bags)
        possible_bags = dfs(data, key, possible_bags)
    possible_bags.remove("shiny gold")
    return len(possible_bags)

    # graph_dict = {key: list(value.keys()) for key, value in data.items() if len(value.keys())>0}
    # graph_dict_works = {key: list(value.keys()) for key, value in data.items()}
    # graph = nx.Graph()
    # graph.add_nodes_from(graph_dict)
    # print(possible_bags)
    # print(len(possible_bags))


TEST = """
light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags.
"""

TEST_TWO = """
shiny gold bags contain 2 dark red bags.
dark red bags contain 2 dark orange bags.
dark orange bags contain 2 dark yellow bags.
dark yellow bags contain 2 dark green bags.
dark green bags contain 2 dark blue bags.
dark blue bags contain 2 dark violet bags.
dark violet bags contain no other bags.
"""

if __name__ == "__main__":
    test_data = parse(TEST.split("\n")[1:-1])
    assert count_possible_bags(test_data) == 4
    assert count_bags(test_data, "shiny gold") - 1 == 32

    test_data = parse(TEST_TWO.split("\n")[1:-1])
    assert count_bags(test_data, "shiny gold") - 1 == 126

    data = parse(load("2020/python/day6/input.txt"))
    print(count_possible_bags(data))
    print(count_bags(data, "shiny gold") - 1)
