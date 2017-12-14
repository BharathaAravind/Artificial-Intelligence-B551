Algorithm:
----------
(1) Get the input file name from user and build the initial_board
(2) Set Goal_State
(3) Check if the board is solvable
	(a) If YES, then
		(i) If initial_board is Goal_State, then
			Print Solution Found
			EXIT
		(ii) Get a list of Up, Down, Left and Right Successors along with thier hueristic value
		(iii) Build a priority_queue with the hueristics and their successValue
		(iv) Based on minimum_value of the priority_queue pop the top-most element as Successor'
		(v) If the Successor' is already visited, pop the element from the queue and get the next Successor'
		(vi) If it is goal state, print the path traversed and the final board solution
		(vii) If it is NOT goal state, repeat from step (ii)
	(b) If NO, then EXIT

Test Cases:
-----------
https://scratch.mit.edu/projects/25647095/
Used the bove website to generate boards based on difficulty levels to check if they can be solved and the run time and the path taken to solve the board.
Files used for testing is also uploaded to Git with file names from 15BoardIn0.txt to 15BoardIn21.txt.

References:
-----------
To understand the list of hueristics that can be used and the way the work used the below website - http://www.brian-borowski.com/software/puzzle/ & http://kociemba.org/fifteen/fifteensolver.html
To understand if a 15-board puzzle is solvable used the website - http://www.geeksforgeeks.org/check-instance-15-puzzle-solvable/
To understand permutation inversion of the solvable check referenced website - https://www.cs.bham.ac.uk/~mdr/teaching/modules04/java2/TilesSolvability.html
To understand implementation of Manhattan Puzzle used reference - https://stackoverflow.com/questions/8224470/calculating-manhattan-distance