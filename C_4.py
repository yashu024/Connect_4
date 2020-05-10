import numpy as np
import pygame
import sys

ROW=6
COLUMN=6

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
                                             #Horizontal checking
    temp=column-1
    while (True):
        if temp>=0 and board[row][temp]==piece:
            same=same+1
            temp=temp-1
            if same==4:
                return True
        else:
            break


    same=0
    temp=row
    while(True):
        if temp>=0 and board[temp][column]==piece:
            same=same+1                              #vertical checking
            temp=temp-1
            if same==4:
                return True
        else:
            break

    temp1=row
    temp2=column
    same=0

    while(True):
        if temp1<ROW and temp2<COLUMN and board[temp1][temp2]==piece:
            same=same+1
            temp1=temp1+1
            temp2=temp2+1
            if same==4:
                return True
        else:
            break
                                                 #diagonal checking
    temp1=row-1
    temp2=column-1

    while (True):
        if temp1>=0 and temp2>=0 and board[temp1][temp2]==piece:
            same=same+1
            temp1=temp1-1
            temp2=temp2-1
            if same==4:
                return True
        else:
            break


    same=0
    temp1=row
    temp2=column

    while (True):
        if temp1>=0 and temp2<COLUMN and board[temp1][temp2]==piece:
            same=same+1
            temp1=temp1-1
            temp2=temp2+1
            if same==4:
                return True
        else:
            break
                                         #diagonal checking
    temp1=row+1
    temp2=column-1

    while(True):
        if temp1<ROW and temp2>=0 and board[temp1][temp2]==piece:
            same=same+1
            temp1=temp1+1
            temp2=temp2-1
            if same==4:
                return True
        else:
            break

    return False

board=create_board(ROW,COLUMN)
print(board)

game_over=False
turn = 0

while not game_over:

    #player 1 turn
    if turn==0:
        while(True):
          col=int(input("Player 1 enter valid column number (0-5):"))
          if is_valid_column(col):
            row=find_row(board,col)
            break

        drop_piece(board,row,col,1)
        if is_winning_move(board,row,col,1):
            print("Player 1 has won the game")
            game_over=True

    #player 2 turn
    if turn==1:
        while (True):
            col = int(input("Player 2 enter valid column number (0-5):"))
            if is_valid_column(col):
                row = find_row(board, col)
                break

        drop_piece(board, row, col, 2)
        if is_winning_move(board,row,col,2):
            print("Player 2 has won the game")
            game_over=True

    print_board(board)
    turn=turn+1
    turn=turn%2
