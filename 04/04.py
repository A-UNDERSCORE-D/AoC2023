import pathlib
import time
from dataclasses import dataclass
from functools import lru_cache


@dataclass
class Card:
    id: int
    numbers: list[int]
    valid_numbers: list[int]

    @staticmethod
    def from_line(line: str) -> "Card":
        num, spl = line.split(": ")
        num = int(num.removeprefix("Card "))

        w_str, c_str = spl.split(" | ")

        winning = [int(x.strip()) for x in w_str.split()]
        card = [int(x.strip()) for x in c_str.split()]

        return Card(num, card, winning)

    @property
    def winning_numbers(self) -> set[int]:
        w, l = set(self.valid_numbers), set(self.numbers)
        return w & l

    @lru_cache()
    def part_one(self):
        out = 0
        for _ in self.winning_numbers:
            if out == 0:
                out = 1
                continue

            out *= 2

        return out


def part_one(cards: list[Card]) -> int:
    return sum(c.part_one() for c in cards)


def part_2(cards: list[Card]) -> int:
    played_cards = 0
    to_play = [1 for _ in range(len(cards))]
    current_card: Card = cards[0]

    while any(to_play):
        if to_play[current_card.id - 1] == 0:
            current_card = cards[current_card.id]

        play_count = to_play[current_card.id - 1]
        winning_numbers = current_card.winning_numbers
        for i, _ in enumerate(winning_numbers):
            to_play[current_card.id + i] += play_count

        played_cards += play_count
        to_play[current_card.id - 1] -= play_count

    return played_cards


if __name__ == "__main__":
    EXAMPLE = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"""
    EXAMPLE = (pathlib.Path(__file__).parent / "input").read_text()

    cards = [Card.from_line(l) for l in EXAMPLE.splitlines()]

    # print(part_one(cards))
    print(part_2(cards))
