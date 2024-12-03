import textwrap
from typing import Callable, Iterable, TypeVar

import numpy as np
from adventofcode import AoC

T1 = TypeVar("T1")
T2 = TypeVar("T2")


def flatmap(
    func: Callable[[T1], T2], matrix: Iterable[Iterable[T1]]
) -> Iterable[Iterable[T2]]:
    return map(lambda row: map(func, row), matrix)


def prepare_input(raw: list[str]) -> list[list[int]]:
    prepared_map = flatmap(int, map(str.split, raw))
    return list(map(list, prepared_map))


def is_safe(row: list[int]) -> bool:
    diff = np.diff(row)
    increasing_check = (1 <= diff) & (diff <= 3)
    decreasing_check = (-3 <= diff) & (diff <= -1)
    return increasing_check.all() | decreasing_check.all()


def part1(raw: list[str]) -> int:
    prepared = prepare_input(raw)
    return sum(map(lambda row: is_safe(row), prepared))


def leave_one_out(x: list[T1]) -> list[list[T1]]:
    combinations = []
    for i in range(len(x)):
        x_ = x[:]
        x_.pop(i)
        combinations.append(x_)
    return combinations


def part2(raw: list[str]) -> int:
    prepared = prepare_input(raw)
    return sum(map(lambda row: any(map(is_safe, leave_one_out(row))), prepared))


aoc = AoC(day=2, year=2024, part_1=part1, part_2=part2)

sample_input = """
    7 6 4 2 1
    1 2 7 8 9
    9 7 6 2 1
    1 3 2 4 5
    8 6 4 4 1
    1 3 6 7 9
"""
sample_input = textwrap.dedent(sample_input).strip()

# Run function with sample input and assert the expected result
aoc.assert_p1(sample_input, 2)
aoc.assert_p2(sample_input, 4)

# Submit solutions
aoc.submit_p1()
aoc.submit_p2()
