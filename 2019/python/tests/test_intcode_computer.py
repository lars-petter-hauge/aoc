from intcode_computer.intcode_computer import IntCodeComputer, parse_input


def run(intcodes, input_signal=0, phase_setting=None, pos=0, yield_at_output=False):
    computer = IntCodeComputer(
        intcodes, phase_setting=phase_setting, yield_at_output=yield_at_output
    )
    computer.run(input_signal)

    return (
        computer._memory,
        computer.value,
        computer._mem_pointer,
        computer.completed,
    )


def test_positional_mode():
    for input_signal in range(-10, 10):
        # Positional mode
        assert (input_signal == 8) == run(
            [3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8], input_signal=input_signal
        )[1]
        assert (input_signal < 8) == run(
            [3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8], input_signal=input_signal
        )[1]


def test_intcode():

    for input_signal in range(-10, 10):
        # Positional mode
        assert (input_signal == 8) == run(
            [3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8], input_signal=input_signal
        )[1]
        assert (input_signal < 8) == run(
            [3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8], input_signal=input_signal
        )[1]

        # Immediate mode
        assert (input_signal == 8) == run(
            [3, 3, 1108, -1, 8, 3, 4, 3, 99], input_signal=input_signal
        )[1]
        assert (input_signal < 8) == run(
            [3, 3, 1107, -1, 8, 3, 4, 3, 99], input_signal=input_signal
        )[1]

        # Jump mode
        assert (input_signal != 0) == run(
            [3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9],
            input_signal=input_signal,
        )[1]
        assert (input_signal != 0) == run(
            [3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1], input_signal=input_signal
        )[1]

        # Larger example
        program = [
            3,
            21,
            1008,
            21,
            8,
            20,
            1005,
            20,
            22,
            107,
            8,
            21,
            20,
            1006,
            20,
            31,
            1106,
            0,
            36,
            98,
            0,
            0,
            1002,
            21,
            125,
            20,
            4,
            20,
            1105,
            1,
            46,
            104,
            999,
            1105,
            1,
            46,
            1101,
            1000,
            1,
            20,
            4,
            20,
            1105,
            1,
            46,
            98,
            99,
        ]
        output = run(program, input_signal=input_signal)[1]

        if input_signal < 8:
            assert output == 999
        elif input_signal == 8:
            assert output == 1000
        else:
            assert output == 1001

    original_data = parse_input("day5/input.txt")
    input_signal = run(original_data, input_signal=1)[1]
    assert input_signal == 13210611

    original_data = parse_input("day5/input.txt")
    input_signal = run(original_data, input_signal=5)[1]
    assert input_signal == 584126
