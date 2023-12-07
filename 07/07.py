import enum
import pathlib
from collections import Counter
from operator import itemgetter


class HAND(enum.IntEnum):
    FIVE_OF_A_KIND = enum.auto()
    FOUR_OF_A_KIND = enum.auto()
    FULL_HOUSE = enum.auto()
    THREE_OF_A_KIND = enum.auto()
    TWO_PAIR = enum.auto()
    ONE_PAIR = enum.auto()
    HIGH_CARD = enum.auto()


def hand_score(cards: str) -> HAND:
    counts = Counter(cards)
    most_common = counts.most_common()
    match len(counts):
        case 1:
            return HAND.FIVE_OF_A_KIND

        case 2 if most_common[0][1] == 4:
            return HAND.FOUR_OF_A_KIND

        case 2 if most_common[0][1] == 3:
            return HAND.FULL_HOUSE

        case 3 if most_common[0][1] == 3:
            return HAND.THREE_OF_A_KIND

        case 3 if most_common[0][1] == 2 and most_common[0][1] == 2:
            return HAND.TWO_PAIR

        case 4 if most_common[0][1] == 2:
            return HAND.ONE_PAIR

    return HAND.HIGH_CARD


def hand_score_2(cards: str):
    if "J" not in cards:
        return hand_score(cards)
    options = set(cards)

    best = 1000
    for option in options:
        score = hand_score(cards.replace("J", option))
        if score < best:
            best = score

    assert isinstance(best, HAND)
    return best


SORTING = "AKQJT98765432"
SORTING_2 = "AKQT98765432J"


def rank_hands(
    hand_bids: list[tuple[str, int]], card_sort=SORTING, card_rank=hand_score
):
    bids = dict(hand_bids)
    hands = [
        (h, score)
        for h, score in sorted(
            [
                (hnd, card_rank(hnd))
                for hnd in sorted(
                    bids.keys(),
                    key=lambda v: tuple(card_sort.index(lt) for lt in v),
                    reverse=True,
                )
            ],
            key=itemgetter(1),
            reverse=True,
        )
    ]

    return {
        hand: (bids[hand], idx + 1, hand_type)
        for idx, (hand, hand_type) in enumerate(hands)
    }


def part_1(parsed: list[tuple[str, int]]):
    scored_hands = rank_hands(parsed)

    return sum(bid * score for bid, score, _ in scored_hands.values())


def part_2(parsed: list[tuple[str, int]]):
    scored_hands = rank_hands(parsed, SORTING_2, hand_score_2)

    return sum(bid * score for bid, score, _ in scored_hands.values())


if __name__ == "__main__":
    EXAMPLE = """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483"""
    EXAMPLE = (pathlib.Path(__file__).parent / "input").read_text()

    parsed: list[tuple[str, int]] = [
        (hand, int(bid)) for hand, bid in [s.split() for s in EXAMPLE.splitlines()]
    ]

    print(part_1(parsed))
    print(part_2(parsed))
