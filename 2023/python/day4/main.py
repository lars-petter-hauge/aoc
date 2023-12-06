from collections import defaultdict
import math


TEST_DATA="""Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"""

def load_input(fname):
    with open(fname) as fh:
        return fh.readlines()



def parse_input(string):
    winning_numbers, player_numbers = string.split("|")
    card, winning_numbers = winning_numbers.split(":")
    player_numbers = [int(num.strip()) for num in player_numbers.split(" ") if num]
    winning_numbers = [int(num.strip()) for num in winning_numbers.split(" ") if num]
    card = int(card.split(" ")[-1])
    return card, winning_numbers, player_numbers

def score_card(player_numbers, winning_numbers):
    match = set(player_numbers) & set(winning_numbers)
    if len(match)==0:
        return 0
    return 2**(len(match)-1)

def cards_won(player_numbers, winning_numbers):
    return len(set(player_numbers) & set(winning_numbers))

def deck_amount(games):

    card_amounts = {card_id:1 for card_id,_,_ in games}

    for (card_id, winning_numbers, player_numbers) in games:
        score = cards_won(player_numbers, winning_numbers)
        for i in range(card_id+1, card_id+1+score):
            if i in card_amounts:
                card_amounts[i] += (card_amounts[card_id])

    return sum(card_amounts.values())


games = [parse_input(line) for line in TEST_DATA.split("\n") if line]

scores = [score_card(player_numbers, winning_numbers) for card, winning_numbers, player_numbers in games ]
print(sum(scores))
print(deck_amount(games))

data = load_input("input.txt")
games = [parse_input(line) for line in data]

scores = [score_card(player_numbers, winning_numbers) for card, winning_numbers, player_numbers in games ]
print(sum(scores))
print(deck_amount(games))
