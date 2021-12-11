from collections import namedtuple

TEST_DATA = """F10
N3
F7
R90
F11"""

Location = namedtuple("point", ["NS", "EW"])


def load(fname):
    with open(fname) as fh:
        lines = fh.readlines()
    return lines


def parse(lines):
    return [(l[0], int(l[1:])) for l in lines]


def move_direction(direction, value, location):
    if direction == "N":
        return Location(NS=location.NS + value, EW=location.EW)
    if direction == "E":
        return Location(NS=location.NS, EW=location.EW + value)
    if direction == "S":
        return Location(NS=location.NS - value, EW=location.EW)
    if direction == "W":
        return Location(NS=location.NS, EW=location.EW - value)
    raise NotImplementedError("Unknown direction")


def rotate_around_point(location, direction):
    if location == Location(0, 0):
        return location

    if direction == "R":
        return Location(NS=-location.EW, EW=location.NS)
    elif direction == "L":
        return Location(NS=location.EW, EW=-location.NS)
    else:
        raise ValueError("Missing direction")


def simulate_part_one(instructions):
    location = Location(0, 0)
    face_direction = "E"
    directions = ["N", "E", "S", "W"]

    for direction, value in instructions:

        if direction == "R":
            face_direction = directions[
                (directions.index(face_direction) + int(value / 90)) % len(directions)
            ]
        elif direction == "L":
            face_direction = directions[
                (directions.index(face_direction) - int(value / 90)) % len(directions)
            ]
        elif direction == "F":
            location = move_direction(face_direction, value, location)
        else:
            location = move_direction(direction, value, location)
    return location


def simulate_part_two(instructions):
    ship_location = Location(0, 0)
    waypoint = Location(1, 10)

    for direction, value in instructions:
        if direction in ["R", "L"]:
            for _ in range(int(value / 90)):
                waypoint = rotate_around_point(waypoint, direction)
        elif direction == "F":
            for _ in range(value):
                ship_location = Location(
                    NS=ship_location.NS + waypoint.NS, EW=ship_location.EW + waypoint.EW
                )
        else:
            waypoint = move_direction(direction, value, waypoint)
    return ship_location


if __name__ == "__main__":
    location = simulate_part_one(parse(TEST_DATA.split("\n")))
    assert location.EW == 17
    assert location.NS == -8

    location = simulate_part_one(parse(load("input.txt")))
    print(abs(location[0]) + abs(location[1]))

    assert rotate_around_point(Location(NS=4, EW=10), "R") == Location(NS=-10, EW=4)

    assert rotate_around_point(Location(1, 10), "R") == Location(-10, 1)
    assert rotate_around_point(Location(1, -10), "R") == Location(10, 1)
    assert rotate_around_point(Location(-10, 1), "R") == Location(-1, -10)
    assert rotate_around_point(Location(-10, -1), "R") == Location(1, -10)

    assert rotate_around_point(Location(1, 10), "L") == Location(10, -1)
    assert rotate_around_point(Location(1, -10), "L") == Location(-10, -1)
    assert rotate_around_point(Location(-10, 1), "L") == Location(1, 10)
    assert rotate_around_point(Location(-10, -1), "L") == Location(-1, 10)

    location = simulate_part_two(parse(TEST_DATA.split("\n")))
    assert location.EW == 214
    assert location.NS == -72

    location = simulate_part_two(parse(load("input.txt")))
    print(abs(location[0]) + abs(location[1]))
