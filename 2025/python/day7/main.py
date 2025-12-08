import sys
import itertools
import math

TEST = """162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689"""

content = TEST
content = sys.stdin.read()


content = [tuple(map(int, line.split(","))) for line in content.splitlines()]


def calc_distance(source, target):
    return math.sqrt(sum([abs(s - t) ** 2 for s, t in zip(source, target)]))


distances = {(x, y): calc_distance(x, y) for x, y in itertools.combinations(content, 2)}

distances = {k: v for k, v in sorted(distances.items(), key=lambda item: item[1])}

connection_groups = []

for idx, (box_pair, distance) in enumerate(distances.items(), start=1):
    # print(f"Checking pair: {box_pair}")
    something = [
        group
        for group in connection_groups
        if box_pair[0] in group or box_pair[1] in group
    ]
    if len(something) == 2:
        # print(f"Merging: {something}")
        first = connection_groups.pop(connection_groups.index(something[0]))
        second = connection_groups.pop(connection_groups.index(something[1]))
        connection_groups.append(first + second)
    elif len(something) == 1:
        # print(f"Found single group {something[0]}")
        first = connection_groups.pop(connection_groups.index(something[0]))
        if box_pair[0] not in first:
            # print(f"Adding {box_pair[0]} to {first}")
            first = first + (box_pair[0],)
        elif box_pair[1] not in first:
            # print(f"Adding {box_pair[1]} to {first}")
            first = first + (box_pair[1],)
        connection_groups.append(first)
    else:
        # print("neither in group, adding as a new group")
        connection_groups.append(box_pair)
    if len(connection_groups) == 1 and len(connection_groups[0]) == len(content):
        print("All in one group")
        print(box_pair[0][0] * box_pair[1][0])
        break
    # if idx==1000:
    #     break


connection_groups = sorted(connection_groups, key=len, reverse=True)[:3]

print(math.prod([len(g) for g in connection_groups]))
