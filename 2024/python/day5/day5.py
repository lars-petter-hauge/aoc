from pathlib import Path
from re import sub

TEST_INPUT="""47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47"""


def load():
    with open(Path(__file__).parent / "input.in") as fh:
        lines = fh.readlines()
    return lines

def parse_line(lines):
    from collections import defaultdict
    graph = defaultdict(list)
    updates = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if "|" in line:
            a,b = line.split("|")
            graph[a].append(b)
        else:
            updates.append(line.split(","))
    return graph, updates

def solve(graph,updates):
    correctly, incorrectly = [],[]
    for update in updates:
        valid = True
        for elem in update:
            subsequents = graph.get(elem,[])
            elem_pos = update.index(elem)
            for sub in subsequents:
                if sub not in update:
                    continue
                if update.index(sub)<elem_pos:
                    valid = False
                    incorrectly.append(update)
                    break
            if not valid:
                break
        if valid:
            correctly.append(update)
    return correctly, incorrectly


def sort_em(graph, updates):
    result = []
    for update in updates:
        sorted = []
        new_graph = {}
        for entry in update:
            new_graph[entry] = [x for x in update if x in graph.get(entry,[])]
        for entry in update:
            if entry in new_graph:
                continue
            sorted.append(entry)
            update.remove(entry)
        while update:
            for key, values in new_graph.items():
                if key in sorted:
                    continue
                if all([x in sorted for x in values]):
                    sorted.append(key)
                    update.remove(key)
                    break
        result.append(list(reversed(sorted)))
    return result

graph, updates = parse_line(TEST_INPUT.split('\n'))
correctly, incorrectly = solve(graph, updates)
sorted_updates = sort_em(graph, incorrectly)

print(sum([int(entry[len(entry)//2]) for entry in correctly]))
print(sum([int(entry[len(entry)//2]) for entry in sorted_updates]))


graph, updates = parse_line(load())
correctly, incorrectly = solve(graph, updates)
sorted_updates = sort_em(graph, incorrectly)

print(sum([int(entry[len(entry)//2]) for entry in correctly]))
print(sum([int(entry[len(entry)//2]) for entry in sorted_updates]))
