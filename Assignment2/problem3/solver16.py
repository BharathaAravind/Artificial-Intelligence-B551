#!/usr/bin/env python
# put your 15 puzzle solver here!

import copy
import math
import sys

#Function to determine the position of 0 in the board returns x & y coodinates of the board
def findEmptyPos(board, charToBeFound=0):
	for row in range(0,4,1):
		for col in range(0,4,1):
			if board[row][col] == charToBeFound:
				pos=(row, col)
				return ([(pos)])

#To understand the hueristics and the one that can be applied to this problem has been referenced in websites
#http://www.brian-borowski.com/software/puzzle/ & http://kociemba.org/fifteen/fifteensolver.html
#Function to determine the hueristic value using the number of misplaced tiles in a given board
#def defineHueristic(tempBoard):
#	hueristicValue=0
#	if tempBoard[0][0] != 1 :
#		hueristicValue+=1
#	if tempBoard[0][1] != 2 :
#		hueristicValue+=1
#	if tempBoard[0][2] != 3 :
#		hueristicValue+=1
#	if tempBoard[0][3] != 4 :
#		hueristicValue+=1
#	if tempBoard[1][0] != 5 :
#		hueristicValue+=1
#	if tempBoard[1][1] != 6 :
#		hueristicValue+=1
#	if tempBoard[1][2] != 7 :
#		hueristicValue+=1
#	if tempBoard[1][3] != 8 :
#		hueristicValue+=1
#	if tempBoard[2][0] != 9 :
#		hueristicValue+=1
#	if tempBoard[2][1] != 10 :
#		hueristicValue+=1
#	if tempBoard[2][2] != 11 :
#		hueristicValue+=1
#	if tempBoard[2][3] != 12 :
#		hueristicValue+=1
#	if tempBoard[3][0] != 13 :
#		hueristicValue+=1
#	if tempBoard[3][1] != 14 :
#		hueristicValue+=1
#	if tempBoard[3][2] != 15 :
#		hueristicValue+=1
#	return hueristicValue

#Function to determine the hueristic value using the manhattan distance
#To understand implementation of Manhattan Puzzle used references
#https://stackoverflow.com/questions/8224470/calculating-manhattan-distance & https://stackoverflow.com/questions/12526792/manhattan-distance-in-a
def manhattanDistanceHueristic(board):
	manhattanDistance = 0
	for row in range (0,4,1):
		for col in range (0,4,1):
			cellValue = board[row][col]
			if cellValue != 0:
				if cellValue == 1:
					origXPos=0
					origYPos=0
				if cellValue == 2:
					origXPos=0
					origYPos=1
				if cellValue == 3:
					origXPos=0
					origYPos=2
				if cellValue == 4:
					origXPos=0
					origYPos=3
				if cellValue == 5:
					origXPos=1
					origYPos=0
				if cellValue == 6:
					origXPos=1
					origYPos=1
				if cellValue == 7:
					origXPos=1
					origYPos=2
				if cellValue == 8:
					origXPos=1
					origYPos=3
				if cellValue == 9:
					origXPos=2
					origYPos=0
				if cellValue == 10:
					origXPos=2
					origYPos=1
				if cellValue == 11:
					origXPos=2
					origYPos=2		
				if cellValue == 12:
					origXPos=2
					origYPos=3
				if cellValue == 13:
					origXPos=3
					origYPos=0
				if cellValue == 14:
					origXPos=3
					origYPos=1
				if cellValue == 15:
					origXPos=3
					origYPos=2
				diffToX = row - origXPos
				diffToY = col - origYPos
				manhattanDistance = manhattanDistance + abs(diffToX) + abs(diffToY)
	return manhattanDistance

