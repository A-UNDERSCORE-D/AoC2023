import itertools
import math
import pathlib
from dataclasses import dataclass
from typing import Callable


@dataclass
class Node:
    name: str
    left: "Node" = None  # type: ignore[assignment]
    right: "Node" = None  # type: ignore[assignment]


def create_graph(input: str) -> tuple[Node, dict[str, Node]]:
    raw_graph = {}

    for line in input.splitlines():
        parent, line = line.strip().split(" = ")
        left, right = line[1:-1].split(", ")

        raw_graph[parent] = [left, right]

    full_graph = {}

    for (name), (left, right) in raw_graph.items():
        full_graph[name] = (n := Node(name))

    while True:
        for n in full_graph.values():
            if n.left is None or n.right is None:
                break
        else:
            break

        if n.left is None:
            n.left = full_graph[raw_graph[n.name][0]]

        if n.right is None:
            n.right = full_graph[raw_graph[n.name][1]]

    return full_graph["AAA" if "AAA" in full_graph else "11A"], full_graph


def steps_to(start: Node, target: str | Callable[[Node], bool], step_order: str):
    infinite_steps = itertools.cycle(step_order)
    if isinstance(target, str):
        target = lambda v: v.name == target  # noqa: its a default

    current = start
    steps = 0
    while not target(current):
        steps += 1
        nx = next(infinite_steps)
        if nx == "R":
            current = current.right

        else:
            current = current.left

    return steps


def steps_to_2(start: list[Node], step_order: str):
    cycles: list[int] = []

    for node in start:
        cycles.append(steps_to(node, lambda v: v.name[-1] == "Z", step_order))

    return math.lcm(*cycles)


if __name__ == "__main__":
    EXAMPLE = """LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)"""

    EXAMPLE = """LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)"""

    EXAMPLE = (pathlib.Path(__file__).parent / "input").read_text()

    steps, graph = EXAMPLE.split("\n\n")

    g, nodes = create_graph(graph)
    # print(steps_to(g, "ZZZ", steps))
    starts = []

    for line in graph.splitlines():
        name, _ = line.strip().split(" = ")

        if name[-1] == "A":
            starts.append(name)

    print(steps_to_2([nodes[n] for n in starts], steps))
