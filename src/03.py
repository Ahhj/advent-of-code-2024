from adventofcode import AoC
import textwrap
import re


def prepare_input(raw: str) -> str:
    return "".join(raw).strip()


def part1(raw: str) -> int:
    prepared = prepare_input(raw)
    pattern = re.compile(r"(mul\(\d{1,3},\d{1,3}\))")
    total = 0
    for match in pattern.finditer(prepared):
        x, y = re.findall(r"\d{1,3}", match.group(0))
        total += int(x) * int(y)

    return total


def part2(raw: str) -> int:
    prepared = "do()" + prepare_input(raw)
    do_sections = []
    for section in prepared.split("don't()"):
        _, *do_parts = section.split("do()")
        do_sections += do_parts
    
    return part1("".join(do_sections))
    

aoc = AoC(day=3, year=2024, part_1=part1, part_2=part2)

sample_input = """
    xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))
"""
sample_input = textwrap.dedent(sample_input).strip()

# Run function with sample input and assert the expected result
aoc.assert_p1(sample_input, 161)
aoc.assert_p2(sample_input, 48)

# Submit solutions
aoc.submit_p1()
aoc.submit_p2()
