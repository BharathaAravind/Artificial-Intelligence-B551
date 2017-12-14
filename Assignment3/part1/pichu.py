# Implementing alpha-beta pruning for pichu
# For a particular state of the board , We used the following heuristic function to evaluate the board
# h(s) = 200*(K-k)+ 9*(Q-q)+ 5*(R-r) + 3*(B-b + N-n)+ 1*(P-p) +0.1*(mobility(s,'w')-mobility(s,'b'))
#
# Here the mobility function gets all the legal moves for a state for white and black which gives an extra advantage and gives out the best move for a side.
# The runtime for the board is more when the mobility feature is added



import copy
import sys
import time

#
# def printBoard(s):
#     for list in s:
#         print list

#sucessor function which generates successors of parakeet
def paraheet(s, currentPlayer):
   listOfParaheetSuccesors = []
   if currentPlayer == 'w':
       for row in range(0, len(s)):
           for col in range(0, len(s[0])):
               if s[row][col] == 'P':
                   # For killing a piece by pawn to the right
                   if col >= 0 and col < 7:
                       if s[row+1][col+1].islower():
                           if row == 6:
                               tempboard = copy.deepcopy(s)
                               tempboard[row + 1][col+1] = 'Q'
                               tempboard[row][col] = '.'
                               listOfParaheetSuccesors.append(tempboard)
                           else:
                               tempboard = copy.deepcopy(s)
                               tempboard[row+1][col+1] = 'P'
                               tempboard[row][col] = '.'
                               listOfParaheetSuccesors.append(tempboard)

                   # For killing a piece by pawn to the left
                   if col > 0 and col <= 7:
                       #For killing a piece by pawn
                       if s[row+1][col-1].islower():
                           if row == 6:
                               tempboard = copy.deepcopy(s)
                               tempboard[row + 1][col-1] = 'Q'
                               tempboard[row][col] = '.'
                               listOfParaheetSuccesors.append(tempboard)
                           else:
                               tempboard = copy.deepcopy(s)
                               tempboard[row+1][col-1] = 'P'
                               tempboard[row][col] = '.'
                               listOfParaheetSuccesors.append(tempboard)
                        #checking for first row
                   if row == 1:
                       if s[row+1][col] == '.':
                           tempboard = copy.deepcopy(s)
                           tempboard[row+1][col] = 'P'
                           tempboard[row][col] = '.'
                           listOfParaheetSuccesors.append(tempboard)

                       if s[row + 1][col] == '.' and s[row+2][col] == '.':
                           tempboard = copy.deepcopy(s)
                           tempboard[row+2][col] = 'P'
                           tempboard[row][col] = '.'
                           listOfParaheetSuccesors.append(tempboard)

                   if row > 1 and s[row + 1][col] == '.':
                       if row==6:
                           tempboard = copy.deepcopy(s)
                           tempboard[row + 1][col] = 'Q'
                           tempboard[row][col] = '.'
                           listOfParaheetSuccesors.append(tempboard)
                       else:
                           tempboard = copy.deepcopy(s)
                           tempboard[row + 1][col] = 'P'
                           tempboard[row][col] = '.'
                           listOfParaheetSuccesors.append(tempboard)

   else:
       for row in range(0, len(s)):
           for col in range(0, len(s[0])):
               if s[row][col] == 'p':
                   # For killing a piece by pawn to the right
                   if col >= 0 and col < 7:
                       if s[row-1][col+1].isupper():
                           if row == 1:
                               tempboard = copy.deepcopy(s)
                               tempboard[row - 1][col+1] = 'q'
                               tempboard[row][col] = '.'
                               listOfParaheetSuccesors.append(tempboard)
                           else:
                               tempboard = copy.deepcopy(s)
                               tempboard[row-1][col+1] = 'p'
                               tempboard[row][col] = '.'
                               listOfParaheetSuccesors.append(tempboard)

                   # For killing a piece by pawn to the left
                   if col > 0 and col <= 7:
                       #For killing a piece by pawn
                       if s[row-1][col-1].isupper():
                           if row == 1:
                               tempboard = copy.deepcopy(s)
                               tempboard[row - 1][col-1] = 'q'
                               tempboard[row][col] = '.'
                               listOfParaheetSuccesors.append(tempboard)
                           else:
                               tempboard = copy.deepcopy(s)
                               tempboard[row-1][col-1] = 'p'
                               tempboard[row][col] = '.'
                               listOfParaheetSuccesors.append(tempboard)

                   if row == 6:
                       if s[row-1][col] == '.':
                           tempboard = copy.deepcopy(s)
                           tempboard[row-1][col] = 'p'
                           tempboard[row][col] = '.'
                           listOfParaheetSuccesors.append(tempboard)

                       if s[row - 1][col] == '.' and s[row-2][col] == '.':
                           tempboard = copy.deepcopy(s)
                           tempboard[row-2][col] = 'p'
                           tempboard[row][col] = '.'
                           listOfParaheetSuccesors.append(tempboard)

                   if row < 6 and s[row-1][col] == '.':
                       if row == 1:
                           tempboard = copy.deepcopy(s)
                           tempboard[row - 1][col] = 'q'
                           tempboard[row][col] = '.'
                           listOfParaheetSuccesors.append(tempboard)
                       else:
                           tempboard = copy.deepcopy(s)
                           tempboard[row-1][col] = 'p'
                           tempboard[row][col] = '.'
                           listOfParaheetSuccesors.append(tempboard)
   return listOfParaheetSuccesors


