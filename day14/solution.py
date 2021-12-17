from collections import Counter, defaultdict
from functools import lru_cache

from util.read_file import read_file

lines = read_file("input.txt")[:-1]

iterator = iter(lines)
template = next(iterator)
next(iterator)

rules = {}
while True:
    try:
        a, b = next(iterator).split(" -> ")
        rules[a] = b
    except StopIteration:
        break

count_of = defaultdict(lambda: 0)
for pair in zip(template, template[1:]):
    count_of[pair] += 1

n_steps = 40
for _ in range(n_steps):
    new_count_of = defaultdict(lambda: 0)
    for pair, count in count_of.items():
        middle = rules["".join(pair)]
        new_pairs = [(pair[0], middle), (middle, pair[1])]
        for new_pair in new_pairs:
            new_count_of[new_pair] += count
    count_of = new_count_of

letter_counts = defaultdict(lambda: 0)
for pair, count in count_of.items():
    letter_counts[pair[0]] += count
    letter_counts[pair[1]] += count

actual_counts = {letter: (count // 2) + (count % 2) for (letter, count) in letter_counts.items()}
answer = max(actual_counts.values()) - min(actual_counts.values())
print(f"Part 2: {answer}")
