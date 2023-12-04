import pathlib
from textwrap import dedent


def extract(in_: str) -> list[list[str]]:
    return [[c for c in l] for l in in_.splitlines()]


def neighbours(row, col):
    for r_opt in (-1, 0, 1):
        for c_opt in (-1, 0, 1):
            yield (row + r_opt, col + c_opt)


def find_number_at(row: int, col: int, board: list[list[str]]) -> tuple[int, int]:
    target_row = board[row]
    while col > 0 and target_row[col - 1].isnumeric():
        col -= 1

    num = target_row[col]
    num_start = col

    while True:
        col += 1
        if col == len(target_row):
            break
        if not (next := target_row[col]).isnumeric():
            break

        num += next

    return int(num), num_start


def part_1(input: list[list[str]]):
    out = []
    seen: list[tuple[int, int]] = []
    for row, line in enumerate(input):
        for col, char in enumerate(line):
            if char.isnumeric() or char == ".":
                continue

            for r, c in neighbours(row, col):
                if not input[r][c].isnumeric():
                    continue

                num, col_start = find_number_at(r, c, input)
                if (r, col_start) not in seen:
                    seen.append((r, col_start))
                    out.append(num)
    return sum(out)


def part_2(input: list[list[str]]):
    out = []
    for row, line in enumerate(input):
        for col, char in enumerate(line):
            if char.isnumeric() or char != "*":
                continue

            n = []
            s_n = []
            for r, c in neighbours(row, col):
                if not input[r][c].isnumeric():
                    continue

                num, col_start = find_number_at(r, c, input)
                if (coords := (r, col_start)) in s_n:
                    continue

                n.append(num)
                s_n.append(coords)
            if len(n) == 2:
                out.append(n[0] * n[1])

    return sum(out)


if __name__ == "__main__":
    EXAMPLE = dedent(
        """\
        467..114..
        ...*......
        ..35..633.
        ......#...
        617*......
        .....+.58.
        ..592.....
        ......755.
        ...$.*....
        .664.598.."""
    )

    EXAMPLE = (pathlib.Path(__file__).parent / "input").read_text()
    v = extract(EXAMPLE)
    print(part_1(v))
    print(part_2(v))