#sucessor function which generates successors of robin
def robin(s, currentPlayer):
   listOfRobinSuccesors = []
   if currentPlayer == 'w':
       for row in range(0, len(s)):
           for col in range(0, len(s[0])):
               if s[row][col] == 'R':
                   for i in range(row+1,8):
                       if s[i][col].isupper():
                           break;
                       if s[i][col].islower():
                           tempboard = copy.deepcopy(s)
                           tempboard[i][col] = 'R'
                           tempboard[row][col] = '.'
                           listOfRobinSuccesors.append(tempboard)
                           break;
                       if s[i][col]=='.':
                           tempboard = copy.deepcopy(s)
                           tempboard[i][col] = 'R'
                           tempboard[row][col] = '.'
                           listOfRobinSuccesors.append(tempboard)
                   for i in range(row-1,-1,-1):
                       if s[i][col].isupper():
                           break;
                       if s[i][col].islower():
                           tempboard = copy.deepcopy(s)
                           tempboard[i][col] = 'R'
                           tempboard[row][col] = '.'
                           listOfRobinSuccesors.append(tempboard)
                           break;
                       if s[i][col]=='.':
                           tempboard = copy.deepcopy(s)
                           tempboard[i][col] = 'R'
                           tempboard[row][col] = '.'
                           listOfRobinSuccesors.append(tempboard)
                   for i in range(col+1,8):
                       if s[row][i].isupper():
                           break;
                       if s[row][i].islower():
                           tempboard = copy.deepcopy(s)
                           tempboard[row][i] = 'R'
                           tempboard[row][col] = '.'
                           listOfRobinSuccesors.append(tempboard)
                           break;
                       if s[row][i]=='.':
                           tempboard = copy.deepcopy(s)
                           tempboard[row][i] = 'R'
                           tempboard[row][col] = '.'
                           listOfRobinSuccesors.append(tempboard)
                   for i in range(col-1,-1,-1):
                       if s[row][i].isupper():
                           break;
                       if s[row][i].islower():
                           tempboard = copy.deepcopy(s)
                           tempboard[row][i] = 'R'
                           tempboard[row][col] = '.'
                           listOfRobinSuccesors.append(tempboard)
                           break;
                       if s[row][i]=='.':
                           tempboard = copy.deepcopy(s)
                           tempboard[row][i] = 'R'
                           tempboard[row][col] = '.'
                           listOfRobinSuccesors.append(tempboard)
   else:
       for row in range(0, len(s)):
           for col in range(0, len(s[0])):
               if s[row][col] == 'r':
                   for i in range(row+1,8):
                       if s[i][col].islower():
                           break;
                       if s[i][col].isupper():
                           tempboard = copy.deepcopy(s)
                           tempboard[i][col] = 'r'
                           tempboard[row][col] = '.'
                           listOfRobinSuccesors.append(tempboard)
                           break;
                       if s[i][col]=='.':
                           tempboard = copy.deepcopy(s)
                           tempboard[i][col] = 'r'
                           tempboard[row][col] = '.'
                           listOfRobinSuccesors.append(tempboard)
                   for i in range(row-1,-1,-1):
                       if s[i][col].islower():
                           break;
                       if s[i][col].isupper():
                           tempboard = copy.deepcopy(s)
                           tempboard[i][col] = 'r'
                           tempboard[row][col] = '.'
                           listOfRobinSuccesors.append(tempboard)
                           break;
                       if s[i][col]=='.':
                           tempboard = copy.deepcopy(s)
                           tempboard[i][col] = 'r'
                           tempboard[row][col] = '.'
                           listOfRobinSuccesors.append(tempboard)
                   for i in range(col+1,8):
                       if s[row][i].islower():
                           break;
                       if s[row][i].isupper():
                           tempboard = copy.deepcopy(s)
                           tempboard[row][i] = 'r'
                           tempboard[row][col] = '.'
                           listOfRobinSuccesors.append(tempboard)
                           break;
                       if s[row][i]=='.':
                           tempboard = copy.deepcopy(s)
                           tempboard[row][i] = 'r'
                           tempboard[row][col] = '.'
                           listOfRobinSuccesors.append(tempboard)
                   for i in range(col-1,-1,-1):
                       if s[row][i].islower():
                           break;
                       if s[row][i].isupper():
                           tempboard = copy.deepcopy(s)
                           tempboard[row][i] = 'r'
                           tempboard[row][col] = '.'
                           listOfRobinSuccesors.append(tempboard)
                           break;
                       if s[row][i]=='.':
                           tempboard = copy.deepcopy(s)
                           tempboard[row][i] = 'r'
                           tempboard[row][col] = '.'
                           listOfRobinSuccesors.append(tempboard)
   return listOfRobinSuccesors


