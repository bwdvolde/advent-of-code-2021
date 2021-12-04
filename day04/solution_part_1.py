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

    winning_board = None
    draw_i = 0
    while not winning_board:
        draw = draws[draw_i]

        for board in boards:
            for r in range(len(board)):
                for c in range(len(board[r])):
                    if board[r][c] == draw:
                        board[r][c] = None

        for board in boards:
            for row in board:
                if all(number is None for number in row):
                    winning_board = board
                    break

            for c in range(len(board[0])):
                if all(board[r][c] is None for r in range(len(board))):
                    winning_board = board
                    break

        draw_i += 1

    total_unmarked = 0
    for r in range(len(winning_board)):
        for c in range(len(winning_board[r])):
            total_unmarked += winning_board[r][c] if winning_board[r][c] is not None else 0

    print(f"Part 1: {total_unmarked * draws[draw_i - 1]}")
