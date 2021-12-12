import math
from collections import Counter
from functools import lru_cache

from util.read_file import read_file

lines = read_file("input.txt")[:-1]

grid = [[int(x) for x in line] for line in lines]


def neighbors(r, c):
    possible_coords = [
        (r - 1, c),
        (r + 1, c),
        (r, c - 1),
        (r, c + 1),
    ]
    return [(_r, _c) for (_r, _c) in possible_coords if 0 <= _r < len(grid) and 0 <= _c < len(grid[0])]


def is_low_point(r, c):
    return all(grid[r][c] < grid[_r][_c] for (_r, _c) in neighbors(r, c))


part_1 = 0
for r, row in enumerate(grid):
    for c, height in enumerate(grid[r]):
        if is_low_point(r, c):
            part_1 += height + 1
print(f"Part 1: {part_1}")


@lru_cache
def calculate_basin(r, c):
    if grid[r][c] == 9:
        return None
    elif is_low_point(r, c):
        return r, c
    else:
        random_lower_neighbor = [(_r, _c) for (_r, _c) in neighbors(r, c) if grid[_r][_c] < grid[r][c]][0]
        return calculate_basin(*random_lower_neighbor)


basins = [calculate_basin(r, c) for r, row in enumerate(grid) for c in range(len(grid[r]))]
basins = [basin for basin in basins if basin]
basin_counts = Counter(basins)
basin_sizes = list(basin_counts.values())
basin_sizes.sort(reverse=True)
part_2 = math.prod(basin_sizes[:3])
print(f"Part 2: {part_2}")