#sucessor function which generates successors of nighthawk
def nightHawk(s, currentPlayer):
   listOfnightHawnSuccesors = []
   if currentPlayer == 'w':
       for row in range(0, len(s)):
           for col in range(0, len(s[0])):
               if s[row][col] == 'N':
                   if row+1<8 and col+2<8:
                       if not (s[row+1][col+2].isupper()):
                           tempboard = copy.deepcopy(s)
                           tempboard[row+1][col+2] = 'N'
                           tempboard[row][col] = '.'
                           listOfnightHawnSuccesors.append(tempboard)
                   if row + 1 < 8 and col -2 > -1:
                       if not (s[row + 1][col - 2].isupper()):
                           tempboard = copy.deepcopy(s)
                           tempboard[row + 1][col - 2] = 'N'
                           tempboard[row][col] = '.'
                           listOfnightHawnSuccesors.append(tempboard)
                   if row - 1 >-1 and col + 2 < 8:
                       if not (s[row - 1][col + 2].isupper()):
                           tempboard = copy.deepcopy(s)
                           tempboard[row - 1][col + 2] = 'N'
                           tempboard[row][col] = '.'
                           listOfnightHawnSuccesors.append(tempboard)
                   if row - 1 > -1 and col - 2 > -1:
                       if not (s[row - 1][col - 2].isupper()):
                           tempboard = copy.deepcopy(s)
                           tempboard[row - 1][col - 2] = 'N'
                           tempboard[row][col] = '.'
                           listOfnightHawnSuccesors.append(tempboard)
                   if row + 2 < 8 and col + 1 < 8:
                       if not (s[row + 2][col + 1].isupper()):
                           tempboard = copy.deepcopy(s)
                           tempboard[row + 2][col + 1] = 'N'
                           tempboard[row][col] = '.'
                           listOfnightHawnSuccesors.append(tempboard)
                   if row + 2 < 8 and col - 1 > -1:
                       if not (s[row + 2][col - 1].isupper()):
                           tempboard = copy.deepcopy(s)
                           tempboard[row + 2][col - 1] = 'N'
                           tempboard[row][col] = '.'
                           listOfnightHawnSuccesors.append(tempboard)
                   if row - 2 > -1 and col + 1 < 8:
                       if not (s[row - 2][col + 1].isupper()):
                           tempboard = copy.deepcopy(s)
                           tempboard[row - 2][col + 1] = 'N'
                           tempboard[row][col] = '.'
                           listOfnightHawnSuccesors.append(tempboard)
                   if row - 2 > -1 and col - 1 > -1:
                       if not (s[row - 2][col - 1].isupper()):
                           tempboard = copy.deepcopy(s)
                           tempboard[row - 2][col - 1] = 'N'
                           tempboard[row][col] = '.'
                           listOfnightHawnSuccesors.append(tempboard)

   else:
       for row in range(0, len(s)):
           for col in range(0, len(s[0])):
               if s[row][col] == 'n':
                   if row+1<8 and col+2<8:
                       if not (s[row+1][col+2].islower()):
                           tempboard = copy.deepcopy(s)
                           tempboard[row+1][col+2] = 'n'
                           tempboard[row][col] = '.'
                           listOfnightHawnSuccesors.append(tempboard)
                   if row + 1 < 8 and col -2 > -1:
                       if not (s[row + 1][col - 2].islower()):
                           tempboard = copy.deepcopy(s)
                           tempboard[row + 1][col - 2] = 'n'
                           tempboard[row][col] = '.'
                           listOfnightHawnSuccesors.append(tempboard)
                   if row - 1 >-1 and col + 2 < 8:
                       if not (s[row - 1][col + 2].islower()):
                           tempboard = copy.deepcopy(s)
                           tempboard[row - 1][col + 2] = 'n'
                           tempboard[row][col] = '.'
                           listOfnightHawnSuccesors.append(tempboard)
                   if row - 1 > -1 and col - 2 > -1:
                       if not (s[row - 1][col - 2].islower()):
                           tempboard = copy.deepcopy(s)
                           tempboard[row - 1][col - 2] = 'n'
                           tempboard[row][col] = '.'
                           listOfnightHawnSuccesors.append(tempboard)
                   if row + 2 < 8 and col + 1 < 8:
                       if not (s[row + 2][col + 1].islower()):
                           tempboard = copy.deepcopy(s)
                           tempboard[row + 2][col + 1] = 'n'
                           tempboard[row][col] = '.'
                           listOfnightHawnSuccesors.append(tempboard)
                   if row + 2 < 8 and col - 1 > -1:
                       if not (s[row + 2][col - 1].islower()):
                           tempboard = copy.deepcopy(s)
                           tempboard[row + 2][col - 1] = 'n'
                           tempboard[row][col] = '.'
                           listOfnightHawnSuccesors.append(tempboard)
                   if row - 2 > -1 and col + 1 < 8:
                       if not (s[row - 2][col + 1].islower()):
                           tempboard = copy.deepcopy(s)
                           tempboard[row - 2][col + 1] = 'n'
                           tempboard[row][col] = '.'
                           listOfnightHawnSuccesors.append(tempboard)
                   if row - 2 > -1 and col - 1 > -1:
                       if not (s[row - 2][col - 1].islower()):
                           tempboard = copy.deepcopy(s)
                           tempboard[row - 2][col - 1] = 'n'
                           tempboard[row][col] = '.'
                           listOfnightHawnSuccesors.append(tempboard)
   return listOfnightHawnSuccesors


