class Dice:

    def __init__(self):
        self.next_roll = 1
        self.n_rolls = 0

    def __next__(self):
        to_return = self.next_roll
        self.next_roll = (self.next_roll + 1) % 100
        self.n_rolls += 1
        return to_return


positions = [3, 2]
scores = [0, 0]
next_dice_roll = 1
player_index = 0
dice = Dice()

while all(score < 1000 for score in scores):
    d_position = next(dice) + next(dice) + next(dice)
    positions[player_index] = (positions[player_index] + d_position) % 10
    scores[player_index] += positions[player_index] + 1
    player_index = (player_index + 1) % 2

part_1 = dice.n_rolls * min(scores)
print(f"Part 1: {part_1}")
