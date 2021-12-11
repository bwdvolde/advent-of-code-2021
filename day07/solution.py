from util.read_file import read_file

positions = [int(x) for x in read_file("input.txt")[0].split(",")]

lower_bound = min(positions)
upper_bound = max(positions)


def calculate_fuel_needed_part_1(position):
    return sum(abs(position - x) for x in positions)


def calculate_fuel_needed_part_2(position):
    fuel_needed = 0
    for x in positions:
        n = abs(x - position)
        fuel_needed += n * (n + 1) // 2
    return fuel_needed


min_fuel_needed_part_1 = min(calculate_fuel_needed_part_1(position) for position in range(lower_bound, upper_bound + 1))
print(f"Part 1: {min_fuel_needed_part_1}")

min_fuel_needed_part_2 = min(calculate_fuel_needed_part_2(position) for position in range(lower_bound, upper_bound + 2))
print(f"Part 2: {min_fuel_needed_part_2}")
