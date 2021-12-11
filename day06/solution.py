from collections import Counter, defaultdict

from util.read_file import read_file

lines = read_file("input.txt")
lines = [int(x) for x in lines[0].split(",")]


def calculate_n_fish_after(n_days):
    counts = Counter(lines)
    for _ in range(n_days):
        new_counts = defaultdict(lambda: 0)
        for days_left, amount in counts.items():
            if days_left == 0:
                new_counts[6] += amount
                new_counts[8] += amount
            else:
                new_counts[days_left - 1] += amount
        counts = new_counts
    return sum(counts.values())


print(f"Part 1: {calculate_n_fish_after(80)}")
print(f"Part 1: {calculate_n_fish_after(256)}")