#sucessor function which generates successors of quitzal
def quitzal(s, currentPlayer):
   listOfQuitzalSuccesors = []
   if currentPlayer == 'w':
       for row in range(0, len(s)):
           for col in range(0, len(s[0])):
               if s[row][col] == 'Q':
                   for i in range(row+1,8):
                       if s[i][col].isupper():
                           break;
                       if s[i][col].islower():
                           tempboard = copy.deepcopy(s)
                           tempboard[i][col] = 'Q'
                           tempboard[row][col] = '.'
                           listOfQuitzalSuccesors.append(tempboard)
                           break;
                       if s[i][col]=='.':
                           tempboard = copy.deepcopy(s)
                           tempboard[i][col] = 'Q'
                           tempboard[row][col] = '.'
                           listOfQuitzalSuccesors.append(tempboard)
                   for i in range(row-1,-1,-1):
                       if s[i][col].isupper():
                           break;
                       if s[i][col].islower():
                           tempboard = copy.deepcopy(s)
                           tempboard[i][col] = 'Q'
                           tempboard[row][col] = '.'
                           listOfQuitzalSuccesors.append(tempboard)
                           break;
                       if s[i][col]=='.':
                           tempboard = copy.deepcopy(s)
                           tempboard[i][col] = 'Q'
                           tempboard[row][col] = '.'
                           listOfQuitzalSuccesors.append(tempboard)
                   for i in range(col+1,8):
                       if s[row][i].isupper():
                           break;
                       if s[row][i].islower():
                           tempboard = copy.deepcopy(s)
                           tempboard[row][i] = 'Q'
                           tempboard[row][col] = '.'
                           listOfQuitzalSuccesors.append(tempboard)
                           break;
                       if s[row][i]=='.':
                           tempboard = copy.deepcopy(s)
                           tempboard[row][i] = 'Q'
                           tempboard[row][col] = '.'
                           listOfQuitzalSuccesors.append(tempboard)
                   for i in range(col-1,-1,-1):
                       if s[row][i].isupper():
                           break;
                       if s[row][i].islower():
                           tempboard = copy.deepcopy(s)
                           tempboard[row][i] = 'Q'
                           tempboard[row][col] = '.'
                           listOfQuitzalSuccesors.append(tempboard)
                           break;
                       if s[row][i]=='.':
                           tempboard = copy.deepcopy(s)
                           tempboard[row][i] = 'Q'
                           tempboard[row][col] = '.'
                           listOfQuitzalSuccesors.append(tempboard)
                   for i in range(row+1,8):
                       if col+(i-row)<8:
                           if s[i][col+(i-row)].isupper():
                               break;
                           if s[i][col+(i-row)].islower():
                               tempboard = copy.deepcopy(s)
                               tempboard[i][col+(i-row)] = 'Q'
                               tempboard[row][col] = '.'
                               listOfQuitzalSuccesors.append(tempboard)
                               break;
                           if s[i][col+(i-row)]=='.':
                               tempboard = copy.deepcopy(s)
                               tempboard[i][col+(i-row)] = 'Q'
                               tempboard[row][col] = '.'
                               listOfQuitzalSuccesors.append(tempboard)
                       if col-(i-row)>-1:
                           if s[i][col-(i-row)].isupper():
                               break;
                           if s[i][col-(i-row)].islower():
                               tempboard = copy.deepcopy(s)
                               tempboard[i][col-(i-row)] = 'Q'
                               tempboard[row][col] = '.'
                               listOfQuitzalSuccesors.append(tempboard)
                               break;
                           if s[i][col-(i-row)]=='.':
                               tempboard = copy.deepcopy(s)
                               tempboard[i][col-(i-row)] = 'Q'
                               tempboard[row][col] = '.'
                               listOfQuitzalSuccesors.append(tempboard)
                   for i in range(row-1,-1,-1):
                       if col+(row-i)<8:
                           if s[i][col+(row-i)].isupper():
                               break;
                           if s[i][col+(row-i)].islower():
                               tempboard = copy.deepcopy(s)
                               tempboard[i][col+(row-i)] = 'Q'
                               tempboard[row][col] = '.'
                               listOfQuitzalSuccesors.append(tempboard)
                               break;
                           if s[i][col+(row-i)]=='.':
                               tempboard = copy.deepcopy(s)
                               tempboard[i][col+(row-i)] = 'Q'
                               tempboard[row][col] = '.'
                               listOfQuitzalSuccesors.append(tempboard)
                       if col-(row-i)>-1:
                           if s[i][col-(row-i)].isupper():
                               break;
                           if s[i][col-(row-i)].islower():
                               tempboard = copy.deepcopy(s)
                               tempboard[i][col-(row-i)] = 'Q'
                               tempboard[row][col] = '.'
                               listOfQuitzalSuccesors.append(tempboard)
                               break;
                           if s[i][col-(row-i)]=='.':
                               tempboard = copy.deepcopy(s)
                               tempboard[i][col-(row-i)] = 'Q'
                               tempboard[row][col] = '.'
                               listOfQuitzalSuccesors.append(tempboard)
   else:
       for row in range(0, len(s)):
           for col in range(0, len(s[0])):
               if s[row][col] == 'q':
                   for i in range(row + 1, 8):
                       if s[i][col].islower():
                           break;
                       if s[i][col].isupper():
                           tempboard = copy.deepcopy(s)
                           tempboard[i][col] = 'q'
                           tempboard[row][col] = '.'
                           listOfQuitzalSuccesors.append(tempboard)
                           break;
                       if s[i][col] == '.':
                           tempboard = copy.deepcopy(s)
                           tempboard[i][col] = 'q'
                           tempboard[row][col] = '.'
                           listOfQuitzalSuccesors.append(tempboard)
                   for i in range(row - 1, -1, -1):
                       if s[i][col].islower():
                           break;
                       if s[i][col].isupper():
                           tempboard = copy.deepcopy(s)
                           tempboard[i][col] = 'q'
                           tempboard[row][col] = '.'
                           listOfQuitzalSuccesors.append(tempboard)
                           break;
                       if s[i][col] == '.':
                           tempboard = copy.deepcopy(s)
                           tempboard[i][col] = 'q'
                           tempboard[row][col] = '.'
                           listOfQuitzalSuccesors.append(tempboard)
                   for i in range(col + 1, 8):
                       if s[row][i].islower():
                           break;
                       if s[row][i].isupper():
                           tempboard = copy.deepcopy(s)
                           tempboard[row][i] = 'q'
                           tempboard[row][col] = '.'
                           listOfQuitzalSuccesors.append(tempboard)
                           break;
                       if s[row][i] == '.':
                           tempboard = copy.deepcopy(s)
                           tempboard[row][i] = 'q'
                           tempboard[row][col] = '.'
                           listOfQuitzalSuccesors.append(tempboard)
                   for i in range(col - 1, -1, -1):
                       if s[row][i].islower():
                           break;
                       if s[row][i].isupper():
                           tempboard = copy.deepcopy(s)
                           tempboard[row][i] = 'q'
                           tempboard[row][col] = '.'
                           listOfQuitzalSuccesors.append(tempboard)
                           break;
                       if s[row][i] == '.':
                           tempboard = copy.deepcopy(s)
                           tempboard[row][i] = 'q'
                           tempboard[row][col] = '.'
                           listOfQuitzalSuccesors.append(tempboard)
                   for i in range(row+1,8):
                       if col+(i-row)<8:
                           if s[i][col+(i-row)].islower():
                               break;
                           if s[i][col+(i-row)].isupper():
                               tempboard = copy.deepcopy(s)
                               tempboard[i][col+(i-row)] = 'q'
                               tempboard[row][col] = '.'
                               listOfQuitzalSuccesors.append(tempboard)
                               break;
                           if s[i][col+(i-row)]=='.':
                               tempboard = copy.deepcopy(s)
                               tempboard[i][col+(i-row)] = 'q'
                               tempboard[row][col] = '.'
                               listOfQuitzalSuccesors.append(tempboard)
                       if col-(i-row)>-1:
                           if s[i][col-(i-row)].islower():
                               break;
                           if s[i][col-(i-row)].isupper():
                               tempboard = copy.deepcopy(s)
                               tempboard[i][col-(i-row)] = 'q'
                               tempboard[row][col] = '.'
                               listOfQuitzalSuccesors.append(tempboard)
                               break;
                           if s[i][col-(i-row)]=='.':
                               tempboard = copy.deepcopy(s)
                               tempboard[i][col-(i-row)] = 'q'
                               tempboard[row][col] = '.'
                               listOfQuitzalSuccesors.append(tempboard)
                   for i in range(row-1,-1,-1):
                       if col+(row-i)<8:
                           if s[i][col+(row-i)].islower():
                               break;
                           if s[i][col+(row-i)].isupper():
                               tempboard = copy.deepcopy(s)
                               tempboard[i][col+(row-i)] = 'q'
                               tempboard[row][col] = '.'
                               listOfQuitzalSuccesors.append(tempboard)
                               break;
                           if s[i][col+(row-i)]=='.':
                               tempboard = copy.deepcopy(s)
                               tempboard[i][col+(row-i)] = 'q'
                               tempboard[row][col] = '.'
                               listOfQuitzalSuccesors.append(tempboard)
                       if col-(row-i)>-1:
                           if s[i][col-(row-i)].islower():
                               break;
                           if s[i][col-(row-i)].isupper():
                               tempboard = copy.deepcopy(s)
                               tempboard[i][col-(row-i)] = 'q'
                               tempboard[row][col] = '.'
                               listOfQuitzalSuccesors.append(tempboard)
                               break;
                           if s[i][col-(row-i)]=='.':
                               tempboard = copy.deepcopy(s)
                               tempboard[i][col-(row-i)] = 'q'
                               tempboard[row][col] = '.'
                               listOfQuitzalSuccesors.append(tempboard)
   return listOfQuitzalSuccesors