#Function to get a list of all successors up from the x & y coodinates of 0
def successorUp(initial_board, indexPos):
	i=1
	xPos=indexPos[0]
	yPos=indexPos[1]
	tempState=copy.deepcopy(initial_board)
	stateCounter=0
	#counter=xPos
	for i in range(xPos,0,-1):
		tempBoard=copy.deepcopy(tempState)
		tempBoard[xPos][yPos]=tempState[xPos-1][yPos]
		tempBoard[xPos-1][yPos]=0
		xPos-=1
		tempBoardHueristics=manhattanDistanceHueristic(tempBoard)
		insertFlag='Y'
		for visitedCounter in range(0,len(visitedStates),1):
			if tempBoard==visitedStates[visitedCounter]:
				insertFlag='N'
				break
		if insertFlag=='Y':
			stateCounter+=1
			priorityQueue.setdefault(tempBoardHueristics,[])
			priorityQueue[tempBoardHueristics].append(copy.deepcopy(tempBoard))
			pathTaken[" ".join([ " ".join([ str(col) for col in row ]) for row in tempBoard])]='U'+str(stateCounter)+str(yPos+1)
		tempState=copy.deepcopy(tempBoard)

#Function to get a list of all successors left from the x & y coodinates of 0
def successorLeft(initial_board, indexPos):
	i=1
	xPos=indexPos[0]
	yPos=indexPos[1]
	tempState=copy.deepcopy(initial_board)
	stateCounter=0
	#counter=yPos
	for i in range(yPos,3,1):
		tempBoard=copy.deepcopy(tempState)
		tempBoard[xPos][yPos]=tempState[xPos][yPos+1]
		tempBoard[xPos][yPos+1]=0
		yPos+=1
		tempBoardHueristics=manhattanDistanceHueristic(tempBoard)
		insertFlag='Y'
		for visitedCounter in range(0,len(visitedStates),1):
			if tempBoard==visitedStates[visitedCounter]:
				insertFlag='N'
				break
		if insertFlag=='Y':
			stateCounter+=1
			priorityQueue.setdefault(tempBoardHueristics,[])
			priorityQueue[tempBoardHueristics].append(copy.deepcopy(tempBoard))
			pathTaken[" ".join([ " ".join([ str(col) for col in row ]) for row in tempBoard])]='L'+str(stateCounter)+str(xPos+1)
		tempState=copy.deepcopy(tempBoard)

#Function to get a list of all successors down from the x & y coodinates of 0
def successorDown(initial_board, indexPos):
	i=1
	xPos=indexPos[0]
	yPos=indexPos[1]
	tempState=copy.deepcopy(initial_board)
	stateCounter=0
	#counter=xPos
	for i in range(xPos,3,1):
		tempBoard=copy.deepcopy(tempState)
		tempBoard[xPos][yPos]=tempState[xPos+1][yPos]
		tempBoard[xPos+1][yPos]=0
		xPos+=1
		tempBoardHueristics=manhattanDistanceHueristic(tempBoard)
		insertFlag='Y'
		for visitedCounter in range(0,len(visitedStates),1):
			if tempBoard==visitedStates[visitedCounter]:
				insertFlag='N'
				break
		if insertFlag=='Y':
			stateCounter+=1
			priorityQueue.setdefault(tempBoardHueristics,[])
			priorityQueue[tempBoardHueristics].append(copy.deepcopy(tempBoard))
			pathTaken[" ".join([ " ".join([ str(col) for col in row ]) for row in tempBoard])]='D'+str(stateCounter)+str(yPos+1)
		tempState=copy.deepcopy(tempBoard)

#Function to get a list of all successors right from the x & y coodinates of 0
def successorRight(initial_board, indexPos):
	i=1
	xPos=indexPos[0]
	yPos=indexPos[1]
	tempState=copy.deepcopy(initial_board)
	stateCounter=0
	#counter=yPos
	for i in range(yPos,0,-1):
		tempBoard=copy.deepcopy(tempState)
		tempBoard[xPos][yPos]=tempState[xPos][yPos-1]
		tempBoard[xPos][yPos-1]=0
		yPos-=1
		tempBoardHueristics=manhattanDistanceHueristic(tempBoard)
		insertFlag='Y'
		for visitedCounter in range(0,len(visitedStates),1):
			if tempBoard==visitedStates[visitedCounter]:
				insertFlag='N'
				break
		if insertFlag=='Y':
			stateCounter+=1
			priorityQueue.setdefault(tempBoardHueristics,[])
			priorityQueue[tempBoardHueristics].append(copy.deepcopy(tempBoard))
			pathTaken[" ".join([ " ".join([ str(col) for col in row ]) for row in tempBoard])]='R'+str(stateCounter)+str(xPos+1)
		tempState=copy.deepcopy(tempBoard)

