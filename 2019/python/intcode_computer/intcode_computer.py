def parse_input(fname):
    with open(fname) as f:
        data = f.readlines()
    return ExpandingList([int(x) for x in data[0].split(",")])


class ExpandingList(list):
    def __setitem__(self, index, value):
        if index >= len(self):
            self.extend([0] * (index + 1 - len(self)))
        list.__setitem__(self, index, value)

    def __getitem__(self, index):
        if isinstance(index, int):
            if index >= len(self):
                self.extend([0] * (index + 1 - len(self)))
            if index < 0:
                raise IndexError
        else:
            if index.stop and index.stop >= len(self):
                self.extend([0] * (index.stop + 1 - len(self)))
            if index.start and index.start < 0:
                raise IndexError

        return list.__getitem__(self, index)


class IntCodeComputer:
    def __init__(self, program, phase_setting=None, yield_at_output=False):
        self._memory = program
        self.yield_at_output = yield_at_output
        self._mem_pointer = 0
        self._internal_base = 0
        self.completed = True
        self.operation = None

        self.phase_setting = phase_setting
        self.value = None
        self.phase_set = phase_setting is None
        self.read_first_method = None
        self.read_second_method = None

        self.read_modes = {
            0: self.from_position,
            1: self.from_memory,
            2: self.from_relative_position,
        }

        self.set_modes = {
            0: self.to_position,
            2: self.to_relative_position,
        }

        self.operations = {
            1: self.add,
            2: self.multiply,
            3: self.save,
            4: self.output,
            5: self.jump_if_true,
            6: self.jump_if_false,
            7: self.less_than,
            8: self.equals,
            9: self.set_base,
        }
        self.verbose = False

    def run(self, input_signal):
        self.completed = True
        if not self.phase_set:
            self.value = self.phase_setting
        else:
            self.value = input_signal

        while self._memory[self._mem_pointer] != 99:

            self.update_mode()
            self.operation()

            if self.operation.__name__ == "save":
                if not self.phase_set:
                    self.value = input_signal
                    self.phase_set = True

            if self.operation.__name__ == "output":
                if self.yield_at_output:
                    self.completed = False
                    break

    def add(self):
        a, b, c = self._memory[self._mem_pointer + 1 : self._mem_pointer + 4]
        value = self.read_first_method(a) + self.read_second_method(b)
        self.set_value_method(pos=c, value=value)
        self._mem_pointer += 4

    def multiply(self):
        a, b, c = self._memory[self._mem_pointer + 1 : self._mem_pointer + 4]
        value = self.read_first_method(a) * self.read_second_method(b)
        self.set_value_method(pos=c, value=value)
        self._mem_pointer += 4

    def save(self):
        pos = self.read_first_method(self._mem_pointer + 1)
        self.set_value_method(pos=pos, value=self.value)
        self._mem_pointer += 2

    def output(self):
        pos = self.read_first_method(self._mem_pointer + 1)
        self.value = self._memory[pos]
        if self.verbose:
            print("Output value: {}".format(self.value))
        self._mem_pointer += 2

    def jump_if_true(self):
        a, b, c = self._memory[self._mem_pointer + 1 : self._mem_pointer + 4]
        a = self.read_first_method(a)
        b = self.read_second_method(b)
        if a:
            self._mem_pointer = b
        else:
            self._mem_pointer += 3

    def jump_if_false(self):
        a, b, c = self._memory[self._mem_pointer + 1 : self._mem_pointer + 4]
        a = self.read_first_method(a)
        b = self.read_second_method(b)
        if not a:
            self._mem_pointer = b
        else:
            self._mem_pointer += 3

    def less_than(self):
        a, b, c = self._memory[self._mem_pointer + 1 : self._mem_pointer + 4]
        a = self.read_first_method(a)
        b = self.read_second_method(b)
        if a < b:
            value = 1
        else:
            value = 0
        self.set_value_method(pos=c, value=value)
        self._mem_pointer += 4

    def equals(self):
        a, b, c = self._memory[self._mem_pointer + 1 : self._mem_pointer + 4]
        a = self.read_first_method(a)
        b = self.read_second_method(b)
        if a == b:
            value = 1
        else:
            value = 0
        self.set_value_method(pos=c, value=value)
        self._mem_pointer += 4

    def set_base(self):
        pos = self.read_first_method(self._mem_pointer + 1)
        self._internal_base += self._memory[pos]
        self._mem_pointer += 2

    def from_position(self, pos):
        return self._memory[pos]

    def from_relative_position(self, pos):
        return self._memory[pos + self._internal_base]

    def from_memory(self, pos):
        return pos

    def to_position(self, pos, value):
        self._memory[pos] = value

    def to_relative_position(self, pos, value):
        self._memory[pos + self._internal_base] = value

    def update_mode(self):
        code = str(self._memory[self._mem_pointer])

        if len(code) == 5:
            a = int(code[0])
            code = code[1:]
        else:
            a = 0
        self.set_value_method = self.set_modes[a]

        if len(code) == 4:
            b = int(code[0])
            code = code[1:]
        else:
            b = 0
        self.read_second_method = self.read_modes[b]

        if len(code) == 3:
            c = int(code[0])
            code = code[1:]
        else:
            c = 0
        self.read_first_method = self.read_modes[c]

        op = int(code)

        # back hack.. If it's a save method, the setting applies
        # to the final mode instead of the first. maybe.
        if op == 3:
            self.set_value_method = self.set_modes[c]

        self.operation = self.operations[op]
