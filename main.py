import pygame, sys
from board import board


# Initialize Pygame Window
pygame.init()
pygame.display.set_caption('Sudoku')
screen = pygame.display.set_mode((900, 600))

# Initializ fonts for buttons and text
number_font = pygame.font.Font(None, 20)
game_over_font = pygame.font.Font(None, 50)
button_font = pygame.font.Font(None, 36)

# Sudoku background image
background_image = pygame.image.load('Sudoku.png')

# Dimensions for buttons/background fill
button_width = 150
button_height = 80
button_y = (1200 - button_width) // 2
easy_button = 100
medium_button = 300
hard_button = 500

# Initialize variables for the screen displays
# When the button text is TRUE, the button is clickable
game_board = None
difficulty_selected = False
game_over = False
buttons_clickable = {
    'easy': True,
    'medium': True,
    'hard': True,
    'reset': False,
    'restart': False,
    'exit': False
}

# Loop for game screen
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        screen.blit(background_image, (0, 0))

        # Create text for welcome screen
        # Buttons, followed by text in the buttons
        # Open first window when difficulty is not selected

        if not difficulty_selected:
            pygame.draw.rect(screen, (0, 0, 255), (100, 175, button_width + 250, button_height))
            pygame.draw.rect(screen, (255, 165, 0), (easy_button, button_y, button_width, button_height))
            pygame.draw.rect(screen, (255, 165, 0), (medium_button, button_y, button_width, button_height))
            pygame.draw.rect(screen, (255, 165, 0), (hard_button, button_y, button_width, button_height))
            welcome_text = game_over_font.render('Welcome to Sudoku!', True, (0,0,0))
            easy_button_text = button_font.render("Easy", True, (0,0,0))
            medium_button_text = button_font.render("Medium", True, (0, 0, 0))
            hard_button_text = button_font.render("Hard", True, (0, 0, 0))
            screen.blit(welcome_text, (120, 200))
            screen.blit(easy_button_text, (easy_button+40, button_y + 20))
            screen.blit(medium_button_text, (medium_button+20, button_y + 20))
            screen.blit(hard_button_text, (hard_button+40, button_y + 20))

            # If a button is clicked, create a board depending on difficulty
            # Turn the buttons off and advance to next screen

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                if buttons_clickable['easy'] and easy_button <= mx <= easy_button + button_width and button_y <= my <= button_y + button_height:
                    difficulty = 'Easy'
                    game_board = board(550, 550, screen, difficulty)
                    buttons_clickable['easy'] = False
                    buttons_clickable['medium'] = False
                    buttons_clickable['hard'] = False
                elif buttons_clickable['medium'] and medium_button <= mx <= medium_button + button_width and button_y <= my <= button_y + button_height:
                    difficulty = 'Medium'
                    game_board = board(550, 550, screen, difficulty)
                    buttons_clickable['easy'] = False
                    buttons_clickable['medium'] = False
                    buttons_clickable['hard'] = False
                elif buttons_clickable['hard'] and hard_button <= mx <= hard_button + button_width and button_y <= my <= button_y + button_height:
                    difficulty = 'Hard'
                    game_board = board(550, 550, screen, difficulty)
                    buttons_clickable['easy'] = False
                    buttons_clickable['medium'] = False
                    buttons_clickable['hard'] = False

        # When a board is created, display the board and new buttons
        # Hide all old old buttons

        if game_board is not None and not game_board.check_board():
            screen.fill((255,255,255))
            game_board.draw()
            reset_button_text = button_font.render("Reset", True, (0, 0, 0))
            restart_button_text = button_font.render("Restart", True, (0, 0, 0))
            exit_button_text = button_font.render("Exit", True, (0, 0, 0))
            pygame.draw.rect(screen, (255, 165, 0), (700, 200, button_width, button_height))
            pygame.draw.rect(screen, (255, 165, 0), (700, 300, button_width, button_height))
            pygame.draw.rect(screen, (255, 165, 0), (700, 400, button_width, button_height))
            screen.blit(reset_button_text, (710, 210))
            screen.blit(restart_button_text, (710, 310))
            screen.blit(exit_button_text, (710, 410))
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                if buttons_clickable['reset'] and 700 <= mx <= 700 + button_width and 200 <= my <= 200 + button_height:
                    game_board.reset_to_original()
                    game_board.draw()
                elif buttons_clickable['restart'] and 700 <= mx <= 700 + button_width and 300 <= my <= 300 + button_height:
                    game_board = None
                    difficulty_selected = False
                    buttons_clickable['easy'] = True
                    buttons_clickable['medium'] = True
                    buttons_clickable['hard'] = True
                elif buttons_clickable['restart'] and 700 <= mx <= 700 + button_width and 400 <= my <= 400 + button_height:
                    pygame.quit()
                else:
                    clicked_row, clicked_col = game_board.click(mx, my)
                    if clicked_row is not None and clicked_col is not None:
                        if 0 <= clicked_row < len(game_board.initial) and 0 <= clicked_col < len(game_board.initial):
                            if game_board.initial[clicked_row][clicked_col] == 0:
                                game_board.selected_cell = (clicked_row, clicked_col)
                            else:
                                game_board.selected_cell = None

            # Interpret key inputs
            # If a cell is selected and a number is pressed add the number
            # If an arrow key is pressed

            if event.type == pygame.KEYDOWN:
                if game_board.selected_cell:
                    # 1-9 keyboard input
                    if pygame.K_1 <= event.key <= pygame.K_9:
                        number_input = event.key - pygame.K_0
                        game_board.update_board(number_input)
                        game_board.draw()

                    # Arrow key input move to the cells, check if the cell is an initial cell,
                    # or if it's within the range.

                    if event.key == pygame.K_LEFT:
                        if game_board.selected_cell[1] > 0:
                            if game_board.initial[game_board.selected_cell[0]][game_board.selected_cell[1]-1] == 0:
                                game_board.selected_cell = (game_board.selected_cell[0], game_board.selected_cell[1]- 1)
                            else:
                                game_board.selected_cell = game_board.find_empty()
                        else:
                            game_board.selected_cell = game_board.find_empty()
                    elif event.key == pygame.K_RIGHT:
                        if game_board.selected_cell[1] < 8:
                            if game_board.initial[game_board.selected_cell[0]][game_board.selected_cell[1]+1] == 0:
                                game_board.selected_cell = (game_board.selected_cell[0], game_board.selected_cell[1] + 1)
                            else:
                                game_board.selected_cell = game_board.find_empty()
                        else:
                            game_board.selected_cell = game_board.find_empty()
                    elif event.key == pygame.K_UP:
                        if game_board.selected_cell[0] > 0:
                            if game_board.initial[game_board.selected_cell[0]-1][game_board.selected_cell[1]] == 0:
                                game_board.selected_cell = (game_board.selected_cell[0] - 1, game_board.selected_cell[1])
                            else:
                                game_board.selected_cell = game_board.find_empty()
                        else:
                            game_board.selected_cell = game_board.find_empty()
                    elif event.key == pygame.K_DOWN:
                        if game_board.selected_cell[0] < 8:
                            if game_board.initial[game_board.selected_cell[0]+1][game_board.selected_cell[1]] == 0:
                                game_board.selected_cell = (game_board.selected_cell[0] + 1, game_board.selected_cell[1])
                            else:
                                game_board.selected_cell = game_board.find_empty()
                        else:
                            game_board.selected_cell = game_board.find_empty()

            # Check if the board is full, if it is, and it's not correct show GAME OVER
            # If the board is full and correct show YOU WIN

            if game_board is not None and game_board.is_full() and not game_board.check_board():
                game_over = True
                game_result = 'GAME OVER'
            if game_board is not None and game_board.is_full() and game_board.check_board():
                game_over = True
                game_result = 'YOU WIN!'

        if not game_over:
            pass
        else:
            screen.blit(background_image, (0, 0))
            welcome_text = game_over_font.render(game_result, True, (0,50,255))
            screen.blit(welcome_text, (325, 200))

            exit_button_rect = pygame.draw.rect(screen, (255, 165, 0), (350, 500, button_width, button_height))
            exit_button_text = button_font.render("Exit", True, (0, 0, 0))
            screen.blit(exit_button_text, (375, 520))

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                if 350 <= mx <= 350 + button_width and 500 <= my <= 500 + button_height:
                    pygame.quit()
                    sys.exit()

    pygame.display.update()