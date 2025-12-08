import sys
import math

from itertools import zip_longest

TEST = """123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  """

content = TEST
content = sys.stdin.read()
values = []
operators = []
for line in content.splitlines():
    try:
        values.append([int(c) for c in line.split()])
    except ValueError:
        operators = line.split()
result = 0

for i in range(len(values[0])):
    column = [row[i] for row in values]
    if operators[i] == "+":
        result += sum(column)
    elif operators[i] == "*":
        result += math.prod(column)
    else:
        raise ValueError()

print(result)

something = content.splitlines()
operator = None
numbers = []
result = 0
for i in range(len(something[0])):
    column = [row[i] for row in something]
    if column[-1] in ["*", "+"]:
        operator = column[-1]
    try:
        numbers.append(int("".join([c for c in column[:-1] if c.isdigit()])))
    except ValueError:
        # we hit a column with all whitespace, time to apply operator
        if operator == "+":
            print(f"Summing {numbers}")
            result += sum(numbers)
        elif operator == "*":
            print(f"multiplying {numbers}")
            result += math.prod(numbers)
        numbers = []

if operator == "+":
    print(f"Summing {numbers}")
    result += sum(numbers)
elif operator == "*":
    print(f"multiplying {numbers}")
    result += math.prod(numbers)
print(result)
