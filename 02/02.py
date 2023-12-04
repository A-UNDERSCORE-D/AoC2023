import pathlib
from dataclasses import dataclass
from typing import Callable, Iterable, Self

EXAMPLE = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""


@dataclass
class Game:
    id: int
    sets: list["CubeSet"]

    @dataclass
    class CubeSet:
        red: int = 0
        green: int = 0
        blue: int = 0

        @property
        def power(self) -> int:
            return self.red * self.green * self.blue

        @staticmethod
        def from_str(set: str):
            split = set.split(", ")
            out = {}
            for entry in split:
                num, colour = entry.split(" ")
                out[colour] = int(num)

            return Game.CubeSet(**out)

    @staticmethod
    def from_str(input: str) -> "Game":
        id, sets = input.split(": ", maxsplit=1)
        id = int(id.removeprefix("Game "))

        cube_sets = [Game.CubeSet.from_str(s) for s in sets.split("; ")]

        return Game(id, cube_sets)

    def predicate(self, func: Callable[[Iterable[int]], int]) -> CubeSet:
        return Game.CubeSet(
            red=func(s.red for s in self.sets),
            green=func(s.green for s in self.sets),
            blue=func(s.blue for s in self.sets),
        )


def part_1(games: list[Game], red: int, green: int, blue: int):
    """Find the sum of the games that are impossible"""

    possible: list[Game] = []

    for game in games:
        maximum = game.predicate(max)
        if any((maximum.red > red, maximum.green > green, maximum.blue > blue)):
            continue

        possible.append(game)

    print("\n".join(str(g.id) for g in possible))

    return sum(g.id for g in possible)


def part_2(games: list[Game]):
    """Find the minimum number of cubes required"""

    minimums: list[Game.CubeSet] = []

    for game in games:
        min_cubes = game.predicate(max)
        minimums.append(min_cubes)

    return sum(s.power for s in minimums)


if __name__ == "__main__":
    EXAMPLE = pathlib.Path("./02/input").read_text()
    games = [Game.from_str(g) for g in EXAMPLE.splitlines()]

    print(part_1(games, 12, 13, 14))
    print(part_2(games))
