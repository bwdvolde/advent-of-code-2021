import re
from collections import defaultdict

from util.read_file import read_file


def parse_file():
    lines = read_file("input.txt")[:-1]

    segments = []
    for line in lines:
        result = re.search("(.*),(.*) -> (.*),(.*)", line)
        groups = result.groups()
        segments.append(((int(groups[0]), int(groups[1])), (int(groups[2]), int(groups[3]))))
    return segments


def calculate_at_least_two_overlaps(segments, include_diagonal):
    if not include_diagonal:
        segments = [
            segment for segment in segments if
            segment[0][0] == segment[1][0] or segment[0][1] == segment[1][1]
        ]

    n_overlaps = defaultdict(lambda: 0)
    for segment in segments:
        dx = segment[1][0] - segment[0][0]
        dy = segment[1][1] - segment[0][1]
        dx /= abs(dx) if dx else 1
        dy /= abs(dy) if dy else 1
        current = segment[0]

        n_overlaps[current] += 1
        while current != segment[1]:
            current = current[0] + dx, current[1] + dy
            n_overlaps[current] += 1
    answer = 0
    for point, overlaps in n_overlaps.items():
        if overlaps >= 2:
            answer += 1
    return answer


if __name__ == '__main__':
    segments = parse_file()
    print(f"Part 1: {calculate_at_least_two_overlaps(segments, include_diagonal=False)}")
    print(f"Part 2: {calculate_at_least_two_overlaps(segments, include_diagonal=True)}")
