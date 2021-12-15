from dataclasses import dataclass

from util.read_file import read_file


@dataclass
class Point:
    col: int
    row: int


@dataclass
class Fold:
    char: str
    coordinate: int


lines = read_file("input.txt")

points = []
iterator = iter(lines)
while line := next(iterator):
    point = Point(*(int(x) for x in line.split(",")))
    points.append(point)

folds = []
while True:
    try:
        line = next(iterator)
        if line:
            char, coordinate = line[11:].split("=")
            coordinate = int(coordinate)
            folds.append(Fold(char, coordinate))
    except StopIteration:
        break

n_rows = max(point.row for point in points) + 1
n_cols = max(point.col for point in points) + 1

grid = [[False for _ in range(n_cols)] for _ in range(n_rows)]
for point in points:
    grid[point.row][point.col] = True

for i, fold in enumerate(folds):
    if fold.char == "y":
        new_n_rows = fold.coordinate
        new_n_cols = n_cols
        for r in range(fold.coordinate + 1, n_rows):
            for c in range(n_cols):
                grid[2 * fold.coordinate - r][c] |= grid[r][c]

    else:
        new_n_rows = n_rows
        new_n_cols = fold.coordinate
        for r in range(n_rows):
            for c in range(fold.coordinate + 1, n_cols):
                grid[r][2 * fold.coordinate - c] |= grid[r][c]

    n_rows = new_n_rows
    n_cols = new_n_cols

    if i == 0:
        points_left = sum(1 for r in range(n_rows) for c in range(n_cols) if grid[r][c])
        print(f"Part 1: {points_left}")

grid = [col[:n_cols] for col in grid[:n_rows]]
print("Part 2:")
for row in grid:
    for c in row:
        if c:
            print("X", end="")
        else:
            print(" ", end="")
    print()
print()
