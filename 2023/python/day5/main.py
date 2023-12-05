TEST_DATA = """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
"""


def load_input(fname):
    with open(fname) as fh:
        return fh.readlines()


def parse_lines(lines):
    result = {}
    map_name = None
    ranges = []
    seeds = ""
    for line in lines:
        line = line.strip()
        if line == "":
            continue
        elif line.startswith("seeds"):
            _, seeds = line.split(":")
            seeds = [int(x.strip()) for x in seeds.split() if x != " "]
            continue
        elif "map" in line:
            if map_name is not None:
                result[map_name] = ranges
                ranges = []
            source, destination = line.split("-to-")
            destination = destination[:-5]
            map_name = (source, destination)
            continue
        else:
            destination, source, range_len = (int(v) for v in line.split())
            ranges.append(
                (
                    range(source, source + range_len),
                    range(destination, destination + range_len),
                )
            )
    # Add last entry
    result[map_name] = ranges
    return seeds, result


def evaluate_map(number, source, maps):
    destination = ""
    ranges = []
    for key, value in maps.items():
        if key[0] == source:
            ranges = value
            destination = key[1]
            break

    available_range = [r for r in ranges if number in r[0]]
    if available_range:
        source_range, dest_range = available_range[0]
        number = dest_range[source_range.index(number)]

    if destination == "location":
        return number

    for key in maps.keys():
        if key[0] == destination:
            source = destination
            destination = key[1]
            break

    return evaluate_map(number, source, maps)


seeds, maps = parse_lines(TEST_DATA.split("\n"))
result = {seed: evaluate_map(seed, source="seed", maps=maps) for seed in seeds}
result = {k: v for k, v in sorted(result.items(), key=lambda item: item[1])}
print(
    [
        f"seed: {seed} loc: {evaluate_map(seed, source='seed', maps=maps)}"
        for seed in seeds
    ]
)

seeds, maps = parse_lines(load_input("input.txt"))
result = {seed: evaluate_map(seed, source="seed", maps=maps) for seed in seeds}
result = {k: v for k, v in sorted(result.items(), key=lambda item: item[1])}
print(
    [
        f"seed: {seed} loc: {evaluate_map(seed, source='seed', maps=maps)}"
        for seed in seeds
    ]
)

# The ranges are linearly mapped, take the smallest delta range among all
# maps to search with
delta = 9999999999999
for _, ranges in maps.items():
    for rang in ranges:
        delta = min(delta, rang[0][-1] - rang[0][0])

# Make sure we're not on an edge (could be less, but doesn't matter much)
delta = int(delta / 2)

# Create ranges as specified
ranges = [
    range(begin, begin + length) for begin, length in zip(seeds[::2], seeds[1::2])
]
best_location = 9999999999
best_range = None
best_seed = -1
# Find range that contains best seed
for rang in ranges:
    number = rang[0]
    end = rang[-1]
    print(f"At ranges {rang}")
    while number <= end:
        location = evaluate_map(number, "seed", maps)
        if location < best_location:
            print(f"found better for seed {number}: {location}")
            best_location = location
            best_range = rang
            best_seed = number
        number += delta

# Time to hone in
delta = 10000
while delta > 1:
    seed = best_seed - delta
    location = evaluate_map(seed, "seed", maps)

    if location < best_location:
        best_location = location
        best_seed = seed
        print(f"Improved location {location} using seed {seed}")
    else:
        delta = delta // 2
        print(f"We went too far, reducing to {delta} at seed {seed}")
