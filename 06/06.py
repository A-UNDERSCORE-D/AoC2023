import pathlib


def run_race_1(max_time, record_distance):
    beats = []
    for i in range(max_time):
        speed = i
        time = max_time - i

        end_distance = speed * time
        if end_distance > record_distance:
            beats.append(i)

    return beats


def part_1(races: list[tuple[int, int]]):
    solution = 0
    for t, dist in races:
        res = run_race_1(t, dist)
        options = len(res)
        if solution == 0:
            solution = options
        else:
            solution *= options

    return solution


if __name__ == "__main__":
    EXAMPLE = """Time:      7  15   30
Distance:  9  40  200"""
    EXAMPLE = (pathlib.Path(__file__).parent / "input").read_text()

    races = list(
        zip(
            map(int, EXAMPLE.splitlines()[0].removeprefix("Time:").strip().split()),
            map(int, EXAMPLE.splitlines()[1].removeprefix("Distance:").strip().split()),
        )
    )
    print(part_1(races))

    races = [
        (
            int(EXAMPLE.splitlines()[0].removeprefix("Time:").replace(" ", "")),
            int(EXAMPLE.splitlines()[1].removeprefix("Distance:").replace(" ", "")),
        )
    ]
    print(len(run_race_1(*races[0])))
