import sys

stdin = sys.stdin.read()

TEST = """L68
L30
R48
L5
R60
L55
L1
L99
R14
L82"""

# stdin = TEST

dial = 50
p1 = 0
p2 = 0

for turn in stdin.splitlines():
    d = turn[0]
    length = int(turn[1:])
    for _ in range(length):
        if d == "L":
            dial = (dial - 1) % 100
        else:
            dial = (dial + 1) % 100

        if dial == 0:
            p2 += 1

    if dial == 0:
        p1 += 1

print(p1)
print(p2)
