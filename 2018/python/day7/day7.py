import unittest
import string

def parse_data(lines):
    parsed = {}
    for line in lines:
        key = line[36]
        val = line[5]
        if key not in parsed:
            parsed[key] = [val]
        else:
            parsed[key].append(val)
    return parsed


def read_input(fname):
    with open(fname) as f:
        data = f.readlines()
    return data

def work_time(char, min_time):
    bonustime = list(string.ascii_uppercase).index(char) + 1
    return  min_time + bonustime

def define_order(steps, instructions):
    completed= []
    while len(steps)>0:
        possible_steps = [s for s in steps if s not in instructions.keys()]
        possible_steps.sort()
        next_step = possible_steps[0]

        steps.remove(next_step)
        completed.append(next_step)

        # update values
        for key, values in instructions.items():
            instructions[key] = [x for x in values if x not in completed]
        # remove steps with no more steps required
        instructions = {key: value for key, value in instructions.items() if len(value)>0}
    return completed

def define_worktime(steps, instructions, workers = 1, min_time = 0):
    completed = []
    progress = {}
    total = 0
    while len(steps)>0:
        newly_compl = []
        for work, time in progress.items():
            progress[work] = time - 1

        newly_compl = [key for key,val in progress.items() if val==0]
        progress = {key:val for key,val in progress.items() if val>0}

        completed.extend(newly_compl)

        if newly_compl:
            for c in newly_compl:
                steps.remove(c)
            # update values
            for key, values in instructions.items():
                instructions[key] = [x for x in values if x not in completed]
            # remove steps with no more steps required
            instructions = {key: value for key, value in instructions.items() if len(value)>0}

        # all workers occupado..
        if len(progress) == workers:
            total+=1
            continue

        possible_steps = [s for s in steps if s not in instructions.keys()]
        possible_steps = [s for s in possible_steps if s not in progress.keys()]
        possible_steps.sort()

        if len(possible_steps)==0:
            total += 1
            continue

        for s in possible_steps:
            if len(progress)==workers:
                break
            progress[s] = work_time(s, min_time)

        total += 1
    # Subtracting the last added value
    total -= 1
    return total


def steps(data):
    y = []
    [y.extend(x) for x in data.values()]
    [y.extend(x) for x in data.keys()]
    steps = set(y)
    return steps

class Test(unittest.TestCase):
    def test(self):
        data = read_input('day7_test')
        parsed = parse_data(data)
        order = define_order(steps(parsed), parsed)
        work_time = define_worktime(steps(parsed), parsed, workers = 2, min_time = 0)
        assert order == ['C','A','B','D','F','E']
        assert work_time == 15



if __name__ == '__main__':
    #unittest.main()
    data = read_input('day7input')
    parsed = parse_data(data)
    work_time = define_worktime(steps(parsed), parsed, workers = 5, min_time = 60)
    print(work_time)
