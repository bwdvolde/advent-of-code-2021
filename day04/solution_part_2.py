from util.read_file import read_file


def parse_file():
    lines = read_file("input.txt")
    iterator = iter(lines)
    draws = [int(x) for x in next(iterator).split(",")]
    boards = []

    next(iterator)
    while True:
        try:
            board = []
            while line := next(iterator):
                board.append([int(x) for x in line.split()])
            boards.append(board)
        except StopIteration:
            break

    return draws, boards


if __name__ == '__main__':
    draws, boards = parse_file()

    worst_board = None
    draw_i = 0
    remaining_boards = boards
    while not worst_board:
        next_boards = []
        draw = draws[draw_i]

        for board in remaining_boards:
            for r in range(len(board)):
                for c in range(len(board[r])):
                    if board[r][c] == draw:
                        board[r][c] = None

        for board in remaining_boards:
            won = False
            for row in board:
                if all(number is None for number in row):
                    won = True

            for c in range(len(board[0])):
                if all(board[r][c] is None for r in range(len(board))):
                    won = True

            if not won:
                next_boards.append(board)
            elif len(remaining_boards) == 1:
                worst_board = board

        remaining_boards = next_boards
        draw_i += 1

    total_unmarked = 0
    for r in range(len(worst_board)):
        for c in range(len(worst_board[r])):
            total_unmarked += worst_board[r][c] if worst_board[r][c] is not None else 0

    print(total_unmarked, draws[draw_i - 1])
    print(f"Part 2: {total_unmarked * draws[draw_i - 1]}")
