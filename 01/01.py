import pathlib


def part_1(inp: str):
    values: list[int] = []
    for line in inp.splitlines():
        if not line:
            continue

        nums = [l for l in line if l.isnumeric()]
        if len(nums) == 1:
            values.append(int(nums[0] * 2))
        else:
            values.append(int(nums[0] + nums[-1]))

    return values


WORDS = [
    "sdkjfghdfkljghdfkljghdfkljghdfkljghdfklgjhdfkljghdfkljghdklfjghdklfjghdklfjghdklfjghdklfjghdklfgjhdfklgjh",
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
    "ten",
]


def part_2(inp: str):
    all_nums = []
    for line in inp.splitlines():
        nums = []
        while line:
            if line[0].isnumeric():
                nums.append(line[0])
                line = line[0:]

            for n in WORDS:
                if line.startswith(n):
                    nums.append(str(WORDS.index(n)))
                    line = line[1:]
                    break
            else:
                line = line[1:]

        all_nums.append(nums)

    return sum(int(v[0] + v[-1]) for v in all_nums)


TEST = """two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
eighthree"""

print(sum(part_1(pathlib.Path("./input").read_text())))
print(part_2(pathlib.Path("./input").read_text()))