#sucessor function which generates successors of bluejay
def blueJay(s, currentPlayer):
   listOfBlueJaySuccesors = []
   if currentPlayer == 'w':
       for row in range(0, len(s)):
           for col in range(0, len(s[0])):
               if s[row][col] == 'B':
                   for i in range(row+1,8):
                       if col+(i-row)<8:
                           if s[i][col+(i-row)].isupper():
                               break;
                           if s[i][col+(i-row)].islower():
                               tempboard = copy.deepcopy(s)
                               tempboard[i][col+(i-row)] = 'B'
                               tempboard[row][col] = '.'
                               listOfBlueJaySuccesors.append(tempboard)
                               break;
                           if s[i][col+(i-row)]=='.':
                               tempboard = copy.deepcopy(s)
                               tempboard[i][col+(i-row)] = 'B'
                               tempboard[row][col] = '.'
                               listOfBlueJaySuccesors.append(tempboard)
                       if col-(i-row)>-1:
                           if s[i][col-(i-row)].isupper():
                               break;
                           if s[i][col-(i-row)].islower():
                               tempboard = copy.deepcopy(s)
                               tempboard[i][col-(i-row)] = 'B'
                               tempboard[row][col] = '.'
                               listOfBlueJaySuccesors.append(tempboard)
                               break;
                           if s[i][col-(i-row)]=='.':
                               tempboard = copy.deepcopy(s)
                               tempboard[i][col-(i-row)] = 'B'
                               tempboard[row][col] = '.'
                               listOfBlueJaySuccesors.append(tempboard)
                   for i in range(row-1,-1,-1):
                       if col+(row-i)<8:
                           if s[i][col+(row-i)].isupper():
                               break;
                           if s[i][col+(row-i)].islower():
                               tempboard = copy.deepcopy(s)
                               tempboard[i][col+(row-i)] = 'B'
                               tempboard[row][col] = '.'
                               listOfBlueJaySuccesors.append(tempboard)
                               break;
                           if s[i][col+(row-i)]=='.':
                               tempboard = copy.deepcopy(s)
                               tempboard[i][col+(row-i)] = 'B'
                               tempboard[row][col] = '.'
                               listOfBlueJaySuccesors.append(tempboard)
                       if col-(row-i)>-1:
                           if s[i][col-(row-i)].isupper():
                               break;
                           if s[i][col-(row-i)].islower():
                               tempboard = copy.deepcopy(s)
                               tempboard[i][col-(row-i)] = 'B'
                               tempboard[row][col] = '.'
                               listOfBlueJaySuccesors.append(tempboard)
                               break;
                           if s[i][col-(row-i)]=='.':
                               tempboard = copy.deepcopy(s)
                               tempboard[i][col-(row-i)] = 'B'
                               tempboard[row][col] = '.'
                               listOfBlueJaySuccesors.append(tempboard)
   else:
       for row in range(0, len(s)):
           for col in range(0, len(s[0])):
               if s[row][col] == 'b':
                   for i in range(row+1,8):
                       if col+(i-row)<8:
                           if s[i][col+(i-row)].islower():
                               break;
                           if s[i][col+(i-row)].isupper():
                               tempboard = copy.deepcopy(s)
                               tempboard[i][col+(i-row)] = 'b'
                               tempboard[row][col] = '.'
                               listOfBlueJaySuccesors.append(tempboard)
                               break;
                           if s[i][col+(i-row)]=='.':
                               tempboard = copy.deepcopy(s)
                               tempboard[i][col+(i-row)] = 'b'
                               tempboard[row][col] = '.'
                               listOfBlueJaySuccesors.append(tempboard)
                       if col-(i-row)>-1:
                           if s[i][col-(i-row)].islower():
                               break;
                           if s[i][col-(i-row)].isupper():
                               tempboard = copy.deepcopy(s)
                               tempboard[i][col-(i-row)] = 'b'
                               tempboard[row][col] = '.'
                               listOfBlueJaySuccesors.append(tempboard)
                               break;
                           if s[i][col-(i-row)]=='.':
                               tempboard = copy.deepcopy(s)
                               tempboard[i][col-(i-row)] = 'b'
                               tempboard[row][col] = '.'
                               listOfBlueJaySuccesors.append(tempboard)
                   for i in range(row-1,-1,-1):
                       if col+(row-i)<8:
                           if s[i][col+(row-i)].islower():
                               break;
                           if s[i][col+(row-i)].isupper():
                               tempboard = copy.deepcopy(s)
                               tempboard[i][col+(row-i)] = 'b'
                               tempboard[row][col] = '.'
                               listOfBlueJaySuccesors.append(tempboard)
                               break;
                           if s[i][col+(row-i)]=='.':
                               tempboard = copy.deepcopy(s)
                               tempboard[i][col+(row-i)] = 'b'
                               tempboard[row][col] = '.'
                               listOfBlueJaySuccesors.append(tempboard)
                       if col-(row-i)>-1:
                           if s[i][col-(row-i)].islower():
                               break;
                           if s[i][col-(row-i)].isupper():
                               tempboard = copy.deepcopy(s)
                               tempboard[i][col-(row-i)] = 'b'
                               tempboard[row][col] = '.'
                               listOfBlueJaySuccesors.append(tempboard)
                               break;
                           if s[i][col-(row-i)]=='.':
                               tempboard = copy.deepcopy(s)
                               tempboard[i][col-(row-i)] = 'b'
                               tempboard[row][col] = '.'
                               listOfBlueJaySuccesors.append(tempboard)
   return listOfBlueJaySuccesors


