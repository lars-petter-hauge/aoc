from copy import copy
import itertools

from intcode_computer import parse_input
from intcode_computer import run as run_intcode_computer

def run(controller_input, phase_settings):
    input_signal = 0
    for phase_setting in phase_settings:
        _, input_signal, _, _ = run_intcode_computer(intcodes=copy(controller_input),
                                                     input_signal=input_signal,
                                                     phase_setting=phase_setting)
    return input_signal


def run_part2(controller_input, phase_settings):
    state = {index: {"input_signal": 0, "program": copy(controller_input), "position": 0} for index, phase in enumerate(phase_settings)}

    completed = False
    iteration = 0
    while not completed:
        phase = None
        print("running iteration {}".format(iteration))
        for i in range(5):
            program_state = state[i]
            input_signal = program_state["input_signal"]
            position = program_state["position"]
            if iteration == 0:
                phase = phase_settings[i]
            intcodes, value, pos, completed = run_intcode_computer(intcodes=program_state["program"],
                                                                   input_signal=input_signal,
                                                                   phase_setting=phase,
                                                                   pos=position,
                                                                   yield_at_output=True)
            print("output signal: {}".format(value))
            program_state["position"] = pos
            program_state["program"] = intcodes
            if i==4:
                state[0][0] = value
            else:
                state[i+1][0] = value
        iteration += 1

    return state[0][0]

def run_tests_part1():
    controller_input = [3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0]
    assert 43210 == run(controller_input, phase_settings=[4,3,2,1,0])

    controller_input = [3,23,3,24,1002,24,10,24,1002,23,-1,23,
                        101,5,23,23,1,24,23,23,4,23,99,0,0]
    assert 54321 == run(controller_input, phase_settings=[0,1,2,3,4])

    controller_input = [3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,
                        1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0]
    assert 65210 == run(controller_input, phase_settings=[1,0,4,3,2])

def run_tests_part2():
    controller_input = [3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,
                        27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5]
    value = run_part2(controller_input, phase_settings=[9,8,7,6,5])
    assert 139629729 == value

    controller_input = [3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,
                        -5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,
                        53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10]

    value = run_part2(controller_input, phase_settings=[9,7,8,5,6])
    assert 18216 == value

if __name__ == '__main__':
    controller_input = parse_input("day7/input.txt")
    run_tests_part1()
    run_tests_part2()
    max_thruster = 0
    #for phase_settings in itertools.permutations([0,1,2,3,4], 5):
    #    max_thruster = max(max_thruster, run(controller_input, phase_settings))
    #print(max_thruster)
