from copy import copy
import itertools

from intcode_computer import parse_input
from intcode_computer import IntCodeComputer


def run(controller_input, phase_settings):
    input_signal = 0
    for phase_setting in phase_settings:
        computer = IntCodeComputer(
            program=copy(controller_input), phase_setting=phase_setting
        )
        computer.run(input_signal)
        input_signal = computer.value
    return input_signal


def run_part2(controller_input, phase_settings):
    computers = [
        IntCodeComputer(
            program=copy(controller_input), phase_setting=phase, yield_at_output=True
        )
        for phase in phase_settings
    ]

    completed = False
    input_signal = 0
    while not completed:
        for computer in computers:
            computer.run(input_signal)
            input_signal = computer.value

        completed = all(c.completed for c in computers)

    return computers[0].value


def run_tests_part1():
    controller_input = [3, 15, 3, 16, 1002, 16, 10, 16, 1, 16, 15, 15, 4, 15, 99, 0, 0]
    assert 43210 == run(controller_input, phase_settings=[4, 3, 2, 1, 0])

    controller_input = [
        3,
        23,
        3,
        24,
        1002,
        24,
        10,
        24,
        1002,
        23,
        -1,
        23,
        101,
        5,
        23,
        23,
        1,
        24,
        23,
        23,
        4,
        23,
        99,
        0,
        0,
    ]
    assert 54321 == run(controller_input, phase_settings=[0, 1, 2, 3, 4])

    controller_input = [
        3,
        31,
        3,
        32,
        1002,
        32,
        10,
        32,
        1001,
        31,
        -2,
        31,
        1007,
        31,
        0,
        33,
        1002,
        33,
        7,
        33,
        1,
        33,
        31,
        31,
        1,
        32,
        31,
        31,
        4,
        31,
        99,
        0,
        0,
        0,
    ]
    assert 65210 == run(controller_input, phase_settings=[1, 0, 4, 3, 2])


def run_tests_part2():
    controller_input = [
        3,
        26,
        1001,
        26,
        -4,
        26,
        3,
        27,
        1002,
        27,
        2,
        27,
        1,
        27,
        26,
        27,
        4,
        27,
        1001,
        28,
        -1,
        28,
        1005,
        28,
        6,
        99,
        0,
        0,
        5,
    ]
    value = run_part2(controller_input, phase_settings=[9, 8, 7, 6, 5])
    assert 139629729 == value

    controller_input = [
        3,
        52,
        1001,
        52,
        -5,
        52,
        3,
        53,
        1,
        52,
        56,
        54,
        1007,
        54,
        5,
        55,
        1005,
        55,
        26,
        1001,
        54,
        -5,
        54,
        1105,
        1,
        12,
        1,
        53,
        54,
        53,
        1008,
        54,
        0,
        55,
        1001,
        55,
        1,
        55,
        2,
        53,
        55,
        53,
        4,
        53,
        1001,
        56,
        -1,
        56,
        1005,
        56,
        6,
        99,
        0,
        0,
        0,
        0,
        10,
    ]

    value = run_part2(controller_input, phase_settings=[9, 7, 8, 5, 6])
    assert 18216 == value


if __name__ == "__main__":
    controller_input = parse_input("day7/input.txt")
    run_tests_part1()
    run_tests_part2()
    max_thruster = 0
    for phase_settings in itertools.permutations([5, 6, 7, 8, 9], 5):
        max_thruster = max(max_thruster, run_part2(controller_input, phase_settings))
    print(max_thruster)