#sucessor function which generates successors of kingfisher
def kingFisher(s, currentPlayer):
   listOfKingFisherSuccesors = []
   if currentPlayer == 'w':
       for row in range(0, len(s)):
           for col in range(0, len(s[0])):
               if s[row][col] == 'K':
                   if col+1<8 and (s[row][col+1].islower() or s[row][col+1] =='.'):
                       # s[row][col + 1] = 'K'
                       tempboard = copy.deepcopy(s)
                       tempboard[row][col+1] = 'K'
                       tempboard[row][col] = '.'
                       listOfKingFisherSuccesors.append(tempboard)

                   if col-1>-1 and (s[row][col-1].islower() or s[row][col-1] =='.'):
                        # s[row][col - 1] = 'K'
                        tempboard = copy.deepcopy(s)
                        tempboard[row][col -1] = 'K'
                        tempboard[row][col] = '.'
                        listOfKingFisherSuccesors.append(tempboard)

                   if row+1 < 8 and (s[row + 1][col].islower() or s[row + 1][col] =='.'):
                       #s[row + 1][col] = 'K'
                       tempboard = copy.deepcopy(s)
                       tempboard[row + 1][col] = 'K'
                       tempboard[row][col] = '.'
                       listOfKingFisherSuccesors.append(tempboard)
                       if col+1<8 and (s[row + 1][col+1].islower() or s[row + 1][col+1] =='.'):
                           #s[row + 1][col + 1] = 'K'
                           tempboard = copy.deepcopy(s)
                           tempboard[row + 1][col+1] = 'K'
                           tempboard[row][col] = '.'
                           listOfKingFisherSuccesors.append(tempboard)
                       if col-1>-1 and (s[row + 1][col-1].islower() or s[row + 1][col-1] =='.'):
                            #s[row + 1][col - 1] = 'K'
                            tempboard = copy.deepcopy(s)
                            tempboard[row + 1][col - 1] = 'K'
                            tempboard[row][col] = '.'
                            listOfKingFisherSuccesors.append(tempboard)

                   if row-1>-1 and (s[row - 1][col].islower() or s[row - 1][col] =='.'):
                        #s[row-1][col] = 'K'
                        tempboard = copy.deepcopy(s)
                        tempboard[row - 1][col] = 'K'
                        tempboard[row][col] = '.'
                        listOfKingFisherSuccesors.append(tempboard)
                        if col+1<8 and (s[row - 1][col+1].islower() or s[row - 1][col+1] =='.'):
                           #s[row - 1][col + 1] = 'K'
                           tempboard = copy.deepcopy(s)
                           tempboard[row - 1][col+1] = 'K'
                           tempboard[row][col] = '.'
                           listOfKingFisherSuccesors.append(tempboard)
                        if col-1>-1 and (s[row - 1][col-1].islower() or s[row - 1][col-1] =='.'):
                           # s[row - 1][col - 1] = 'K'
                           tempboard = copy.deepcopy(s)
                           tempboard[row - 1][col-1] = 'K'
                           tempboard[row][col] = '.'
                           listOfKingFisherSuccesors.append(tempboard)
   else:
       for row in range(0, len(s)):
           for col in range(0, len(s[0])):
               if s[row][col] == 'k':
                   if col+1<8 and (s[row][col + 1].isupper() or s[row][col+1]=='.'):
                       # s[row][col + 1] = 'K'
                       tempboard = copy.deepcopy(s)
                       tempboard[row][col+1] = 'k'
                       tempboard[row][col] = '.'
                       listOfKingFisherSuccesors.append(tempboard)

                   if col-1>-1 and (s[row][col - 1].isupper() or s[row][col-1]=='.'):
                        # s[row][col - 1] = 'K'
                        tempboard = copy.deepcopy(s)
                        tempboard[row][col -1] = 'k'
                        tempboard[row][col] = '.'
                        listOfKingFisherSuccesors.append(tempboard)

                   if row+1 < 8 and (s[row+1][col].isupper() or s[row+1][col]=='.'):
                       #s[row + 1][col] = 'K'
                       tempboard = copy.deepcopy(s)
                       tempboard[row + 1][col] = 'k'
                       tempboard[row][col] = '.'
                       listOfKingFisherSuccesors.append(tempboard)
                       if col+1<8 and (s[row+1][col + 1].isupper() or s[row+1][col+1]=='.'):
                           #s[row + 1][col + 1] = 'K'
                           tempboard = copy.deepcopy(s)
                           tempboard[row + 1][col+1] = 'k'
                           tempboard[row][col] = '.'
                           listOfKingFisherSuccesors.append(tempboard)
                       if col-1>-1 and (s[row+1][col - 1].isupper() or s[row+1][col-1]=='.'):
                            #s[row + 1][col - 1] = 'K'
                            tempboard = copy.deepcopy(s)
                            tempboard[row + 1][col - 1] = 'k'
                            tempboard[row][col] = '.'
                            listOfKingFisherSuccesors.append(tempboard)

                   if row-1>-1 and (s[row-1][col].isupper() or s[row-1][col]=='.'):
                        #s[row-1][col] = 'K'
                        tempboard = copy.deepcopy(s)
                        tempboard[row - 1][col] = 'k'
                        tempboard[row][col] = '.'
                        listOfKingFisherSuccesors.append(tempboard)
                        if col+1<8 and (s[row-1][col + 1].isupper() or s[row-1][col+1]=='.'):
                           #s[row - 1][col + 1] = 'K'
                           tempboard = copy.deepcopy(s)
                           tempboard[row - 1][col+1] = 'k'
                           tempboard[row][col] = '.'
                           listOfKingFisherSuccesors.append(tempboard)
                        if col-1>-1 and (s[row-1][col - 1].isupper() or s[row-1][col-1]=='.'):
                           # s[row - 1][col - 1] = 'K'
                           tempboard = copy.deepcopy(s)
                           tempboard[row - 1][col-1] = 'k'
                           tempboard[row][col] = '.'
                           listOfKingFisherSuccesors.append(tempboard)

   return listOfKingFisherSuccesors

