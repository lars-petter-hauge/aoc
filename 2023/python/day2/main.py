from collections import defaultdict
import math


def load_input(fname):
    with open(fname) as fh:
        return fh.read()


AVAILABLE_BALLS = {"red": 12, "green": 13, "blue": 14}


def parse_input(string):
    name, games = string.split(":")
    balls = defaultdict(lambda: 0)
    for sub_game in games.split(";"):
        for ball in sub_game.split(","):
            amount, color = ball.split()
            amount = int(amount)
            balls[color] = max(amount, balls[color])

    return (int(name.split()[1]), balls)


def valid_game(game):
    for color, amount in game.items():
        if AVAILABLE_BALLS[color] < amount:
            return False
    return True


data = load_input("input.txt")

games = [parse_input(line) for line in data.split("\n") if line]
valid_games = [game_id for game_id, balls in games if valid_game(balls)]
print(sum(valid_games))
print(sum([math.prod(balls.values()) for _, balls in games]))
