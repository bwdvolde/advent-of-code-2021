from util.read_file import read_file

closing_to_open = {
    ")": "(",
    "]": "[",
    "}": "{",
    ">": "<",
}
closing = closing_to_open.keys()
open = closing_to_open.values()

points = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137
}

lines = read_file("input.txt")[:-1]

not_corrupt_lines = []
corrupt_score = 0
for line in lines:
    corrupt = False
    stack = []
    for c in line:
        if c in open:
            stack.append(c)
        else:
            pop = stack.pop()
            if closing_to_open[c] != pop:
                corrupt = True
                corrupt_score += points[c]
    if not corrupt:
        not_corrupt_lines.append(line)
print(f"Part 1: {corrupt_score}")

scores_part_2 = {
    "(": 1,
    "[": 2,
    "{": 3,
    "<": 4,
}

scores = []
for line in not_corrupt_lines:
    stack = []

    for c in line:
        if c in open:
            stack.append(c)
        else:
            stack.pop()

    score_line = 0
    while stack:
        score_line = score_line * 5 + scores_part_2[stack.pop()]
    scores.append(score_line)

scores.sort()
middle_score = scores[len(scores) // 2]
print(f"Part 2: {middle_score}")
