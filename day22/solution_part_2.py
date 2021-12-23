import re
from dataclasses import dataclass

from util.read_file import read_file


@dataclass
class Cuboid:
    is_on: bool
    min_x: int
    max_x: int
    min_y: int
    max_y: int
    min_z: int
    max_z: int

    def __eq__(self, other):
        return self.min_x == other.min_x and self.max_x == other.max_x \
               and self.min_y == other.min_y and self.max_y == other.max_y \
               and self.min_z == other.min_z and self.max_z == other.max_z

    def is_valid(self):
        return self.min_x <= self.max_x and self.min_y <= self.max_y and self.min_z <= self.max_z


lines = read_file("input.txt")[:-1]


def overlaps(a: Cuboid, b: Cuboid) -> bool:
    return max(a.min_x, b.min_x) <= min(a.max_x, b.max_x) \
           and max(a.min_y, b.min_y) <= min(a.max_y, b.max_y) \
           and max(a.min_z, b.min_z) <= min(a.max_z, b.max_z)


def overlapping_cuboid(a: Cuboid, b: Cuboid) -> Cuboid:
    return Cuboid(
        True,
        max(a.min_x, b.min_x),
        min(a.max_x, b.max_x),
        max(a.min_y, b.min_y),
        min(a.max_y, b.max_y),
        max(a.min_z, b.min_z),
        min(a.max_z, b.max_z),
    )


def remove_from(cuboid: Cuboid, overlap: Cuboid) -> list[Cuboid]:
    x_pairs = [(cuboid.min_x, overlap.min_x - 1), (overlap.min_x, overlap.max_x), (overlap.max_x + 1, cuboid.max_x)]
    y_pairs = [(cuboid.min_y, overlap.min_y - 1), (overlap.min_y, overlap.max_y), (overlap.max_y + 1, cuboid.max_y)]
    z_pairs = [(cuboid.min_z, overlap.min_z - 1), (overlap.min_z, overlap.max_z), (overlap.max_z + 1, cuboid.max_z)]
    resulting_cuboids = []
    for x_pair in x_pairs:
        for y_pair in y_pairs:
            for z_pair in z_pairs:
                cuboid = Cuboid(False, *x_pair, *y_pair, *z_pair)
                if cuboid != overlap and cuboid.is_valid():
                    resulting_cuboids.append(cuboid)
    return resulting_cuboids


def calculate_n_on_cuboids(cuboids: list[Cuboid]) -> int:
    answer = 0
    for cuboid in cuboids:
        answer += (cuboid.max_x - cuboid.min_x + 1) * (cuboid.max_y - cuboid.min_y + 1) * (
                cuboid.max_z - cuboid.min_z + 1)
    return answer


cuboids = []
for line in lines:
    params = re.match("(on|off) x=(-?[0-9]+)..(-?[0-9]+),y=(-?[0-9]+)..(-?[0-9]+),z=(-?[0-9]+)..(-?[0-9]+)",
                      line).groups()
    cuboids.append(Cuboid(*[int(param) if param not in ["on", "off"] else param == "on" for param in params]))

on_cuboids = []

for cuboid in cuboids:
    new_on_cuboids = []
    if not on_cuboids and cuboid.is_on:
        new_on_cuboids = [cuboid]
    else:
        for on_cuboid in on_cuboids:
            if overlaps(cuboid, on_cuboid):
                overlap = overlapping_cuboid(cuboid, on_cuboid)
                new_on_cuboids.extend(remove_from(on_cuboid, overlap))
            else:
                new_on_cuboids.append(on_cuboid)
        if cuboid.is_on:
            new_on_cuboids.append(cuboid)
    on_cuboids = new_on_cuboids

print(f"Part 2: {calculate_n_on_cuboids(on_cuboids)}")
