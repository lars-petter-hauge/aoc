TEST_DATA="""939
7,13,x,x,59,x,31,19"""

import math

def load(fname):
    with open(fname) as fh:
        lines = fh.readlines()
    return lines


def parse(lines):
    departure_time=int(lines[0])
    def int_if(value):
        if value == "x":
            return value
        return int(value)

    bus_ids = [int_if(x) for x in lines[1].split(",")]
    return departure_time, bus_ids


def run(departure_time, bus_ids):
    earliest = 999999999999999999
    correct_id = 0
    waiting_time = 0
    for bus in bus_ids:
        departure = math.ceil(departure_time/bus)
        departure = departure*bus
        if departure<earliest:
            earliest=departure
            correct_id = bus
            waiting_time =  departure - departure_time
    return correct_id, waiting_time


def calculate_misfit(departure_time, bus_ids):
    misfit_times = []
    for bus in bus_ids:
        if bus == "x":
            misfit_times.append(0)
            departure_time += 1
            continue

        departure = (math.ceil(departure_time/bus)) * bus

        misfit_times.append(departure - departure_time)
        departure_time += 1
    return misfit_times


if __name__ == "__main__":
    departure_time, bus_ids = parse(TEST_DATA.split("\n"))
    bus_ids = [x for x in bus_ids if x != "x"]
    bus_id, waiting_time = run(departure_time, bus_ids)
    assert bus_id == 59
    assert waiting_time == 5
    departure_time, bus_ids = parse(load("input.txt"))
    bus_ids = [x for x in bus_ids if x != "x"]

    bus_id, waiting_time = run(departure_time, bus_ids)

    departure_time, bus_ids = parse(load("input.txt"))

    print(waiting_time*bus_id)
    print(calculate_misfit(departure_time, bus_ids))

