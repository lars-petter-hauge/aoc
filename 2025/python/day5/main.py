import sys


TEST = """3-5
10-14
16-20
12-18

1
5
8
11
17
32"""


# content = TEST

content = sys.stdin.read()


def parse(lines):
    intervals, ingredients = lines.split("\n\n")

    intervals = [
        (int(i.split("-")[0]), int(i.split("-")[1]))
        for i in intervals.split("\n")
        if len(i) > 0
    ]
    ingredients = [int(i) for i in ingredients.split("\n") if len(i) > 0]
    return intervals, ingredients


def within_interval(number, intervals):
    for interval in intervals:
        if number >= interval[0] and number <= interval[1]:
            return True
    return False


intervals, ingredients = parse(content)

intervals = sorted(intervals)

print(len(list(filter(lambda x: within_interval(x, intervals), ingredients))))

new_intervals = [intervals[0]]

for next_interval in intervals[1:]:
    previous_interval = new_intervals.pop()
    # completely outside, just add
    if next_interval[0] > previous_interval[1]:
        new_intervals.append(previous_interval)
        new_intervals.append(next_interval)
        continue

    # expand if necessary
    previous_interval = (
        previous_interval[0],
        max(previous_interval[1], next_interval[1]),
    )
    new_intervals.append(previous_interval)

print(sum([stop - start + 1 for start, stop in new_intervals]))
