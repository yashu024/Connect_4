import numpy as np
import pygame
import sys

ROW=6
COLUMN=6
##BLUE=(0,0,255)

def create_board(row,column):
    board=np.zeros((row,column))
    return board

def is_valid_column(column):
    if column<COLUMN and column>=0:
        return True
    else:
        return False

def find_row(board,col):
    for r in range(ROW):
        if board[r][col]==0:
            return r

def drop_piece(board,row,column,piece):
    board[row][column]=piece

def print_board(board):
    print(np.flip(board,axis=0))

def is_winning_move(board,row,column,piece):
    same=0
    temp=column
    while (True):
         if temp<COLUMN and board[row][temp]==piece:
            same=same+1
            temp=temp+1
            if same==4:
                return True
         else:
           break

    temp = column - 1
    while (True):                                              #Horizontal checking
         if temp>=0 and board[row][temp]==piece:
            same=same+1
            temp=temp-1
            if same==4:
                return True
         else:
             break

    temp=row+1
    while (True):
         if temp<ROW and board[temp][column]==piece:
             same=same+1
             temp=temp+1
             if same==4:
                 return True                         #Vertical checking
         else:
             break

    temp=row-1
    while (True):
         if temp>=0 and board[temp][column]==piece:
             same=same+1
             temp=temp-1
             if same ==4:
                 return True
         else:
             break

    return False

board=create_board(ROW,COLUMN)
print(board)

game_over=False
turn = 0

##pygame.init()
SQUARESIZE=100
##width=int(COLUMN*SQUARESIZE)
##height=int(ROW*SQUARESIZE)

##size=(width,height)
##screen=pygame.display.set_mode(size)

while not game_over:
##  for event in pygame.event.get():
##      if event.type==pygame.QUIT:
##          sys.exit()

  #player 1 turn
    if turn==0:
        while(True):
          col=int(input("Player 1 enter valid column number (0-5):"))
          if is_valid_column(col):
            row=find_row(board,col)
            break

        drop_piece(board,row,col,1)
        if is_winning_move(board,row,col,1):
            print("Player 1 has win the game")
            game_over=True

    #player 2 turn
    if turn==1:
        while (True):
            col = int(input("Player 2 enter valid column number (0-5):"))
            if is_valid_column(col):
                row = find_row(board, col)
                break

        drop_piece(board, row, col, 2)
        if is_winning_move(board,row,col,1):
            print("Player 1 has win the game")
            game_over=True

    print_board(board)
    turn=turn+1
    turn=turn%2