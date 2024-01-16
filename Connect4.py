import numpy as np
import pygame
import sys

# Function to create a 2D array of 6 x 7 board
def createBoard():
    board = np.zeros((6, 7))
    return board

# Function to set the specific index to the number of the turn
def dropCoin(board, row, col, turn):
    board[row][col] = turn

# Function to check whether the columns has been filled to the top or not. This Function checks for the bottom most row, since the code is designed in a way that the board is reflected on x-axis.
def isValidLocation(board, col):
    return board[5][col] == 0

# Fuction to return the last empty row in the selected column where the coin can be dropped
def getNextOpenRow(board, col):
    for r in range(6):
        if board[r][col] == 0:
            return r

# Function to check all possibilities of winning
def winningMove(board, turn):
    # Check the horizontal line if formed
    # 3 is subtracted because left two or right two columns cannot have 4 consecutive coins on their extreme ends
    for c in range(7 - 3):
        for r in range(6):
            if board[r][c] == turn and board[r][c+1] == turn and board[r][c+2] == turn and board[r][c+3] == turn:
                return True

    # Check the vertical line if formed
    # 3 is subtracted because upper two or bottom two rows cannot have 4 consecutive coins on their extreme ends
    for c in range(7):
        for r in range(6 - 3):
            if board[r][c] == turn and board[r+1][c] == turn and board[r+2][c] == turn and board[r+3][c] == turn:
                return True

    # Check the positive diagonal
    # Both rows and columns cannot have 4 consecutive coins on their extreme ends so 3 is subtracted from both
    for c in range(7 - 3):
        for r in range(6 - 3):
            if board[r][c] == turn and board[r+1][c+1] == turn and board[r+2][c+2] == turn and board[r+3][c+3] == turn:
                return True

    # Check negative diagonal
    for c in range(7 - 3):
        for r in range(3, 6):
            if board[r][c] == turn and board[r-1][c+1] == turn and board[r-2][c+2] == turn and board[r-3][c+3] == turn:
                return True

# Function to draw GUI Board
def draw_board(board):
    # Draw initial board setup
    for c in range(7):
        for r in range(6):
            pygame.draw.rect(screen, 'blue', (c * 100, r * 100 + 100, 100, 100))
            pygame.draw.circle(screen, 'black', (c * 100 + 100//2, r * 100 + 100 + 100//2), 100//2 - 5)

    # Draws the red or yellow circle based on their turns
    for c in range(7):
        for r in range(6):
            if board[r][c] == 1:
                pygame.draw.circle(screen, 'red', (c * 100 + 100//2, height - (r * 100 + 100//2)), 100//2 - 5)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, 'yellow', (c * 100 + 100//2, height - (r * 100 + 100//2)), 100//2 - 5)

    pygame.display.update()

board = createBoard()

turn = 1
game_over = False

pygame.init()
pygame.display.set_caption("Connect 4")
pygame.display.set_icon(pygame.image.load('connect-four-1.png'))

CircleSize = 100
width = CircleSize * 7
height = CircleSize * (6 + 1)

screen = pygame.display.set_mode((width, height))
draw_board(board)

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, 'black', (0, 0, width, CircleSize))
            posx = event.pos[0]
            if turn == 1:
                pygame.draw.circle(screen, 'red', (posx, CircleSize // 2), CircleSize // 2 - 5)
            elif turn == 2:
                pygame.draw.circle(screen, 'yellow', (posx, CircleSize // 2), CircleSize // 2 - 5)
        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            # continue
            if turn == 1:
                col = event.pos[0]//100

                if isValidLocation(board, col):
                    row = getNextOpenRow(board, col)
                    dropCoin(board, row, col, turn)

                    if winningMove(board, turn):
                        print(f"Player 1 wins!!!")
                        game_over = True

                turn = 2

            else:
                col = event.pos[0]//100

                if isValidLocation(board, col):
                    row = getNextOpenRow(board, col)
                    dropCoin(board, row, col, turn)

                    if winningMove(board, turn):
                        print(f"Player 2 wins!!!")
                        game_over = True

                turn = 1

            draw_board(board)

            if game_over:
                pygame.time.wait(3000)
