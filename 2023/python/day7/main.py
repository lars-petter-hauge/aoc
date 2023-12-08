TEST_DATA = """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483"""

TYPE_STRENGTH = ["HIGH", "PAIR", "TWO_PAIRS", "THREE", "HOUSE", "FOUR", "FIVE"]
SINGLE_STRENGTH = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]
SINGLE_STRENGTH_WILDCARD = [
    "J",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "T",
    "Q",
    "K",
    "A",
]
from collections import Counter


class Hand:
    def __init__(self, cards, use_wildcard=False):
        self._cards = cards
        self._counter = Counter(self._cards)
        self._use_wildcard = use_wildcard
        common = self._counter.most_common(2)
        if len(common) == 2:
            (primary_card, primary), (secondary_card, secondary) = common
        else:
            (primary_card, primary) = common[0]
            secondary = None
            secondary_card = None
        if use_wildcard:
            wild_card = self._counter.get("J")
            if wild_card is not None:
                if primary_card == "J" and secondary is not None:
                    primary += secondary
                    secondary = 0
                elif secondary_card == "J":
                    primary += secondary
                    secondary = 0
                else:
                    primary += wild_card
                # edge case (only "J")
                primary = min(primary, 5)
        if primary == 5:
            self._type = "FIVE"
        elif primary == 4:
            self._type = "FOUR"
        elif primary == 3 and secondary == 2:
            self._type = "HOUSE"
        elif primary == 3:
            self._type = "THREE"
        elif primary == 2 and secondary == 2:
            self._type = "TWO_PAIRS"
        elif primary == 2:
            self._type = "PAIR"
        else:
            self._type = "HIGH"

    def __repr__(self):
        return self._cards

    def __lt__(self, other):
        if TYPE_STRENGTH.index(self._type) > TYPE_STRENGTH.index(other._type):
            return False

        if TYPE_STRENGTH.index(self._type) < TYPE_STRENGTH.index(other._type):
            return True

        strength, other_strength = 0, 0
        i = 0
        while strength == other_strength and i <= len(self._cards):
            if self._use_wildcard:
                strength_rating = SINGLE_STRENGTH_WILDCARD
            else:
                strength_rating = SINGLE_STRENGTH
            strength = strength_rating.index(self._cards[i])
            other_strength = strength_rating.index(other._cards[i])
            i += 1

        return strength < other_strength


def calc_score(hands):
    return sum(
        [i * score for i, (_, score) in enumerate(sorted(hands, key=lambda x: x[0]), 1)]
    )


def load_input(fname):
    with open(fname) as fh:
        return fh.readlines()


def parse_lines(lines, wildcard=False):
    result = []

    for line in lines:
        cards, score = line.split()
        result.append((Hand(cards, wildcard), int(score)))
    return result


hands = parse_lines(TEST_DATA.split("\n"))
assert calc_score(hands) == 6440
hands = parse_lines(TEST_DATA.split("\n"), wildcard=True)
assert calc_score(hands) == 5905


hands = parse_lines(load_input("input.txt"))
assert calc_score(hands) == 250474325

hands = parse_lines(load_input("input.txt"), wildcard=True)

print(calc_score(hands))
