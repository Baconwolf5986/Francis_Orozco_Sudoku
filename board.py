import pygame, copy
from sudoku_generator import SudokuGenerator

class cell:
    def __init__(self, value, row, col, screen):
        self.value = value
        self.row = row
        self.col = col
        self.screen = screen
        self.cell_size = 550 // 9
        self.sketched_value = 0

    def set_cell_value(self, value):
        self.value = value

    def set_sketched_value(self, value):
        self.sketched_value = value

    def draw(self, is_initial, is_selected):
        # Draw the cell, along with the value inside of it
        # If the value is 0 draw nothing inside the cell
        width = self.col * self.cell_size + 10
        height = self.row * self.cell_size + 10

        pygame.draw.rect(self.screen, (255,255,255), (width, height, self.cell_size, self.cell_size))
        font = pygame.font.Font(None, 40)
        if is_selected:
            pygame.draw.rect(self.screen, (0, 0, 255), (width, height, self.cell_size,self.cell_size), 3)
        if self.value != 0:
            if is_initial:
                text_color = (0,0,0)
            else:
                text_color = (100,100,200)
            val_text = font.render(str(self.value), True, text_color)
            text_rect = val_text.get_rect(center=(width + self.cell_size // 2, height + self.cell_size // 2))
            self.screen.blit(val_text, text_rect)

        if self.sketched_value != 0:
            font = pygame.font.Font(None, 20)
            val_text = font.render(str(self.sketched_value), True, (0, 0, 0))
            text_rect = val_text.get_rect(topleft=(width + 5, height + 5))
            self.screen.blit(val_text, text_rect)
class board:

    # Initialize the board object
    # The cell size will be 1/9 of the height (or width, it should be the same)
    # Difficulty will determine the number of cells removed
    # Create 3 boards
    # Board: The game board that will be updated by the user
    # Initial: The initial board that can be used to reset the game board
    # Solved: The board with no zero values, to check if the game board is solved

    def __init__(self, width, height, screen, difficulty):
        self.width = width
        self.height = height
        self.screen = screen
        self.difficulty = difficulty
        self.cell_size = self.height//9
        if difficulty == 'Easy':
            del_cells = 30
        elif  difficulty == 'Medium':
            del_cells = 40
        elif difficulty == 'Hard':
            del_cells = 50
        sudoku = SudokuGenerator(9, del_cells)
        sudoku.fill_values()
        solved = copy.deepcopy(sudoku.get_board()) # Solved board
        sudoku.remove_cells()
        board = sudoku.get_board()
        self.solved = solved
        self.board = board
        self.initial = copy.deepcopy(board)
        self.selected_cell = None
        self.cells = []
        for row in range(len(self.board)):
            row_cells = []
            for num in range(len(self.board[row])):
                cell_obj = cell(self.board[row][num], row, num, self.screen)
                row_cells.append(cell_obj)
            self.cells.append(row_cells)

    def draw(self):
        board_size = 550
        cell_size = board_size // 9
        board_x = 10
        board_y = 10

        # Use the initial board to draw the cells and values of the sudoku board
        for row in range(len(self.board)):
            for num in range(len(self.board[row])):
                board_cell = cell(self.board[row][num],row,num,self.screen)
                is_initial = self.initial[row][num] != 0
                is_selected = (row, num) == self.selected_cell
                board_cell.draw(is_initial, is_selected)

        # Draw the board gridlines using the cell size of the board
        for i in range(board_y, board_y + board_size, cell_size):
            pygame.draw.line(self.screen, (0, 0, 0), (board_x, i), (board_x+board_size-1, i))
        for j in range(board_x, board_x + board_size + 1, cell_size):
            pygame.draw.line(self.screen, (0, 0, 0), (j, board_y), (j, board_y + board_size-1))
        for i in range(0, board_size + 1, cell_size * 3):
            pygame.draw.line(self.screen, (0, 0, 0), (board_x, board_y + i), (board_x + board_size - 1, board_y + i), 3)
            pygame.draw.line(self.screen, (0, 0, 0), (board_x + i, board_y), (board_x + i, board_y + board_size - 1), 3)

    def click(self,x,y):
        # If a cell ((X,Y) coordinate tuple) was selected, return that tuple of the row/column
        # Instead of selecting the
        row = y // self.cell_size
        col = x // self.cell_size
        self.selected_cell = (row, col)
        return row, col

    def sketch(self, value):
        # Set the sketched value of the cell to be equal to the user input
        if self.selected_cell:
            row, col = self.selected_cell
            self.board[row][col].set_sketched_value(value)

    def place_number(self, value):
        # Sets the value of the current cell to be user entered value
        # called using enter key
        if self.selected_cell:
            row, col = self.selected_cell
            self.cells[row][col].set_cell_value(value)
            self.draw()

    def reset_to_original(self):
        # Reset all cells in the board to their original values (0 if cleared)
        # Use the self.initial to reset the board to its original state
        self.board = copy.deepcopy(self.initial)

    def is_full(self):
        # Checks if the board has any empty values (0)
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                if self.board[row][col] == 0:
                    return False
        return True

    def update_board(self, number):
        # Updates the self.board attribute when the user inputs a number for their board
        if self.selected_cell:
            row, col = self.selected_cell
            self.board[row][col] = number

    def find_empty(self):
        # Find an empty cell and return its row and column as a tuple (x,y)
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                if self.board[row][col]== 0:
                    return row, col
        return None

    def check_board(self):
        # Check if the solved board is the same as the current board
        if self.board == self.solved:
            return True
        return False