#combines all successors
def successor(s, maxplayer):
    list_succ = []
    if maxplayer == 'w':
        for l in kingFisher(s,'w'):
            score = evaluationFunction(l)
            list_succ.append([score, score, l])
        for l in quitzal(s,'w'):
            score = evaluationFunction(l)
            list_succ.append([score, score, l])
        for l in blueJay(s,'w'):
            score = evaluationFunction(l)
            list_succ.append([score, score, l])
        for l in nightHawk(s,'w'):
            score = evaluationFunction(l)
            list_succ.append([score, score, l])
        for l in robin(s,'w'):
            score = evaluationFunction(l)
            list_succ.append([score, score, l])
        for l in paraheet(s,'w'):
            score = evaluationFunction(l)
            list_succ.append([score, score, l])

    else:
        for l in kingFisher(s,'b'):
            score = evaluationFunction(l)
            list_succ.append([score, score, l])
        for l in quitzal(s,'b'):
            score = evaluationFunction(l)
            list_succ.append([score, score, l])
        for l in blueJay(s,'b'):
            score = evaluationFunction(l)
            list_succ.append([score, score, l])
        for l in nightHawk(s,'b'):
            score = evaluationFunction(l)
            list_succ.append([score, score, l])
        for l in robin(s,'b'):
            score = evaluationFunction(l)
            list_succ.append([score, score, l])
        for l in paraheet(s,'b'):
            score = evaluationFunction(l)
            list_succ.append([score, score, l])
    return list_succ

