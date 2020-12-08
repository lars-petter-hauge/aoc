from collections import defaultdict, deque


def load_input(fname):
    with open(fname) as f:
        lines = f.readlines()
    return [l.strip() for l in lines]


def create_tree(data):
    orbit_tree = defaultdict(list)
    for relation in data:
        a, b = relation.split(")")
        orbit_tree[a].append(b)
    return orbit_tree


def count_orbits(tree, base="COM"):
    queue = deque()
    queue.append(base)

    level = {base: 0}
    while queue:
        root = queue.pop()
        if root in tree:
            nodes = tree[root]
            for node in nodes:
                level[node] = level[root] + 1
            queue.extend(nodes)

    return sum(level.values())


def minimum_distance(tree, start="YOU", stop="SAN"):
    queue = deque()
    queue.append(start)

    distance = {start: 0}
    seen = set([start])
    while queue:
        root = queue.pop()
        if root == stop:
            return distance[root] - 2
        neighbours = tree.get(root, [])
        neighbours.extend([k for k, v in tree.items() if root in v])
        neighbours = set([n for n in neighbours if n not in seen])
        for neighbour in neighbours:
            distance[neighbour] = distance[root] + 1
            seen.add(neighbour)
        queue.extend(neighbours)
    return None


def run_tests():
    orbit_map = [
        "COM)B",
        "B)C",
        "C)D",
        "D)E",
        "E)F",
        "B)G",
        "G)H",
        "D)I",
        "E)J",
        "J)K",
        "K)L",
    ]
    tree = create_tree(orbit_map)
    assert 42 == count_orbits(tree)

    orbit_map = [
        "COM)B",
        "B)C",
        "C)D",
        "D)E",
        "E)F",
        "B)G",
        "G)H",
        "D)I",
        "D)M",
        "E)J",
        "J)K",
        "K)L",
    ]
    tree = create_tree(orbit_map)
    assert 46 == count_orbits(tree)

    orbit_map = [
        "COM)B",
        "B)C",
        "C)D",
        "D)E",
        "E)F",
        "B)G",
        "G)H",
        "D)I",
        "E)J",
        "J)K",
        "K)L",
        "K)YOU",
        "I)SAN",
    ]
    tree = create_tree(orbit_map)
    assert 4 == minimum_distance(tree)


def run(data):
    tree = create_tree(data)
    print(
        "Number of orbits: {}. Orbital jumps required: {}".format(
            count_orbits(tree), minimum_distance(tree)
        )
    )


if __name__ == "__main__":
    run_tests()
    run(load_input("day6/input.txt"))
