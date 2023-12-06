import math

TEST_DATA = [(7, 9), (15, 40), (30, 200)]
TASK_DATA = [(41, 244), (66, 1047), (72, 1228), (66, 1040)]

# Time = b
# Distance = c


def solve_quadratic(a, b, c):
    d = b**2 - 4 * a * c
    if d == 0:
        return (-b + math.sqrt(d)) / (2 * a)
    else:
        x1 = (-b + math.sqrt(d)) / (2 * a)
        x2 = (-b - math.sqrt(d)) / (2 * a)
        return x1, x2


def solve_race(time_distance):
    # Note, we want to beate the time, hence marginally reduce the time
    # This will avoid tied result shown as a valid answer
    solutions = [
        solve_quadratic(a=-1, b=b * 0.99999999, c=-1 * c) for b, c in time_distance
    ]

    # +1 for inclusive
    solutions = [math.floor(x2) - math.ceil(x1) + 1 for x1, x2 in solutions]
    return math.prod(solutions)


print(solve_race(TEST_DATA))
print(solve_race(TASK_DATA))
print(solve_race([(71530, 940200)]))
print(solve_race([(41667266, 244104712281040)]))
