import textwrap
from itertools import combinations

from adventofcode import AoC


NEAREST_NEIGHBOURS = [
    (-1, -1), (-1, 0), (-1, 1), 
    (0, -1), (0, 1),  # Excludes (0, 0)
    (1, -1), (1, 0), (1, 1)
]


def prepare_input(raw: str) -> str:
    return list(map(list, raw))


def get_word_coordinates(grid: list[list[str]], word: str) -> list[list[tuple[int]]]:
    """
    Builds a list-of-list with the coords of each letter in the word.

    E.g. if in XMAS, the 'X' is in the grid at (0, 0) and (2, 4), then the first 
    element of the list will be [(0, 0), (2, 4)].

    The returned list will have the same length as the input word.
    """
    word_coords = []  

    for word_letter in word:
        word_coords.append([])

        for row_idx, row in enumerate(grid):
            for col_idx, grid_letter in enumerate(row):
                if word_letter == grid_letter:
                    word_coords[-1].append((row_idx, col_idx))
            
    return word_coords


def find_remaining_letters(
    word_coords: list[list[str]], 
    current_pos=0, 
    sequences=None
) -> list[list[tuple[int]]]:
    """
    Recursive function. Finds the viable sequences of coordinates 
    for the remaining letters.
    """
    next_pos = current_pos + 1

    if next_pos == len(word_coords):
        # Word completed
        return sequences

    # All the locations of the next letter in the sequence
    possible_moves = word_coords[next_pos]

    if sequences is None:
        # Start new sequences from the current position in the word
        sequences = [[c] for c in word_coords[current_pos]]

    # Starting from the existing sequences, find all possible subsequences
    # given the coordinates of the next letter in the word.
    new_sequences = []
    for seq in sequences:
        i, j = seq[-1]

        if len(seq) > 1:
            # If we already have letters, ensure the sequence is linear
            i_prev, j_prev = seq[-2]
            diffs = [(i - i_prev, j - j_prev)]
        else:
            # Search all neighbours if we only have a single letter
            diffs = NEAREST_NEIGHBOURS

        for di, dj in diffs:
            # Coordinates to check
            i_ = i + di
            j_ = j + dj

            # Check if coordinates are viable
            if (i_, j_) in possible_moves:
                # Restart the search from the position of the neighbour
                new_sequences += find_remaining_letters(word_coords, next_pos, sequences=[[*seq, (i_, j_)]])

    sequences = new_sequences[:]

    return sequences


def part1(raw: str) -> int:
    prepared = prepare_input(raw)
    word = "XMAS"
    coords = get_word_coordinates(prepared, word)            
    sequences = find_remaining_letters(coords, current_pos=0)
    return len(sequences)


def part2(raw: str) -> int:
    prepared = prepare_input(raw)
    word = "MAS"
    coords = get_word_coordinates(prepared, word)            
    sequences = find_remaining_letters(coords, current_pos=0)
    x_sequences = []

    def do_cross(s1, s2):
        return s1[1] == s2[1]
    
    def is_diagonal(seq):
        x1, y1 = seq[0]
        x2, y2 = seq[1]
        return abs(x1 - x2) == 1 and abs(y1 - y2) == 1 
    
    for s1, s2 in combinations(filter(is_diagonal, sequences), 2):
        if s1 == s2:
            continue

        if do_cross(s1, s2):
            x_sequences.append([s1, s2])

    return len(x_sequences)


aoc = AoC(day=4, year=2024, part_1=part1, part_2=part2)

sample_input = """
    MMMSXXMASM
    MSAMXMSMSA
    AMXSXMAAMM
    MSAMASMSMX
    XMASAMXAMM
    XXAMMXXAMA
    SMSMSASXSS
    SAXAMASAAA
    MAMMMXMMMM
    MXMXAXMASX
"""
sample_input = textwrap.dedent(sample_input).strip()

# Run function with sample input and assert the expected result
aoc.assert_p1(sample_input, 18)
aoc.assert_p2(sample_input, 9)

# Submit solutions
aoc.submit_p1()
aoc.submit_p2()
