from collections import defaultdict
import sys

TEST = """.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
..............."""


content = TEST
# content = sys.stdin.read()
beams = set([content.splitlines()[0].index("S")])

times_split = 0

for line in content.splitlines()[1:]:
    print(f"------------ checking line: {line}")
    splitters = [idx for idx, c in enumerate(line) if c == "^"]
    print(f"current beams: {beams}")
    print(f"splitters at: {splitters}")
    beams_to_split = [b for b in beams if any([True for s in splitters if b == s])]
    beams_to_add = []
    print(f"beams to split: {beams_to_split}")
    times_split += len(beams_to_split)
    for beam in beams_to_split:
        beams = beams - {beam}
        beams_to_add.extend(
            [beam + delta for delta in [-1, 1] if 0 < beam + delta < len(line)]
        )
    print(beams_to_add)
    beams = beams | set(beams_to_add)

print(times_split)

graph = defaultdict(list)
beam_connections = {(0, 0): [content.splitlines()[0].index("S")]}
for idx, line in enumerate(content.splitlines()[1:]):
    splitters = [idx for idx, c in enumerate(line) if c == "^"]

    for splitter in splitters:
        for old_splitter, beams in beam_connections.items():
            if splitter in beams:
                beams.pop(beams.index(splitter))
                graph[old_splitter].append((idx, splitter))
                beam_connections[old_splitter] = beams

        possible_connections = [
            splitter + delta for delta in [-1, 1] if 0 < splitter + delta < len(line)
        ]
        beam_connections[(idx, splitter)] = possible_connections

for splitter, beams in beam_connections.items():
    if len(beams) == 0:
        continue
    for beam in beams:
        graph[splitter].append(f"GOAL-{beam}")

# todo: count all pathways leading to a goal node
