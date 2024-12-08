import textwrap

from adventofcode import AoC


def prepare_input(raw: str) -> str:
    split_idx = raw.index("")
    rules_raw, updates_raw = raw[:split_idx], raw[split_idx+1:]
    rules = [tuple(map(int, rule.split("|"))) for rule in rules_raw]
    updates = [list(map(int, update.split(","))) for update in updates_raw]
    return rules, updates


def part1(raw: str) -> int:
    rules, updates = prepare_input(raw)

    def check_rules(update: list[int]) -> bool:
        for x, y in rules:
            if x in update and y in update:
                if update.index(x) > update.index(y):
                    return False
        else:
            return True

    valid_updates = list(filter(check_rules, updates))
    total = sum(update[len(update) // 2] for update in valid_updates)
    return total


def part2(raw: str) -> int:
    rules, updates = prepare_input(raw)
    
    def apply_rules(update: list[int]) -> tuple[list[int], bool]:
        update_fixed = update[:]
        did_fix = False

        # Subset of rules given the pages affected.
        rules_filtered = [(x, y) for x, y in rules if x in update and y in update]
        rules_passing = False

        while not rules_passing:  # Keep applying rules until they all pass
            for x, y in rules_filtered:
                i = update_fixed.index(x)
                j = update_fixed.index(y)
                if i > j:
                    update_fixed.pop(j)
                    update_fixed.insert(i, y)
                    did_fix = True
                    break  # Restart the sweep
            else:
                rules_passing = True  # All rules passed

        return update_fixed, did_fix

    updates_fixed = map(apply_rules, updates)
    updates_invalid = [update for update, did_fix in updates_fixed if did_fix]
    total = sum(update[len(update) // 2] for update in updates_invalid)
    return total


aoc = AoC(day=5, year=2024, part_1=part1, part_2=part2)

sample_input = """
    47|53
    97|13
    97|61
    97|47
    75|29
    61|13
    75|53
    29|13
    97|29
    53|29
    61|53
    97|53
    61|29
    47|13
    75|47
    97|75
    47|61
    75|61
    47|29
    75|13
    53|13

    75,47,61,53,29
    97,61,53,29,13
    75,29,13
    75,97,47,61,53
    61,13,29
    97,13,75,29,47
"""
sample_input = textwrap.dedent(sample_input).strip()

# Run function with sample input and assert the expected result
aoc.assert_p1(sample_input, 143)
aoc.assert_p2(sample_input, 123)

# Submit solutions
aoc.submit_p1()
aoc.submit_p2()
