from collections import Counter
from functools import lru_cache
from itertools import product

d_positions_with_frequency = Counter(sum(combination) for combination in product((1, 2, 3), repeat=3))


@lru_cache(maxsize=None)
def recurse(positions, remaining_scores, player_index):
    if remaining_scores[0] <= 0:
        return 1, 0
    elif remaining_scores[1] <= 0:
        return 0, 1
    else:
        wins_per_player = [0, 0]
        for d_position, frequency in d_positions_with_frequency.items():
            if player_index == 0:
                new_positions = ((positions[0] + d_position) % 10, positions[1])
                new_remaining_scores = (remaining_scores[0] - new_positions[0] - 1, remaining_scores[1])
            else:
                new_positions = (positions[0], (positions[1] + d_position) % 10)
                new_remaining_scores = (remaining_scores[0], remaining_scores[1] - new_positions[1] - 1)
            wins_per_player_recurse = recurse(new_positions, new_remaining_scores, (player_index + 1) % 2)
            wins_per_player[0] += frequency * wins_per_player_recurse[0]
            wins_per_player[1] += frequency * wins_per_player_recurse[1]
        return wins_per_player


wins_per_player = recurse((3, 2), (21, 21), 0)
print(f"Part 2: {max(wins_per_player)}")
