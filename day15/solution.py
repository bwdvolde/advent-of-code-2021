from util.read_file import read_file
import heapq

lines = read_file("input.txt")[:-1]


def calculate_lowest_risk(grid):
    target = len(grid) - 1, len(grid[0]) - 1
    distances = {(r, c): 99999999 for r in range(len(grid)) for c in range(len(grid[r]))}
    distances[(0, 0)] = 0
    seen = set()

    def unfrozen_neighbors(r, c):
        possible_coordinates = [
            (r - 1, c),
            (r + 1, c),
            (r, c - 1),
            (r, c + 1),
        ]
        return [(_r, _c) for (_r, _c) in possible_coordinates if
                0 <= _r < len(grid) and 0 <= _c < len(grid[0]) and (_r, _c) not in seen]

    queue = [(0, (0, 0))]
    while queue:
        distance, current_coordinate = heapq.heappop(queue)
        if current_coordinate == target:
            return distance
        if current_coordinate not in seen:
            seen.add(current_coordinate)
            neighbors = unfrozen_neighbors(*current_coordinate)
            for neighbor in neighbors:
                distance_to_neighbor = distance + grid[neighbor[0]][neighbor[1]]
                if distance_to_neighbor < distances[neighbor]:
                    distances[neighbor] = distance_to_neighbor
                    heapq.heappush(queue, (distance_to_neighbor, neighbor))


tiny_grid = [[int(x) for x in line] for line in lines]
part_1 = calculate_lowest_risk(tiny_grid)
print(f"Part 1: {part_1}")

grid_n_rows = len(tiny_grid)
grid_n_cols = len(tiny_grid[0])
large_grid = [[0 for _ in range(grid_n_cols * 5)] for _ in range(grid_n_rows * 5)]
for r in range(len(large_grid)):
    for c in range(len(large_grid[0])):
        large_grid[r][c] = tiny_grid[r % grid_n_rows][c % grid_n_cols] + r // grid_n_rows + c // grid_n_cols
        if large_grid[r][c] > 9:
            large_grid[r][c] = (large_grid[r][c]) % 9
part_2 = calculate_lowest_risk(large_grid)

print(f"Part 2: {part_2}")
