import textwrap
import operator as op
import itertools
from collections import defaultdict
from functools import reduce
from typing import TypeVar, Iterable, Callable

from tqdm import tqdm

from adventofcode import AoC

T = TypeVar("T")


def prepare_input(raw: str) -> list[tuple[int, list[int]]]:
    prepared = []
    for line in raw:
        test_value, input_values = line.split(":")
        prepared.append(
            (int(test_value), list(map(int, input_values.split())))
        )
    return prepared


def reduce_iter(funcs: Iterable[Callable[[T, T], T]], values: Iterable[T], initial_value: T):
    funcs_iter = iter(funcs)

    def next_func(left: T, right: T) -> T:
        func = next(funcs_iter)
        return func(left, right)

    result = reduce(next_func, values, initial_value)
    return result


def product_range(sequence: Iterable[T], max_repeat=1) -> dict[int, list[T]]:
    products = defaultdict(list)
    for repeat in range(1, max_repeat):
        for perm in itertools.product(sequence, repeat=repeat):
            products[repeat].append(list(perm))

    return products


def part1(raw: str) -> int:
    prepared = prepare_input(raw)

    # All possible combinations of operations for all input sequence lengths
    max_n = max([len(input_values) for _, input_values in prepared])
    operations = product_range([op.add, op.mul], max_n)
    
    valid_tests = []
    for test_value, input_values in tqdm(prepared):
        for seq in operations[len(input_values) - 1]:
            # Apply the operations and check against the test value
            result = reduce_iter(seq, input_values[1:], input_values[0])

            if result == test_value:
                valid_tests.append(test_value)
                break

    return sum(valid_tests)


def concat(left: int, right: int) -> int:
    return int(f"{left}{right}")


def part2(raw: str) -> int:
    prepared = prepare_input(raw)

    # All possible combinations of operations for all input sequence lengths
    max_n = max([len(input_values) for _, input_values in prepared])
    operations = product_range([op.add, op.mul, concat], max_n)
    
    valid_tests = []
    for test_value, input_values in tqdm(prepared):
        for seq in operations[len(input_values) - 1]:
            # Apply the operations and check against the test value
            result = reduce_iter(seq, input_values[1:], input_values[0])

            if result == test_value:
                valid_tests.append(test_value)
                break

    return sum(valid_tests)


aoc = AoC(day=7, year=2024, part_1=part1, part_2=part2)

sample_input = """
    190: 10 19
    3267: 81 40 27
    83: 17 5
    156: 15 6
    7290: 6 8 6 15
    161011: 16 10 13
    192: 17 8 14
    21037: 9 7 18 13
    292: 11 6 16 20
"""
sample_input = textwrap.dedent(sample_input).strip()

# Run function with sample input and assert the expected result
aoc.assert_p1(sample_input, 3749)
aoc.assert_p2(sample_input, 11387)

# Submit solutions
# aoc.submit_p1()
aoc.submit_p2()
