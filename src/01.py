from adventofcode import AoC
import textwrap
from itertools import starmap
from collections import Counter


def split_pairs(pairs: list[str]) -> tuple[list[str], list[str]]:
    # Extract left and right lists
    # Assumes each item is a pair
    ids_raw = [x.split() for x in pairs]
    left, right = zip(*ids_raw)
    return left, right


def prepare_input(raw: list[str]) -> tuple[list[int], list[int]]:
    left, right = split_pairs(raw)

    # Cast to integers
    left = map(int, left)
    right = map(int, right)
    return left, right


def part1(raw: list[str]) -> int:
    left, right = prepare_input(raw)    

    # Pair the sorted ids
    ids_sorted = zip(sorted(left), sorted(right))
    
    # Calculate distances
    distances = starmap(lambda x, y: abs(x-y), ids_sorted)
    total_distance = sum(distances)
    
    return total_distance


def part2(raw: list[str]) -> int:
    left, right = prepare_input(raw)
    # Count each unique integer in the right list
    right_counts = Counter(right)  # {number: count}
    score = sum([x * right_counts[x] for x in left])
    return score


aoc = AoC(day=1, year=2024, part_1=part1, part_2=part2)

sample_input = """
    3   4
    4   3
    2   5
    1   3
    3   9
    3   3
"""
sample_input = textwrap.dedent(sample_input).strip()

# Run function with sample input and assert the expected result
aoc.assert_p1(sample_input, 11)
aoc.assert_p2(sample_input, 31)

# Submit solutions
aoc.submit_p1()
aoc.submit_p2()
