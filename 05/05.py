import os
import pathlib
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass


@dataclass
class Seed:
    id: int
    soil: int
    fertilizer: int
    water: int
    light: int
    temperature: int
    humidity: int
    location: int


@dataclass
class Range:
    start_source: int
    start_destination: int
    length: int

    def lookup(self, source) -> int | None:
        difference = source - self.start_source
        if difference < 0 or difference > self.length:
            return None

        return self.start_destination + difference


@dataclass
class RangeSet:
    name: str
    ranges: list[Range]

    def lookup(self, source: int, default: int) -> int:
        for r in self.ranges:
            if (res := r.lookup(source)) is not None:
                return res

        return default


@dataclass
class Maps:
    seed_soil: RangeSet
    soil_fertilizer: RangeSet
    fertilizer_water: RangeSet
    water_light: RangeSet
    light_temperature: RangeSet
    temperature_humidity: RangeSet
    humidity_location: RangeSet

    def __post_init__(self):
        self.ranges = [
            self.seed_soil,
            self.soil_fertilizer,
            self.fertilizer_water,
            self.water_light,
            self.light_temperature,
            self.temperature_humidity,
            self.humidity_location,
        ]

    @staticmethod
    def from_input(maps: str) -> "Maps":
        split_maps = maps.split("\n\n")
        out: dict[str, RangeSet] = {}
        for map in split_maps:
            split = map.splitlines()
            title = split.pop(0).removesuffix(" map:")
            out_map = []
            for map_entry in split:
                dst_start, src_start, length = [int(v) for v in map_entry.split()]
                out_map.append(
                    Range(
                        start_source=src_start,
                        start_destination=dst_start,
                        length=length,
                    )
                )

            out_map = RangeSet(title, out_map)

            match title.split("-")[0]:
                case "seed":
                    out["seed_soil"] = out_map

                case "soil":
                    out["soil_fertilizer"] = out_map

                case "fertilizer":
                    out["fertilizer_water"] = out_map

                case "water":
                    out["water_light"] = out_map

                case "light":
                    out["light_temperature"] = out_map

                case "temperature":
                    out["temperature_humidity"] = out_map

                case "humidity":
                    out["humidity_location"] = out_map

        return Maps(**out)

    def identify_seed(self, seed: int) -> Seed:
        soil = self.seed_soil.lookup(seed, seed)
        fertilizer = self.soil_fertilizer.lookup(soil, soil)
        water = self.fertilizer_water.lookup(fertilizer, fertilizer)
        light = self.water_light.lookup(water, water)
        temperature = self.light_temperature.lookup(light, light)
        humidity = self.temperature_humidity.lookup(temperature, temperature)
        location = self.humidity_location.lookup(humidity, humidity)
        return Seed(
            seed, soil, fertilizer, water, light, temperature, humidity, location
        )

    def p2_crib(self, seed: int):
        next = seed
        for range in self.ranges:
            for subrange in range.ranges:
                if (diff := next - subrange.start_source) < 0 or diff > subrange.length:
                    continue

                # found our range
                next = subrange.start_destination + diff
                break
            # print(f"{range.name} seed -> {next}")

        return next

        for r in self.seed_soil.ranges:
            if (v := r.lookup(seed)) is not None:
                soil = v
                break
        else:
            soil = seed

        fertilizer = self.soil_fertilizer.lookup(soil, soil)
        water = self.fertilizer_water.lookup(fertilizer, fertilizer)
        light = self.water_light.lookup(water, water)
        temperature = self.light_temperature.lookup(light, light)
        humidity = self.temperature_humidity.lookup(temperature, temperature)
        location = self.humidity_location.lookup(humidity, humidity)

        return location


def part_1(seeds: list[int], maps: Maps):
    return min(maps.identify_seed(s).location for s in seeds)


def find_minimum(pair: tuple[int, int, int], maps, total):
    print(pair)
    start, step, index = pair
    print(f"Starting! {start} -> {start+step} ({step})")
    i = 0
    minimum = 1 << 61
    for seed in range(start, start + step):
        i += 1
        if i % 500_000 == 0:
            print(
                f"{index:05d}/{total:05d}:\t {start+i:010d}/{start+step:010d} {(i/step) * 100:03.2f}\t -- {step:010d}\tmin: {minimum}"
            )
        minimum = min(minimum, loc := (maps.p2_crib(seed)))

    print(f"{index:05d}|{os.getpid()} DONE!")

    return minimum


def part_2(seed_ranges: list[int], maps: Maps):
    pairs = []
    # for v in seed_ranges:
    #     pairs.append((v, 1, 0))
    MAX_SIZE = 10_000_000
    i = 0
    while seed_ranges:
        start, step, *seed_ranges = seed_ranges
        ostart, ostep = start, step
        print(start, step)
        to_add: list[tuple[int, int, int]] = []
        while step > MAX_SIZE:
            i += 1
            to_add.append((start, MAX_SIZE, i))
            start = start + MAX_SIZE
            step -= MAX_SIZE

        i += 1
        to_add.append((start, step, i))

        assert to_add[0][0] == ostart
        assert to_add[-1][0] + to_add[-1][1] == ostart + ostep
        pairs.extend(to_add)

    print(pairs)
    mins = ProcessPoolExecutor(32).map(
        find_minimum, pairs, [maps] * len(pairs), [i] * len(pairs)
    )

    print(mins)
    out = []
    solve = 1 << 64
    for v in mins:
        out.append(v)
        old_solve = solve
        solve = min(solve, v)
        if old_solve != solve:
            print(f"NEW!  {old_solve} -> {solve}")

    print(min(out))
    return


if __name__ == "__main__":
    EXAMPLE = """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4"""

    EXAMPLE = (pathlib.Path(__file__).parent / "input").read_text()

    SEEDS, _, *maps = EXAMPLE.splitlines()
    MAPS = Maps.from_input("\n".join(maps))
    del maps
    SEEDS = [int(s) for s in SEEDS.removeprefix("seeds: ").split()]
    print(part_1(SEEDS, MAPS))
    print(part_2(SEEDS, MAPS))
