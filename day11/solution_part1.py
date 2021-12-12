from util.read_file import read_file

lines = read_file("input.txt")[:-1]

grid = [[int(x) for x in line] for line in lines]


def neighbors(r, c):
    possible_coords = [
        (r - 1, c),
        (r + 1, c),
        (r, c - 1),
        (r, c + 1),
        (r + 1, c + 1),
        (r - 1, c - 1),
        (r - 1, c + 1),
        (r + 1, c - 1),
    ]
    return [(_r, _c) for (_r, _c) in possible_coords if 0 <= _r < len(grid) and 0 <= _c < len(grid[0])]


n_steps = 100
step = 0
total_flashes = 0
while step < n_steps:
    flashed_before = set()
    positions_to_flash = set()
    for r, row in enumerate(grid):
        for c, _ in enumerate(row):
            grid[r][c] += 1
            if grid[r][c] > 9:
                positions_to_flash.add((r, c))

    while positions_to_flash:
        r, c = positions_to_flash.pop()
        for nr, nc in neighbors(r, c):
            grid[nr][nc] += 1
            if grid[nr][nc] > 9 and (nr, nc) not in flashed_before:
                positions_to_flash.add((nr, nc))

        flashed_before.add((r, c))

    for r, c in flashed_before:
        grid[r][c] = 0

    total_flashes += len(flashed_before)
    step += 1

print(f"Part 1: {total_flashes}")
