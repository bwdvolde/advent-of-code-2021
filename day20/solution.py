from util.read_file import read_file

lines = read_file("input.txt")

iterator = iter(lines)
algorithm_string = next(iterator)
next(iterator)

lit_positions = set()

r = 0
while line := next(iterator):
    c = 0
    for char in line:
        if char == "#":
            lit_positions.add((r, c))
        c += 1
    r += 1

n_steps = 50
borders_lit = False
for step in range(n_steps):
    min_r = min(position[0] for position in lit_positions) - 1
    max_r = max(position[0] for position in lit_positions) + 1
    min_c = min(position[1] for position in lit_positions) - 1
    max_c = max(position[1] for position in lit_positions) + 1


    def calculate_index(r, c):
        index = 0
        for _r in [r - 1, r, r + 1]:
            for _c in [c - 1, c, c + 1]:
                if not (min_r + 1 <= _r <= max_r - 1 and min_c + 1 <= _c <= max_c - 1):
                    index = index * 2 + 1 if borders_lit else index * 2
                else:
                    index = index * 2 + 1 if (_r, _c) in lit_positions else index * 2

        return index


    new_lit_positions = set()
    for r in range(min_r, max_r + 1):
        for c in range(min_c, max_c + 1):
            if algorithm_string[calculate_index(r, c)] == "#":
                new_lit_positions.add((r, c))
    lit_positions = new_lit_positions

    # Assuming that the default value always changes between lit and not lit
    if algorithm_string[0] == "#":
        borders_lit = not borders_lit

    if step == 0:
        print("#" * (max_c - min_c + 2))

print(len(lit_positions))
