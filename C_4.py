import numpy as np
import pygame
import sys
import math

ROW=6
COLUMN=6
BLUE=(0,0,200)
BLACK=(0,0,0)
RED=(255,0,0)
YELLOW=(255,255,0)

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

def draw_board(board):
    for c in range(COLUMN):
        for r in range(ROW):
            pygame.draw.rect(screen,BLUE,(c*SQUARESIZE,r*SQUARESIZE+SQUARESIZE,SQUARESIZE,SQUARESIZE))
            pygame.draw.circle(screen,BLACK,(int(c*SQUARESIZE+SQUARESIZE/2),int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)),RADIUS)

    for c in range(COLUMN):
        for r in range(ROW):
            if board[r][c]==1:
                pygame.draw.circle(screen, RED, (int(c * SQUARESIZE + SQUARESIZE / 2), height-int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            elif board[r][c]==2:
                pygame.draw.circle(screen, YELLOW, (int(c * SQUARESIZE + SQUARESIZE / 2), height-int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    pygame.display.update()

board=create_board(ROW,COLUMN)
print(board)

game_over=False
turn = 0

pygame.init()

SQUARESIZE=100

width=COLUMN*100
height=(ROW+1)*100

size=(width,height)
RADIUS=int(SQUARESIZE/2-5)

screen=pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

myfont=pygame.font.SysFont("monospace",75)


while not game_over:

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            sys.exit()

        if event.type==pygame.MOUSEMOTION:
            pygame.draw.rect(screen,BLACK,(0,0,width,SQUARESIZE))
            posx=event.pos[0]
            if turn==0:
                pygame.draw.circle(screen,RED,(posx,int(SQUARESIZE/2)),RADIUS)
            else:
                pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE / 2)), RADIUS)
            pygame.display.update()

        if event.type==pygame.MOUSEBUTTONDOWN:
                #player 1 turn
                if turn==0:
                    while(True):
                        posx=event.pos[0]
                        col=int(math.floor(posx/100))
                        if is_valid_column(col):
                            row=find_row(board,col)
                            break
        
                    drop_piece(board,row,col,1)
                    if is_winning_move(board,row,col,1):
                        print("Player 1 has won the game")
                        label = myfont.render("Player 1 wins !!", 1, RED)
                        screen.blit(label, (40, 10))
                        game_over=True
        
                #player 2 turn
                if turn==1:
                    while (True):
                        posx = event.pos[0]
                        col = int(math.floor(posx / 100))
                        if is_valid_column(col):
                            row = find_row(board, col)
                            break
        
                    drop_piece(board, row, col, 2)
                    if is_winning_move(board,row,col,2):
                        label=myfont.render("Player 2 wins !!",1,RED)
                        screen.blit(label,(40,10))
                        game_over=True
        
                print_board(board)
                draw_board(board)
                turn=turn+1
                turn=turn%2

                if game_over:
                    pygame.time.wait(3000)
