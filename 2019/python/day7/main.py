from copy import copy
import itertools

from intcode_computer import parse_input
from intcode_computer import run as run_intcode_computer

def run(controller_input, phase_settings):
    input_signal = 0
    for phase_setting in phase_settings:
        input_signal = run_intcode_computer(copy(controller_input), values=[phase_setting, input_signal])
    return input_signal


def run_tests():
    controller_input = [3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0]
    assert 43210 == run(controller_input, phase_settings=[4,3,2,1,0])

    controller_input = [3,23,3,24,1002,24,10,24,1002,23,-1,23,
                        101,5,23,23,1,24,23,23,4,23,99,0,0]
    assert 54321 == run(controller_input, phase_settings=[0,1,2,3,4])

    controller_input = [3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,
                        1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0]
    assert 65210 == run(controller_input, phase_settings=[1,0,4,3,2])

if __name__ == '__main__':
    controller_input = parse_input("day7/input.txt")
    run_tests()
    max_thruster = 0
    for phase_settings in itertools.permutations([0,1,2,3,4], 5):
        max_thruster = max(max_thruster, run(controller_input, phase_settings))
    print(max_thruster)
