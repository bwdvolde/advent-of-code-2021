from dataclasses import dataclass
from functools import lru_cache
from typing import List

from util.read_file import read_file


@dataclass(frozen=True)
class Point:
    x: int
    y: int
    z: int

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y, self.z - other.z)


def roll(v): return (v[0], v[2], -v[1])


def turn(v): return (-v[1], v[0], v[2])


def all_possible_rotations(point: Point) -> List[Point]:
    v = [point.x, point.y, point.z]
    rotations = []
    for cycle in range(2):
        for step in range(3):
            v = roll(v)
            rotations.append(Point(*v))
            for i in range(3):
                v = turn(v)
                rotations.append(Point(*v))
        v = roll(turn(roll(v)))
    return rotations


@lru_cache
def all_possible_rotations_many(points: tuple[Point]) -> list[tuple[Point]]:
    result = [[] for _ in range(24)]
    for point in points:
        for i, rotation in enumerate(all_possible_rotations(point)):
            result[i].append(rotation)
    return [tuple(row) for row in result]


def calculate_diff_matrix(points: List[Point]):
    diffs = []
    for a in points:
        distances_a = []
        for b in points:
            distances_a.append((a.x - b.x, a.y - b.y, a.z - b.z))
        diffs.append(distances_a)
    return diffs


lines = read_file("input.txt")

scanners = []
iterator = iter(lines)
while True:
    try:
        points = []
        next(iterator)  # Skip header of scanner
        while line := next(iterator):
            points.append(Point(*[int(x) for x in line.split(",")]))
        scanners.append(tuple(points))
    except StopIteration:
        break


@lru_cache
def find_equal_points(scanner_a, scanner_b):
    diff_matrix_a = calculate_diff_matrix(scanner_a)
    diff_matrix_b = calculate_diff_matrix(scanner_b)

    for point_a, diff_matrix_row_a in zip(scanner_a, diff_matrix_a):
        for point_b, diff_matrix_row_b in zip(scanner_b, diff_matrix_b):
            overlapping_points = set(diff_matrix_row_b) & set(diff_matrix_row_a)
            if len(overlapping_points) >= 12:
                return point_b.x - point_a.x, point_b.y - point_a.y, point_b.z - point_a.z
    return None


scanners = scanners
found_scanners = [scanners[0]]
remaining_scanners = scanners[1:]
scanner_locations = [Point(0, 0, 0)]
while remaining_scanners:
    new_scanner = None

    for remaining_scanner in remaining_scanners:
        for rotated_remaining_scanner in all_possible_rotations_many(remaining_scanner):
            for found_scanner in found_scanners:
                diff = find_equal_points(found_scanner, rotated_remaining_scanner)
                if diff:
                    print("Found a scanner")
                    new_scanner = tuple(Point(point.x - diff[0], point.y - diff[1], point.z - diff[2]) for point in
                                        rotated_remaining_scanner)
                    scanner_locations.append(new_scanner[0] - rotated_remaining_scanner[0])
                    to_remove = remaining_scanner
                    break
            if new_scanner:
                break
        if new_scanner:
            break

    remaining_scanners.remove(to_remove)
    found_scanners.append(new_scanner)

beacons = set(point for scanner in found_scanners for point in scanner)
beacons = sorted(beacons, key=lambda point: point.x)
print(f"Part 1: {len(beacons)}")


def manhattan_distance(a: Point, b: Point) -> int:
    return abs(a.x - b.x) + abs(a.y - b.y) + abs(a.z - b.z)


part_2 = max(manhattan_distance(a, b) for a in scanner_locations for b in scanner_locations)
print(f"Part 2: {part_2}")