#evalluation function which calculates the board value
def evaluationFunction(s):

    K=0;Q=0;B=0;N=0;R=0;P=0;k=0;q=0;b=0;n=0;r=0;p=0

    for line in s:
        K = K + line.count('K')
        Q = Q + line.count('Q')
        B = B + line.count('B')
        N = N + line.count('N')
        R = R + line.count('R')
        P = P + line.count('P')
        k = k + line.count('k')
        q = q + line.count('q')
        b = b + line.count('b')
        n = n + line.count('n')
        r = r + line.count('r')
        p = p + line.count('p')


    if maxplayer=='w':
        # printBoard(s)
        # print 200*(K-k)+ 9*(Q-q)+ 5*(R-r) + 3*(B-b + N-n)+ 1*(P-p)+0.1*(mobility(s,'w')-mobility(s,'b'))
        return 200*(K-k)+ 9*(Q-q)+ 5*(R-r) + 3*(B-b + N-n)+ 1*(P-p) +0.1*(mobility(s,'w')-mobility(s,'b'))
    else:
        # printBoard(s)
        # print 200*(k-K)+ 9*(q-Q)+ 5*(r-R) + 3*(b-B + n-N)+ 1*(p-P)+0.1*(mobility(s,'b')-mobility(s,'w'))
        return 200*(k-K)+ 9*(q-Q)+ 5*(r-R) + 3*(b-B + n-N)+ 1*(p-P) +0.1*(mobility(s,'b')-mobility(s,'w'))


#moability function which calculates no.of possible movements of all pawns for a player
def mobility(s,maxplayer):
    # print len(kingFisher(s,maxplayer))+len(quitzal(s,maxplayer))+len(blueJay(s,maxplayer))+len(nightHawk(s,maxplayer))+len(robin(s,maxplayer))+len(paraheet(s,maxplayer))
    return len(kingFisher(s,maxplayer))+len(quitzal(s,maxplayer))+len(blueJay(s,maxplayer))+len(nightHawk(s,maxplayer))+len(robin(s,maxplayer))+len(paraheet(s,maxplayer))

def checkInState(s):
    s = s[2]
    K =0; k=0;
    for line in s:
        K = K + line.count('K')
        k = k + line.count('k')
    if K-k != 0:
        return True
    else:
        return False

#max value played by the max player
def maxValues(s,depth):
    depth = depth + 1
    currentPlayer = ''
    if maxplayer == 'w':
        currentPlayer = 'w'
    else:
        currentPlayer = 'b'

    if depth >= DEPTH or checkInState(s):
        return s
    successors = successor(s[2], currentPlayer)
    for succ in successors:
        l = minValues(succ,depth)
        s[1] = max(s[1], l)
        if s[1] < l:
            s[1] = l
        if s[0]>s[1]:
            return s
    return s
#played by the min player
def minValues(s, depth):
    depth = depth + 1
    currentPlayer = ''
    if maxplayer == 'w':
        currentPlayer = 'b'
    else:
        currentPlayer = 'w'

    if depth == DEPTH or checkInState(s):
        return s
    successors = successor(s[2], currentPlayer)
    for succ in successors:
        l = maxValues(succ,depth+1)
        if s[1] >= l:
            s[1] = l
        if s[0]>s[1]:
            return s
    return s
#alpha beta decsion
def alphaBetaDecision(initialboard):
    #take second argyment from command line
    listOfSuccessors = successor(initialBoard[2], maxplayer)
    ll = []
    for succ in listOfSuccessors:
        ll.append(minValues(succ,0))
    #sprt ll and take mzaminum
    ll.sort()
    return ll[len(ll)-1]

#convert board string to list of list
def convertBoard(s):
    list = []
    for i in range(0, 57, 8):
        list.append(map(None, s[i: i+8]))
    return list

board = convertBoard(sys.argv[2])


alpha = 9999999999
beta = -9999999999
maxplayer = sys.argv[1]
initialBoard = [alpha, beta, board]
'''
#successor(initialBoard)
printBoard(initialBoard[2])
print 'lsNDL'
ll = nightHawk(initialBoard[2],'w')
evaluationFunction(initialBoard[2])


ll = successor(initialBoard[2])

for  l in ll:
    printBoard(l)
    print('next successor')
'''

# player = 'w'
depth = 0

# printBoard(initialBoard[2])
# print '***'
for i in range(3,11):
    DEPTH = i
    start = time.time()
    solList = alphaBetaDecision(initialBoard)[2]
    end = time.time()
    #print end - start
    # for l in solList:
    #     print l
    sol = ''
    for j in solList:
        sol = sol + ''.join(j)
    # print DEPTH
    print sol
    # print '*'*50

# print initialBoard[2]
# for l in alphaBetaDecision(initialBoard):
#     print 'hi'
#     print l[0]
#     printBoard(l[2])
# print kingFisher(initialBoard[2],'b')