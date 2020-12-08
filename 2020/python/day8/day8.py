import copy


class InstructionError(BaseException):
    pass


class Computer:
    def __init__(self, instructions):
        self._instructions = instructions
        self._accumulator = 0
        self._idx = 0
        self._adapter = {"acc": self._acc, "jmp": self._jmp, "nop": self._nop}

    def run(self):
        called_instructions = []
        while True:
            if self._idx >= len(self._instructions):
                # program complete
                return self._accumulator

            instr, value = self._instructions[self._idx]

            if self._idx in called_instructions:
                raise InstructionError(
                    f"Instruction {instr} at {self._idx} called twice. Accumulator value {self._accumulator}"
                )

            called_instructions.append(self._idx)
            self._adapter[instr](value)

    def _acc(self, value):
        self._idx += 1
        self._accumulator += value

    def _jmp(self, value):
        self._idx += value

    def _nop(self, _):
        self._idx += 1


def load(fname):
    with open(fname) as fh:
        lines = fh.readlines()
    return lines


def parse(lines):
    return [(l.split()[0], int(l.split()[1])) for l in lines]


def run_computer(dataset, expected_succes=True):
    computer = Computer(dataset)
    if expected_succes:
        return computer.run()
    try:
        computer.run()
        raise ValueError("Completed - was not supposed to")
    except InstructionError as e:
        # Last value in error is accumulator value
        return int(str(e).rsplit(" ")[-1])


TEST = """
nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6
"""

if __name__ == "__main__":
    test_data = parse(TEST.split("\n")[1:-1])
    assert 5 == run_computer(test_data, expected_succes=False)

    test_data[-2] = ("nop", -4)
    assert 8 == run_computer(test_data)

    data = parse(load("2020/python/day8/input.txt"))

    assert 1446 == run_computer(data, expected_succes=False)

    changeable = [i for i, x in enumerate(data) if x[0] in ["nop", "jmp"]]

    for change in changeable:
        new_data = copy.deepcopy(data)
        if new_data[change][0] == "nop":
            new_data[change] = ("jmp", new_data[change][1])
        elif new_data[change][0] == "jmp":
            new_data[change] = ("nop", new_data[change][1])
        computer = Computer(new_data)
        try:
            print(computer.run())
            break
        except InstructionError as e:
            continue
