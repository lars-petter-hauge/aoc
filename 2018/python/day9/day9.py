import time


def thegame(players, last_marble):
    marbles = [0, 1]
    idx = 1
    player_score = {}
    progress = last_marble / 100
    progressed = 0
    start = time.time()
    round_time = time.time()
    for i in range(2, last_marble + 1):
        if i > progressed:
            progressed += progress
            percentage = int((progressed / last_marble) * 100)
            print(
                "Progress: {}%. Time elapsed since start: {} minutes, time since last update: {}".format(
                    percentage,
                    (time.time() - start) / 60,
                    (time.time() - round_time) / 60,
                )
            )
            round_time = time.time()

        if i % 23 == 0:
            player = i % players
            score = i
            score_idx = (idx - 7) % len(marbles)
            score += marbles.pop(score_idx)
            idx = score_idx
            player_score[player] = player_score.get(player, 0) + score
        else:
            idx = (idx + 2) % len(marbles)
            marbles.insert(idx, i)
    return max(player_score.values())


# assert thegame(10,1618) == 8317
print("the winner gets: {}".format(thegame(404, 7185200)))
