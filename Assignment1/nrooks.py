#!/usr/bin/env python
# nrooks.py : Solve the N-Rooks problem!
# The N-rooks problem is: Given an empty NxN chessboard, place N rooks on the board so that no rooks
# can take any other, i.e. such that no two rooks share the same row or column.
# D. Crandall, 2016
# Updated by Zehua Zhang, 2017
# Updated by Aravind Bharatha, 2017
# Updated the following:
# 1) Changed the add_piece method a bit so that its readable for me.
# 2) Added the successors2 function which optimized the existing successor function by adding so checks before placing the pawn in the spot.
# 3) Changed the solve function to use DFS by popping the last element of the fringe
# 4) Added and commented the 2nd solve function which uses BFS b always popping the first element that enters the fringe.


import sys

# Count # of pieces in given row
def count_on_row(board, row):
    return sum( board[row] ) 

# Count # of pieces in given column
def count_on_col(board, col):
    return sum( [ row[col] for row in board ] ) 

# Count total # of pieces on board
def count_pieces(board):
    return sum([ sum(row) for row in board ] )

# Return a string with the board rendered in a human-friendly format
def printable_board(board):
    return "\n".join([ " ".join([ "R" if col else "_" for col in row ]) for row in board])

# Add a piece to the board at the given position, and return a new board (doesn't change original)
def add_piece(board, row, col):
    temp = []
    temp =  board[0:row] + [board[row][0:col] + [1,] + board[row][col+1:]] + board[row+1:]
    return temp

# Get list of successors of given board state
# This is the default successor function which is given which relies on brute force tecgnique to find the solution
def successors(board):
    return [ add_piece(board, r, c) for r in range(0, N) for c in range(0,N) ]

# Get list of successors of given board state
# This function optimized the brute force method as it first check if there is any pawn already placed in the row or column before adding it.
def successors2(board):
    list = []
    for r in range(0, N):
        for c in range(0,N):
            if count_on_row(board, r) < 1 and count_on_col(board, c) < 1:
                list.append(add_piece(board,r,c))
    return list

# check if board is a goal state
def is_goal(board):
    return count_pieces(board) == N and \
        all( [ count_on_row(board, r) <= 1 for r in range(0, N) ] ) and \
        all( [ count_on_col(board, c) <= 1 for c in range(0, N) ] )


# Solve n-rooks!
#Changed the fringe to use DFS instead of BFS by changing the fring.pop(0) to fringe.pop()
def solve(initial_board):
    fringe = [initial_board]
    while len(fringe) > 0:
        for s in successors2( fringe.pop() ):
            #print printable_board(s) + "\n hi";
            if is_goal(s):
                return(s)
            fringe.append(s)
    return False
'''
# This code uses the BFS we have to just change the fringe so that it 
# always pops the first element that is zeroth element to convert it into BFS 
#Changed the fringe to use BFS instead of DFS by changing the fring.pop() to fringe.pop(0)
def solve(initial_board):
    fringe = [initial_board]
    while len(fringe) > 0:
        for s in successors2( fringe.pop(0) ):
            #print printable_board(s) + "\n hi";
            if is_goal(s):
                return(s)
            fringe.append(s)
    return False
'''

# This is N, the size of the board. It is passed through command line arguments.
N = int(sys.argv[1])

# The board is stored as a list-of-lists. Each inner list is a row of the board.
# A zero in a given square indicates no piece, and a 1 indicates a piece.
initial_board = [[0]*N]*N
print ("Starting from initial board:\n" + printable_board(initial_board) + "\n\nLooking for solution...\n")
solution = solve(initial_board)
print (printable_board(solution) if solution else "Sorry, no solution found. :(")


