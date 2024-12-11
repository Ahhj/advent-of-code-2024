import textwrap
from typing import Literal
from tqdm import tqdm

from adventofcode import AoC
from collections import defaultdict

Position = tuple[int, int]
Direction = Literal[">", "<", "^", "v"]

TURN_DIRECTIONS: dict[Direction, Direction] = {
    "^": ">",
    "v": "<",
    ">": "v",
    "<": "^"
}
POSITION_UPDATES: dict[Direction, Position] = {
    ">": (1, 0),
    "<": (-1, 0),
    "^": (0, -1),
    "v": (0, 1),
}


def prepare_input(raw: str) -> tuple[Position, Direction, list[Position], tuple[int, int]]:
    position = None
    direction = None
    obstacles = []
    dimensions = (len(raw[0]), len(raw))

    for y, row in enumerate(raw):
        for x, col in enumerate(row):
            if col == ".":
                continue
            elif col == "#":
                obstacles.append((x, y))
            else:
                position = (x, y)
                direction = col

    return position, direction, obstacles, dimensions


def walk_until_stopped(
    position: Position,
    direction: Direction,
    obstacles: list[Position],
    dimensions: tuple[int, int],
) -> dict[tuple[Position, Direction], bool]:
    # Lookups to speed up conditional checking 
    history = defaultdict(lambda: 0)  # Count of being at a given position with a given direction
    obstacle_lookup = defaultdict(lambda: False)  # Flag positions with obstacles
    boundary_lookup = defaultdict(lambda: False)  # Flag boundary positions

    for obstacle in obstacles:
        obstacle_lookup[obstacle] = True

    xmax, ymax = dimensions
    for x in range(-1, xmax+1):
        boundary_lookup[(x, -1)] = True
        boundary_lookup[(x, ymax)] = True

    for y in range(-1, ymax+1):
        boundary_lookup[(-1, y)] = True
        boundary_lookup[(xmax, y)] = True

    # Try to take a step, change direction if the way is blocked
    def try_update(position: Position, direction: Direction) -> tuple[Position, Direction]:
        x, y = position
        dx, dy = POSITION_UPDATES[direction]
        x_ = x + dx
        y_ = y + dy
        
        if obstacle_lookup[(x_, y_)]:
            new_direction = TURN_DIRECTIONS[direction]
            return try_update(position, new_direction)
        
        new_position = (x_, y_)
        return new_position, direction

    def within_boundary(position: Position) -> bool:
        return not boundary_lookup[position]

    def no_loops(position: Position, direction: Direction) -> bool:
        return history[(position, direction)] < 2
            
    while within_boundary(position) and no_loops(position, direction):
        history[(position, direction)] += 1
        position, direction = try_update(position, direction)

    return history


def part1(raw: str) -> int:
    position, direction, obstacles, dimensions = prepare_input(raw)
    history = walk_until_stopped(position, direction, obstacles, dimensions)
    path, _ = zip(*history)
    return len(set(path))


def part2(raw: str) -> int:
    position, direction, obstacles, dimensions = prepare_input(raw)
    
    # Initial walk
    history = walk_until_stopped(position, direction, obstacles, dimensions)
    initial_path, _ = zip(*history)

    # Insert new obstacle at unique positions along the initial path
    loop_count = 0
    for insert_position in tqdm(set(initial_path)):
        new_obstacles = [*obstacles, insert_position]
        history = walk_until_stopped(position, direction, new_obstacles, dimensions)

        # Any positions/directions appear twice?
        loop_count += any((v > 1 for v in history.values()))

    return loop_count


aoc = AoC(day=6, year=2024, part_1=part1, part_2=part2)

sample_input = """
    ....#.....
    .........#
    ..........
    ..#.......
    .......#..
    ..........
    .#..^.....
    ........#.
    #.........
    ......#...

"""
sample_input = textwrap.dedent(sample_input).strip()

# Run function with sample input and assert the expected result
aoc.assert_p1(sample_input, 41)
aoc.assert_p2(sample_input, 6)

# Submit solutions
aoc.submit_p1()
aoc.submit_p2()
