import random
import numpy as np
import pygame
import sys
import math

ROW = 6
COLUMN = 7
BLUE = (0, 0, 200)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
PLAYER = 0
AI = 1
Player_piece = 1
AI_piece = 2
Window_length = 4
EMPYT = 0


def create_board(row, column):
    board = np.zeros((row, column))
    return board


def is_valid_column(column):
    if column < COLUMN and column >= 0:
        return True
    else:
        return False


def find_row(board, col):
    flag = 0
    for r in range(ROW):
        if board[r][col] == 0:
            flag = 1
            return r
    if flag == 0:
        print("Fill valid place !!")
        return -1


def drop_piece(board, row, column, piece):
    board[row][column] = piece


def print_board(board):
    print(np.flip(board, axis=0))


def is_winning_move(board, row, column, piece):
    same = 0
    temp = column

    while (True):
        if temp < COLUMN and board[row][temp] == piece:
            same = same + 1
            temp = temp + 1
            if same == 4:
                return True
        else:
            break
            # Horizontal checking
    temp = column - 1
    while (True):
        if temp >= 0 and board[row][temp] == piece:
            same = same + 1
            temp = temp - 1
            if same == 4:
                return True
        else:
            break

    same = 0
    temp = row
    while (True):
        if temp >= 0 and board[temp][column] == piece:
            same = same + 1  # vertical checking
            temp = temp - 1
            if same == 4:
                return True
        else:
            break

    temp1 = row
    temp2 = column
    same = 0

    while (True):
        if temp1 < ROW and temp2 < COLUMN and board[temp1][temp2] == piece:
            same = same + 1
            temp1 = temp1 + 1
            temp2 = temp2 + 1
            if same == 4:
                return True
        else:
            break
            # diagonal checking
    temp1 = row - 1
    temp2 = column - 1

    while (True):
        if temp1 >= 0 and temp2 >= 0 and board[temp1][temp2] == piece:
            same = same + 1
            temp1 = temp1 - 1
            temp2 = temp2 - 1
            if same == 4:
                return True
        else:
            break

    same = 0
    temp1 = row
    temp2 = column

    while (True):
        if temp1 >= 0 and temp2 < COLUMN and board[temp1][temp2] == piece:
            same = same + 1
            temp1 = temp1 - 1
            temp2 = temp2 + 1
            if same == 4:
                return True
        else:
            break
            # diagonal checking
    temp1 = row + 1
    temp2 = column - 1

    while (True):
        if temp1 < ROW and temp2 >= 0 and board[temp1][temp2] == piece:
            same = same + 1
            temp1 = temp1 + 1
            temp2 = temp2 - 1
            if same == 4:
                return True
        else:
            break

    return False


