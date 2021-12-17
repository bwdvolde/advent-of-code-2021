from dataclasses import dataclass

from util.read_file import read_file


@dataclass
class Bounds:
    x_min: int
    x_max: int
    y_min: int
    y_max: int


line = read_file("input.txt")[0]

x_str, y_str = line[15:].split(", y=")
bounds = Bounds(*map(int, x_str.split("..")), *map(int, y_str.split("..")))


def simulate(dx, dy):
    x, y = 0, 0
    y_max = 0
    while x <= bounds.x_max and y >= bounds.y_min:
        x, y = x + dx, y + dy
        y_max = max(y_max, y)
        if bounds.x_min <= x <= bounds.x_max and bounds.y_min <= y <= bounds.y_max:
            return True, y_max
        dx = max(0, dx - 1)
        dy -= 1

    return False, None


answer_part_1 = 0
velocities_meeting_criteria = set()
for dx in range(bounds.x_max + 1):
    for dy in range(-1000, 1000):
        in_range, highest_pos = simulate(dx, dy)
        if in_range:
            answer_part_1 = max(answer_part_1, highest_pos)
            velocities_meeting_criteria.add((dx, dy))

print(f"Part 1: {answer_part_1}")
print(f"Part 2: {len(velocities_meeting_criteria)}")
