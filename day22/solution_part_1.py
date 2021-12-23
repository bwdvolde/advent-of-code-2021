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


lines = read_file("example.txt")[:-1]

cuboids = []
for line in lines:
    params = re.match("(on|off) x=(-?[0-9]+)..(-?[0-9]+),y=(-?[0-9]+)..(-?[0-9]+),z=(-?[0-9]+)..(-?[0-9]+)",
                      line).groups()
    cuboids.append(Cuboid(*[int(param) if param not in ["on", "off"] else param == "on" for param in params]))

on_cubes = set()
for cuboid in cuboids:
    if cuboid.min_x >= -50 and cuboid.max_x <= 50 and cuboid.min_y >= -50 and cuboid.max_y <= 50 and cuboid.min_z >= -50 and cuboid.max_z <= 50:
        for x in range(cuboid.min_x, cuboid.max_x + 1):
            for y in range(cuboid.min_y, cuboid.max_y + 1):
                for z in range(cuboid.min_z, cuboid.max_z + 1):
                    if cuboid.is_on:
                        on_cubes.add((x, y, z))
                    else:
                        if (x, y, z) in on_cubes:
                            on_cubes.remove((x, y, z))
    print(len(on_cubes))