def draw_board(board):
    for c in range(COLUMN):
        for r in range(ROW):
            pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, r *
                                            SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (
                int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)

    for c in range(COLUMN):
        for r in range(ROW):
            if board[r][c] == Player_piece:
                pygame.draw.circle(screen, RED, (
                    int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            elif board[r][c] == AI_piece:
                pygame.draw.circle(screen, YELLOW, (
                    int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    pygame.display.update()


def score_position(board, piece):
    score = 0
    # Score Center_col
    center_array = [int(i) for i in list(board[:, COLUMN//2])]
    center_count = center_array.count(piece)
    score += center_count*6

    # Score Horizontal
    for r in range(ROW):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(COLUMN-3):
            window = row_array[c:c+Window_length]
            score += evaluate_window(window, piece)

    # Score Vertical
    for c in range(COLUMN):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(ROW-3):
            window = col_array[r:r+Window_length]
            score += evaluate_window(window, piece)

    # +ve slopped Diagonal Score
    for r in range(ROW-3):
        for c in range(COLUMN-3):
            window = [board[r+i][c+i] for i in range(Window_length)]
            score += evaluate_window(window, piece)

     # -ve slopped Diagonal score
    for r in range(ROW-3):
        for c in range(COLUMN-3):
            window = [board[r+3-i][c+i] for i in range(Window_length)]
            score += evaluate_window(window, piece)
    return score


def get_valid_locations(board):
    valid_locations = []
    for c in range(COLUMN):
        if find_row(board, c) >= 0:
            valid_locations.append(c)
    return valid_locations


def pick_best_col(board, piece):
    valid_location = get_valid_locations(board)
    best_score = -10000
    best_col = random.choice(valid_location)
    for col in valid_location:
        row = find_row(board, col)
        temp_board = board.copy()
        drop_piece(temp_board, row, col, piece)
        score = score_position(temp_board, piece)
        if score > best_score:
            best_score = score
            best_col = col
    return best_col


def evaluate_window(window, piece):
    score = 0
    opp_piece = Player_piece
    if opp_piece == piece:
        opp_piece = AI_piece

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(EMPYT) == 1:
        score += 10
    elif window.count(piece) == 2 and window.count(EMPYT) == 2:
        score += 5

    if window.count(opp_piece) == 3 and window.count(EMPYT) == 1:
        score -= 80
    return score


def is_terminal_node(board):
    for r in range(ROW):
        for c in range(COLUMN):
            if is_winning_move(board, r, c, Player_piece):
                return True

    for r in range(ROW):
        for c in range(COLUMN):
            if is_winning_move(board, r, c, AI_piece):
                return True

    if len(get_valid_locations(board)) == 0:
        return True
    
    return False

    


def minmax(board, depth, alpha, beta, maximizing_player):
    valid_locations = get_valid_locations(board)
    if depth == 0 or is_terminal_node(board):
        if is_terminal_node(board):
            for r in range(ROW):
                for c in range(COLUMN):
                    if is_winning_move(board, r, c, AI_piece):
                        return (None, 1000000000)
            for r in range(ROW):
                for c in range(COLUMN):
                    if is_winning_move(board, r, c, Player_piece):
                        return (None, -1000000000)

            return (None, 0)  # No valid moves left

        else:  # Depth is zero
            return (None, score_position(board, AI_piece))

    if maximizing_player:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = find_row(board, col)
            temp_board = board.copy()
            drop_piece(temp_board, row, col, AI_piece)
            new_score = minmax(temp_board, depth-1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return (column, value)

    else:
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = find_row(board, col)
            temp_board = board.copy()
            drop_piece(temp_board, row, col, Player_piece)
            new_score = minmax(temp_board, depth-1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return (column, value)



board = create_board(ROW, COLUMN)
print(board)

game_over = False
turn = random.randint(PLAYER, AI)

pygame.init()

SQUARESIZE = 100

width = COLUMN * 100
height = (ROW + 1) * 100

size = (width, height)
RADIUS = int(SQUARESIZE / 2 - 5)

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

myfont = pygame.font.SysFont("monospace", 50)

total = 0
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            posx = event.pos[0]
            if turn == 0:
                pygame.draw.circle(
                    screen, RED, (posx, int(SQUARESIZE / 2)), RADIUS)
            # else:
            #     pygame.draw.circle(
            #         screen, YELLOW, (posx, int(SQUARESIZE / 2)), RADIUS)
            pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            # player 1 turn
            row = 0
            if turn == PLAYER:
                while (True):
                    posx = event.pos[0]
                    col = int(math.floor(posx / 100))
                    if is_valid_column(col):
                        row = find_row(board, col)
                        break

                if row >= 0:
                    total = total+1
                    drop_piece(board, row, col, Player_piece)
                    if is_winning_move(board, row, col, Player_piece):
                        print("Player 1 has won the game")
                        label = myfont.render("Player 1 wins !!", 1, RED)
                        screen.blit(label, (40, 10))
                        game_over = True

                    turn = turn+1
                    turn = turn % 2
                    print_board(board)
                    draw_board(board)
                else:
                    label = myfont.render("Fill valid place !!", 1, RED)
                    screen.blit(label, (40, 10))

    # player 2 turn
    if turn == AI and game_over != True:
        while (True):
            #col = random.randint(0,COLUMN-1)
            #col = pick_best_col(board, AI_piece)
            col, minmax_score = minmax(board, 4, -math.inf, math.inf, True)
            row = find_row(board, col)
            print("column", col)
            if row >= 0:
                total = total + 1
                drop_piece(board, row, col, AI_piece)
                if is_winning_move(board, row, col, AI_piece):
                    print("Player 2 has won the game")
                    label = myfont.render("Player 2 wins !!", 1, YELLOW)
                    screen.blit(label, (40, 10))
                    game_over = True

                turn = turn+1
                turn = turn % 2
                pygame.time.wait(500)
                print_board(board)
                draw_board(board)
                break

    if total == ROW*COLUMN:
        game_over = True
        label = myfont.render("Match tie !!", 1, RED)
        screen.blit(label, (40, 10))

    if game_over:
        pygame.time.wait(3000)
