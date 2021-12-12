from collections import defaultdict

from util.read_file import read_file

lines = read_file("input.txt")[:-1]

neighbors = defaultdict(list)
for line in lines:
    a, b = line.split("-")
    neighbors[a].append(b)
    neighbors[b].append(a)


def calculate_paths(current_node, remaining_nodes):
    paths = []

    if current_node == "end":
        return [("end",)]

    if current_node.islower():
        remaining_nodes.remove(current_node)

    for neighbor in neighbors[current_node]:
        if neighbor in remaining_nodes:
            for sub_path in calculate_paths(neighbor, remaining_nodes):
                paths.append((current_node,) + sub_path)

    if current_node.islower():
        remaining_nodes.add(current_node)

    return paths


nodes = set(neighbors.keys())
possible_paths = calculate_paths("start", nodes)

answer = len(possible_paths)
print(f"Part 1: {answer}")
