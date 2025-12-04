import sys


TEST = """987654321111111
811111111111119
234234234234278
818181911112111"""


content = TEST

content = sys.stdin.read()


def max_jolt(bank, level):
    draw_from = bank[:-level] if level != 0 else bank
    largest = str(max([int(c) for c in draw_from]))
    if level == 0:
        return largest
    return largest + max_jolt(bank[bank.index(largest) + 1 :], level - 1)


voltage = []
for bank in content.splitlines():
    voltage.append(int(max_jolt(bank, 11)))

print(sum(voltage))
