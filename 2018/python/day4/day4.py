import unittest
from datetime import datetime
from operator import itemgetter


def parse_data(input):
    parsed = []
    for line in input:
        date = line[1:17]
        date = datetime.strptime(date, "%Y-%m-%d %H:%M")
        if line[19] == "f" or line[19] == "w":
            parsed.append((date, line[19]))
            continue
        parsed.append((date, int(line[26:].split()[0])))
    parsed.sort(key=itemgetter(0))
    return parsed


def read_input(fname):
    with open(fname) as f:
        input = f.readlines()
    return input


def calc_sleep_time(schedule):
    """
    Returns a dict with sleep times per guard as a start, end, duration
    """
    guard = 0
    sleep_times = {}
    start = None
    end = None
    for sch in schedule:
        if isinstance(sch[1], int):
            guard = sch[1]
            continue
        if sch[1] == "f":
            start = sch[0]
            continue
        end = sch[0]
        if guard not in sleep_times:
            sleep_times[guard] = []
        sleep_times[guard].append({"start": start, "end": end, "duration": end - start})
    return sleep_times


def calc_total_sleep(sleep_times):
    total = {}
    for guard, list_of_times in sleep_times.items():
        for sleep in list_of_times:
            if guard not in total:
                total[guard] = sleep["duration"]
                continue
            total[guard] += sleep["duration"]
    return total


def guard_longest_sleep(total_times):
    return max(total_times.items(), key=itemgetter(1))[0]


def minute_most_sleep(guard, sleep_times):
    slept = {}
    for sleep in sleep_times:
        for minute in range(sleep["start"].minute, sleep["end"].minute):
            if minute not in slept:
                slept[minute] = 1
                continue
            slept[minute] += 1
    minute = max(slept.items(), key=itemgetter(1))[0]
    return minute, slept[minute]


def minute_guard_most_freq_asleep(sleep_times):
    slept = {}
    max_amount = 0
    for guard, list_of_times in sleep_times.items():
        minute, amount = minute_most_sleep(guard, list_of_times)
        if amount > max_amount:
            max_amount = amount
            guard_max = guard
            min_max = minute
    return guard_max, min_max, max_amount


def main(data):
    sleep_times = calc_sleep_time(parsed)
    total = calc_total_sleep(sleep_times)
    guard = guard_longest_sleep(total)
    minute, amount = minute_most_sleep(guard, sleep_times[guard])
    print(
        "Guard {} slept longest the minute: {}. Multiplied: {}".format(
            guard, minute, guard * minute
        )
    )
    guard, minute, amount = minute_guard_most_freq_asleep(sleep_times)
    print(
        "Guard {} slept the most frequent at minute {}. Multipled {}".format(
            guard, minute, guard * minute
        )
    )


class Test(unittest.TestCase):
    def test(self):
        input = read_input("day4_testinput")
        parsed = parse_data(input)
        sleep_times = calc_sleep_time(parsed)
        total = calc_total_sleep(sleep_times)
        guard = guard_longest_sleep(total)
        minute, amount = minute_most_sleep(guard, sleep_times[guard])
        assert guard == 10
        assert minute == 24

        guard, minute, amount = minute_guard_most_freq_asleep(sleep_times)
        assert guard == 99
        assert minute == 45
        assert amount == 3


if __name__ == "__main__":
    # unittest.main()
    input = read_input("day4input")
    parsed = parse_data(input)
    main(parsed)
