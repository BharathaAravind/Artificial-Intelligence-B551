#!/usr/bin/env python
# nrooks.py : Solve the N-Rooks problem!
# D. Crandall, 2016
# Updated by Zehua Zhang, 2017
#
# Updated by Aravind Bharatha, 2017
# Updated/ Added the following function:
# 1) Re-used parts of the code and made changes in printable_board function, successor2 function and added two functions
# to count diagonals (count_on_back_diag and count_on_fwd_diag)
#
# The N-rooks problem is: Given an empty NxN chessboard, place N rooks on the board so that no rooks
# can take any other, i.e. such that no two rooks share the same row or column.
# The N-queens problem is: Given an empty NxN board we have to place N Queens on the board so that no queen cancels out the other queen.
# ie., if we place one queen on any position we can't place other queens in the same row, column or diagonal

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
def printable_board(board, prob):
    s = ""
    pawn = ""
    if(prob == "nrook"):
        pawn = "R"
    else:
        pawn = "Q"

    for row in range(0, N):
        list = []
        for col in range(0,N):
            if row == x - 1 and col == y - 1:
                list.append("X")
            elif board[row][col] == 1:
                list.append(pawn)
            else:
                list.append("_")
        s = s + " ".join(list) + "\n"
    return s


# Add a piece to the board at the given position, and return a new board (doesn't change original)
def add_piece(board, row, col):
    return board[0:row] + [board[row][0:col] + [1,] + board[row][col+1:]] + board[row+1:]

# Get list of successors of given board state
def successors(board):
    return [ add_piece(board, r, c) for r in range(0, N) for c in range(0,N) ]

# modified successor function which doesnt add pawn if the row or column already has a pawn
def successors2(board):
    list = []
    if prob == "nrook":
        for r in range(0, N):
            for c in range(0,N):
                if (r !=(x-1) or c !=(y-1)):
                    if count_on_row(board, r) < 1 and count_on_col(board, c) < 1:
                        list.append(add_piece(board,r,c))
        return list

    elif prob == "nqueen":
        for r in range(0, N):
            for c in range(0, N):
                if (r != (x - 1) or c != (y - 1)):
                    if count_on_row(board, r) < 1 and count_on_col(board, c) < 1 and count_on_fwd_diag(board, r, c) < 1 \
                            and count_on_back_diag(board, r, c) < 1:
                        list.append(add_piece(board, r, c))
        return list


# check if board is a goal state
def is_goal(board):
    return count_pieces(board) == N and \
        all( [ count_on_row(board, r) <= 1 for r in range(0, N) ] ) and \
        all( [ count_on_col(board, c) <= 1 for c in range(0, N) ] )

# Count # of pieces for given row, col in the diagonal from right to left
def count_on_back_diag(board, row, col):
    sum = 0
    r = row
    c = col
    while r < N and c >= 0:
        sum = sum + board[r][c]
        r = r + 1
        c = c - 1
    r = row
    c = col
    while r >= 0 and c < N:
        sum = sum + board[r][c]
        r = r - 1
        c = c + 1
    sum = sum - board[row][col]
    return sum

# Count # of pieces for given row, col in the diagonal from left to right
def count_on_fwd_diag(board, row, col):
    sum = 0
    r = row
    c = col
    while r < N and c < N:
        sum = sum + board[r][c]
        r = r + 1
        c = c + 1
    r = row
    c = col
    while r >= 0 and c >= 0:
        sum = sum + board[r][c]
        r = r - 1
        c = c - 1
    sum = sum - board[row][col]
    return sum

# Solve n-rooks!
#Changed the fringe to use BFS instead of DFS by changing the fring.pop to fringe.pop(0)
def solve(initial_board):
    fringe = [initial_board]
    while len(fringe) > 0:
        for s in successors2( fringe.pop()):
            if is_goal(s):
                return(s)
            fringe.append(s)
    return False

# This is N, the size of the board. It is passed through command line arguments.
prob = str(sys.argv[1])
N = int(sys.argv[2])
x = int(sys.argv[3])
y = int(sys.argv[4])

if prob != "nqueen" and prob!="nrook":
    print "Either nqueen or nrook is valid"
    exit()

if x > N or y > N:
    print "x and y coordinates should be with in N.";
    exit()

# The board is stored as a list-of-lists. Each inner list is a row of the board.
# A zero in a given square indicates no piece, and a 1 indicates a piece.
# Changed the way in which we intitialize so that when we change at a particular row, col location rest of the rows don't get effected.
initial_board = []
for i in range(0,N):
    initial_board.append([0]*N)

print ("Starting from initial board:\n" + printable_board(initial_board, prob) + "\n\nLooking for solution...\n")
solution = solve(initial_board)
print (printable_board(solution, prob) if solution else "Sorry, no solution found. :(")