#Function to print the final and initial board in a human readable format
def printable_board(board):
	return "\n".join([ "\t".join([ str(col) for col in row ]) for row in board])

#Function to solve the 15 puzzle board
def solve(initial_board):
	successorValue=copy.deepcopy(initial_board)
	while(True):
		indexOfZero=findEmptyPos(successorValue)
		successorUp(successorValue,indexOfZero[0])
		successorDown(successorValue,indexOfZero[0])
		successorLeft(successorValue,indexOfZero[0])
		successorRight(successorValue,indexOfZero[0])
		while True:
			minValue=min(priorityQueue)
			if not priorityQueue[minValue]:
				priorityQueue.pop((minValue),None)
			else:
				successorValue=copy.deepcopy(priorityQueue[minValue].pop(0))
				successorSet="Y"
				for visitedCounter in range(0,len(visitedStates),1):
					if successorValue==visitedStates[visitedCounter]:
						successorSet="N"
						break
				if successorSet=="N":
					continue
				if successorSet=="Y":
					break
		visitedStates.append(copy.deepcopy(successorValue))
		pathKey=" ".join([ " ".join([ str(col) for col in row ]) for row in successorValue])
		pathValue.append(pathTaken[pathKey])
		pathTaken.pop(pathKey)
		if is_goal(successorValue):
			print("Solution Found")
			print(printable_board(successorValue))
			print(" ".join([ str(row) for row in pathValue]))
			exit(1)
		if not any(priorityQueue):
			return False

#Function to check if the board is solvable
#To understand if a 15-board puzzle is solvable used the website - http://www.geeksforgeeks.org/check-instance-15-puzzle-solvable/
#To understand permutation inversion of the solvable check referenced website - https://www.cs.bham.ac.uk/~mdr/teaching/modules04/java2/TilesSolvability.html
def isSolvabe(initialBoard, indexPos):
	xPos=indexPos[0]
	yPos=indexPos[1]
	boardList=[int (i) for i in (' '.join([ ' '.join([ str(col) for col in row ]) for row in initialBoard])).split()]
	inversionNumber=0
	inversionNumber=0
	for i in range(0, len(boardList),1):
		if boardList[i] == 0:
			continue
		inversionNumber=inversionNumber+(boardList[i]-1)
		for j in range(i-1, -1, -1):
			if boardList[j] == 0:
				continue
			if (boardList[j]<boardList[i]) and (boardList[i] != 0 and boardList[j] != 0) :
				inversionNumber-=1
	if (((xPos+1)%2)-1) == 0:
		if (inversionNumber%2)!=0:
			solvable='Y'
		else:
			solvable='N'
	else:
		if (inversionNumber%2)==0:
			solvable='Y'
		else:
			solvable='N'
	return solvable

#Function to check if the board is in goal state
def is_goal(board):
	if board == [[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,0]]:
		return True
	else:
		return False

#Initialize the board
initialBoard=[]
pathValue=[]
#Read the file name containing the board configuartion as an input from user
#fileName = raw_input("Enter the file name of 15 board to start : ")
fileName = sys.argv[1]
with open(fileName,'r') as sourcein:
	for sourceLine in sourcein:
		initialBoard.append(sourceLine.strip().split())

initial_board=[[int(col) for col in row] for row in initialBoard]
priorityQueue={}
pathTaken={}
visitedStates=[copy.deepcopy(initial_board)]
print ("Starting from initial board:\n" + printable_board(initial_board))
indexOfZero=findEmptyPos(initial_board)
solvableFlag=isSolvabe(initial_board,indexOfZero[0])
#Check if the board is solvable if yes, begin solving the board
if solvableFlag == 'Y':
	if is_goal(initial_board):
		print("Solution Found")
		print(printable_board(initial_board))
		print("Initial board is goal state")
		exit(1)
	solve(initial_board)
else:
	print("The board cannot be solved!! Bubbye")