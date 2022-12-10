TEST_INPUT = """R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2"""

TEST_INPUT_TWO = """R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20"""


def load_input(fname):
    with open(fname) as fh:
        return [l.strip() for l in fh.readlines()]


def parse_lines(lines):
    result = []
    for line in lines:
        direction, n = line.split()
        result.extend([direction] * int(n))
    return result


def move_head(move, pos):
    if move == "D":
        pos[0] += 1
        return pos
    elif move == "U":
        pos[0] -= 1
        return pos
    elif move == "R":
        pos[1] += 1
        return pos
    elif move == "L":
        pos[1] -= 1
        return pos
    raise NotImplementedError()


def update_follower(leader, follower):

    for i in range(2):
        diff = leader[i] - follower[i]
        if abs(diff) > 1:
            follower[i] += int(diff / 2)
            j = 1 if i == 0 else 0
            diff = leader[j] - follower[j]
            if abs(diff) > 1:
                diff = int(diff / 2)
            if abs(diff) > 0:
                follower[j] += int(diff)

    return follower


def update_tail(head_pos, tail_positions):
    front_pos = update_follower(head_pos, tail_positions[0])
    tail_positions[0] = front_pos
    for i in range(len(tail_positions) - 1):
        tail_positions[i + 1] = update_follower(
            tail_positions[i], tail_positions[i + 1]
        )
    return tail_positions


def run(head_moves, length=2):
    tail_positions = [[0, 0] for _ in range(length - 1)]
    head_pos = [0, 0]
    tail_end_history = set()

    for head_move in head_moves:
        head_pos = move_head(head_move, head_pos)
        tail_positions = update_tail(head_pos, tail_positions)
        tail_end_history.add(tuple(tail_positions[-1]))
    return tail_end_history


# may happen if position ahead was updated diagonally.
assert update_follower(leader=[5, 5], follower=[7, 7]) == [6, 6]
assert update_follower(leader=[5, 9], follower=[7, 7]) == [6, 8]

moves = parse_lines(TEST_INPUT.split("\n"))
positions = run(moves, length=2)
assert len(positions) == 13
positions = run(moves, length=10)
assert len(positions) == 1

moves = parse_lines(TEST_INPUT_TWO.split("\n"))
positions = run(moves, length=10)
assert len(positions) == 36

moves = parse_lines(load_input("input.txt"))
positions = run(moves, length=2)
assert len(run(moves)) == 6044
positions = run(moves, length=10)
assert len(positions) == 2384
