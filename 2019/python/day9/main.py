from intcode_computer import parse_input, IntCodeComputer, ExpandingList


def run_tests():
    computer = IntCodeComputer(ExpandingList([104, 1125899906842624, 99]))
    computer.run(0)
    assert 1125899906842624 == computer.value

    computer = IntCodeComputer(
        ExpandingList([1102, 34915192, 34915192, 7, 4, 7, 99, 0])
    )
    computer.run(0)
    assert 1219070632396864 == computer.value

    program = [109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99]
    computer = IntCodeComputer(ExpandingList(program))
    computer.run(input_signal=0)
    assert program == computer.program[: len(program)]


if __name__ == "__main__":
    # run_tests()

    controller_input = parse_input("day9/input.txt")
    computer = IntCodeComputer(ExpandingList(controller_input))
    computer.verbose = True
    computer.run(input_signal=10)
    print(computer.value)
