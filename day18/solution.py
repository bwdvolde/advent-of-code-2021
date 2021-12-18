from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from itertools import combinations, permutations
from typing import Optional, List

from util.read_file import read_file


@dataclass(eq=False)
class Node:
    left: Optional[Node]
    right: Optional[Node]
    value: Optional[int]

    def __str__(self):
        if self.value is not None:
            return str(self.value)
        return f"[{self.left},{self.right}]"


def parse_line(line):
    i = 0

    def recurse() -> Node:
        nonlocal i
        c = line[i]
        if c == "[":
            i += 1  # [
            left = recurse()
            i += 1  # ,
            right = recurse()
            i += 1  # ]
            return Node(left, right, None)
        elif c.isdigit():
            i += 1
            return Node(None, None, int(c))

    return recurse()


def flatten(node: Node) -> List[Node]:
    if node.value is not None:
        return [node]
    return flatten(node.left) + flatten(node.right)


def explode(root: Node) -> bool:
    def recurse(node: Node, depth: int):
        if node.left and node.right:
            if depth == 4:
                flattened = flatten(root)
                i = flattened.index(node.left)
                if i - 1 >= 0:
                    flattened[i - 1].value += node.left.value
                if i + 2 < len(flattened):
                    flattened[i + 2].value += node.right.value
                node.left = None
                node.right = None
                node.value = 0
                return True
            else:
                return recurse(node.left, depth + 1) or recurse(node.right, depth + 1)
        return False

    return recurse(root, 0)


def split(root: Node) -> True:
    def recurse(node: Node) -> bool:
        if node.left and node.right:
            return recurse(node.left) or recurse(node.right)
        else:
            if node.value >= 10:
                half = node.value // 2
                node.left = Node(None, None, half)
                node.right = Node(None, None, node.value - half)
                node.value = None
                return True
            return False

    return recurse(root)


def magnitude(node: Node) -> int:
    if node.left and node.right:
        return 3 * magnitude(node.left) + 2 * magnitude(node.right)
    else:
        return node.value


lines = read_file("input.txt")[:-1]

nodes = [parse_line(line) for line in lines]


def take_sum(nodes):
    nodes = deepcopy(nodes)
    root = nodes[0]
    for node in nodes[1:]:
        root = Node(root, node, None)
        should_reduce = True
        while should_reduce:
            should_reduce = explode(root) or split(root)
    return root


print(f"Part 1: {magnitude(take_sum(nodes))}")

part_2 = max(magnitude(take_sum(permutation)) for permutation in permutations(nodes, 2))
print(f"Part 2: {part_2}")
