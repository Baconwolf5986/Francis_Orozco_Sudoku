# COP3502 Project 4
# Sudoku Generator Class

import random
class SudokuGenerator:

    def __init__(self, row_length, removed_cells):
        self.row_length = row_length
        self.removed_cells = removed_cells
        board = []
        for i in range(row_length):
            row = [0] * row_length
            board.append(row)
        self.board = board
        self.box_length = 3

    def get_board(self):
        # Return the board attribute
        return self.board

    def print_board(self):
        #  Print the board
        for row in self.board:
            row_str = ''
            for num in row:
                num_str = str(num)
                row_str += num_str + ' '
            print(row_str)

    def valid_in_row(self, row, num):
        # Check if num is already in the row
        # If not the row, return True
        if num not in self.board[row]:
            return True
        return False

    def valid_in_col(self, col, num):
        # Check if num is already in the column
        # If not return, True
        for row in range(self.row_length):
            if self.board[row][col] == num:
                return False
        return True

    def valid_in_box(self, row_start, col_start, num):
        # Check if num is already in the box
        # Go through every value in a 3x3 box, if it is Return False
        for row in range(3):
            for column in range(3):
                if self.board[row_start+row][col_start+column] == num:
                    return False
        return True

    def is_valid(self, row, col, num):
        # Check if the number is valid
        # Check if it is valid in the row and the column
        # Box_row and box_col are set to check which th
        box_row = row - row % 3
        box_col = col - col % 3
        if (self.valid_in_row(row, num) and self.valid_in_col(col,num) and self.valid_in_box(box_row, box_col, num)):
            return True
        return False

    def fill_box(self, row_start, col_start):
        # Fill each 3x3 square on the board
        # Create an array containing one of each digit 1-9
        # Randomly shuffle these numbers, and place them in the box
        numbers = [1,2,3,4,5,6,7,8,9]
        random.shuffle(numbers)
        num = 0
        for row in range(3):
            for column in range(3):
                self.board[row_start+row][col_start+column] = numbers[num]
                num += 1

    def fill_diagonal(self):
        # Use the fill box function to fill each 3x3 box along the diagonal of the board.
        # Go along the board as though it were a 3x3 box
        for i in range(0, 9, 3):
            self.fill_box(i,i)

    def fill_remaining(self, row, col):
        if (col >= self.row_length and row < self.row_length - 1):
            row += 1
            col = 0
        if row >= self.row_length and col >= self.row_length:
            return True
        if row < self.box_length:
            if col < self.box_length:
                col = self.box_length
        elif row < self.row_length - self.box_length:
            if col == int(row // self.box_length * self.box_length):
                col += self.box_length
        else:
            if col == self.row_length - self.box_length:
                row += 1
                col = 0
                if row >= self.row_length:
                    return True
        for num in range(1, self.row_length + 1):
            if self.is_valid(row, col, num):
                self.board[row][col] = num
                if self.fill_remaining(row, col + 1):
                    return True
                self.board[row][col] = 0
        return False

    def fill_values(self):
        self.fill_diagonal()
        self.fill_remaining(0, self.box_length)

    def remove_cells(self):
        # Delete a certain number of cells depending on the 'removed_cells' attribute given
        # Randomly choose a row and column and set that cell to 0
        # Repeat 'removed_cells' number of times
        del_cells = self.removed_cells
        while del_cells > 0:
            row = random.randint(0,8)
            column = random.randint(0,8)
            if self.board[row][column] != 0:
                self.board[row][column] = 0
                del_cells -= 1

def generate_sudoku(size, removed):
    sudoku = SudokuGenerator(size, removed)
    sudoku.fill_values()
    board = sudoku.get_board()
    sudoku.remove_cells()
    board = sudoku.get_board()
    sudoku.print_board()
    return board

def main():
    generate_sudoku(9, 30)

if __name__ == '__main__':
    main()