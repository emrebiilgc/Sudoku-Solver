import sys

# The limit is increased because the code stops working after a while due to too many attempts
sys.setrecursionlimit(10000)


def solve(board, row, col, output_file, step):

    # col means column
    if col == 9:    # When column 9 is reached, it signifies the end of the row
        if row == 8:    # If the column is the last column, the code is finished
            return True
        else:   # If not, the beginning of the next row is proceeded to
            col = 0
            row = row + 1

    if single_value_possible(board, row, col, output_file, step):

        # If only one number fits the empty cell, place it and restart from the beginning
        step = step + 1
        solve(board, 0, 0, output_file, step)
    else:
        solve(board, row, col + 1, output_file, step)


def single_value_possible(board, row, col, output_file, step):

    if board[row][col] != 0:
        return False

    possibilities = []
    # The numbers are tried one by one, and it is found out which ones can be placed in the empty cell
    for num in range(1, 10):

        in_row = False
        # True is returned if that number exists in another cell in that row
        for j in range(9):
            if num == board[row][j]:
                in_row = True
                break

        in_col = False
        # True is returned if that number exists in another cell in that column
        for i in range(9):
            if num == board[i][col]:
                in_col = True
                break

        start_row, start_col = 3 * (row // 3), 3 * (col // 3)   # Divide the sudoku board into 3x3 pieces
        in_box = False
        # True is returned if that number exists in another cell in that 3x3 piece
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if num == board[i][j]:
                    in_box = True
                    break
        # If one is correct, that number can't fill the cell, as it already exists at an intersection point
        if not (in_row or in_col or in_box):
            # If no true is returned, the number might appear in the cell and be added to the list
            possibilities.append(num)

    # If there is only one possibility, that number is added to that cell and the steps are printed
    if len(possibilities) == 1:
        board[row][col] = possibilities[0]
        print_board(board, output_file, row, col, possibilities[0], step)
        return True

    else:
        return False


def print_board(board, output_file, row, col, num, step):
    # Since both the row and the column are initiated from zero, they are each incremented by one during the printing
    output_file.write(f"Step {step} - {num} @ R{row + 1}C{col + 1}\n")
    output_file.write("------------------\n")
    zero_count = 0
    for row in board:   # The number of empty cells in the board is checked
        for col in row:
            if col == 0:
                zero_count += 1
    # If there are no empty cells, it indicates that the sudoku is completed; do not add a new line
    if zero_count == 0:
        for i in range(9):
            row_str = ""
            for j in range(9):
                row_str += str(board[i][j]) + " "
            output_file.write(row_str[:-1] + "\n")
        output_file.write("------------------")
        output_file.close()
    else:
        for i in range(9):
            row_str = ""
            for j in range(9):
                row_str += str(board[i][j]) + " "
            output_file.write(row_str[:-1] + "\n")
        output_file.write("------------------\n")


def matrix(input_line):
    return [int(number) for number in input_line.strip() if number.isdigit()]


def main():
    input_file_path = sys.argv[1]
    input_file = open(input_file_path, "r")
    board = [matrix(line) for line in input_file.readlines()]
    output_file_path = sys.argv[2]
    output_file = open(output_file_path, "w")
    output_file.write("------------------\n")
    step = 1
    solve(board, 0, 0, output_file, step)


if __name__ == "__main__":
    main()
