from util.read_file import read_file

lair_cols = [2, 4, 6, 8]
pod_types = ["A", "B", "C", "D"]
n_rows = 4
max_depth = len(lair_cols) ** n_rows

should_occupied_by = {(r + 1, c): pod for r in range(n_rows) for c, pod in zip(lair_cols, pod_types)}
temporary_positions = [(0, 0), (0, 1), (0, 3), (0, 5), (0, 7), (0, 9), (0, 10)]


def is_end_position(occupied_positions: dict):
    return all(occupied_positions.get(position) == pod for position, pod in should_occupied_by.items())


def can_move_to(from_position, to_position, occupied_positions):
    if to_position in occupied_positions:
        return False

    if from_position[0] < to_position[0]:
        current = from_position
        destination = to_position
    else:
        current = to_position
        destination = from_position

    step = 1 if current[1] < destination[1] else -1
    while current[1] != destination[1]:
        current = (current[0], current[1] + step)
        if current in occupied_positions:
            return False

    while current != destination:
        current = (current[0] + 1, current[1])
        if current != from_position and current in occupied_positions:
            return False
    return True


def energy_required_to_move(from_position, to_position, pod) -> int:
    steps_needed = abs(from_position[0] - to_position[0]) + abs(from_position[1] - to_position[1])
    return (10 ** (pod_types.index(pod))) * steps_needed


best_energy = 10 ** 20


def calculate_least_energy_required(current_energy, occupied_positions: dict, depth):
    global best_energy
    min_extra_energy_needed = 0

    for position, pod in occupied_positions.items():
        if should_occupied_by.get(position) != pod:
            should_be_at_col = [destination for destination, destination_pod in should_occupied_by.items() if
                                destination_pod == pod][0][1]
            min_steps_needed = position[0] + abs(should_be_at_col - position[1]) + 1
            min_extra_energy_needed += (10 ** (pod_types.index(pod))) * min_steps_needed

    if current_energy + min_extra_energy_needed >= best_energy:
        return

    if is_end_position(occupied_positions):
        best_energy = min(best_energy, current_energy)
        print(current_energy)
    else:

        for potentially_occupied_position, desired_pod in should_occupied_by.items():
            if potentially_occupied_position in occupied_positions:
                continue
            above_positions = [(r, potentially_occupied_position[1]) for r in
                               range(potentially_occupied_position[0] + 1, n_rows + 1)]
            if potentially_occupied_position[0] < n_rows and any(
                    occupied_positions.get(above) != desired_pod for above in above_positions):
                continue
            for temporary_position in sorted(temporary_positions,
                                             key=lambda p: abs(p[1] - potentially_occupied_position[1])):
                if occupied_positions.get(temporary_position) == desired_pod \
                        and can_move_to(temporary_position, potentially_occupied_position, occupied_positions):
                    energy = energy_required_to_move(temporary_position, potentially_occupied_position, desired_pod)

                    del occupied_positions[temporary_position]
                    occupied_positions[potentially_occupied_position] = desired_pod
                    calculate_least_energy_required(current_energy + energy, occupied_positions, depth + 1)
                    del occupied_positions[potentially_occupied_position]
                    occupied_positions[temporary_position] = desired_pod

        for position, desired_pod in should_occupied_by.items():
            pod = occupied_positions.get(position)
            above_positions = [(r, position[1]) for r in
                               range(position[0] + 1, n_rows + 1)]

            if pod and (pod != desired_pod or (position[0] < n_rows and any(
                    occupied_positions.get(above) != desired_pod for above in above_positions))):
                for temporary_position in temporary_positions:
                    if can_move_to(position, temporary_position, occupied_positions):
                        energy = energy_required_to_move(position, temporary_position, pod)

                        del occupied_positions[position]
                        occupied_positions[temporary_position] = pod
                        calculate_least_energy_required(current_energy + energy, occupied_positions, depth + 1)
                        del occupied_positions[temporary_position]
                        occupied_positions[position] = pod


def print_burrow(occupied_positions):
    print("#############")
    print("#", end="")
    print("".join([occupied_positions[(0, c)] if (0, c) in occupied_positions else "." for c in range(0, 11)]), end="")
    print("#")
    for r in range(1, n_rows + 1):
        print("###", end="")
        print(occupied_positions.get((r, 2)) if (r, 2) in occupied_positions else ".", end="")
        print("#", end="")
        print(occupied_positions.get((r, 4)) if (r, 4) in occupied_positions else ".", end="")
        print("#", end="")
        print(occupied_positions.get((r, 6)) if (r, 6) in occupied_positions else ".", end="")
        print("#", end="")
        print(occupied_positions.get((r, 8)) if (r, 8) in occupied_positions else ".", end="")
        print("###")


lines = read_file("input.txt")
occupied_positions = {}
occupied_positions[(1, 2)] = lines[2][3]
occupied_positions[(1, 4)] = lines[2][5]
occupied_positions[(1, 6)] = lines[2][7]
occupied_positions[(1, 8)] = lines[2][9]

occupied_positions[(4, 2)] = lines[3][3]
occupied_positions[(4, 4)] = lines[3][5]
occupied_positions[(4, 6)] = lines[3][7]
occupied_positions[(4, 8)] = lines[3][9]

occupied_positions[(2, 2)] = "D"
occupied_positions[(3, 2)] = "D"
occupied_positions[(2, 4)] = "C"
occupied_positions[(3, 4)] = "B"
occupied_positions[(2, 6)] = "B"
occupied_positions[(3, 6)] = "A"
occupied_positions[(2, 8)] = "A"
occupied_positions[(3, 8)] = "C"

print(calculate_least_energy_required(0, occupied_positions, 0))
