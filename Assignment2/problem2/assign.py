'''
Problem2 write Up:
Goal State:
    All students mapped to a group
Initial State:
    Empty Fringe with no students added
Successor Function:
    Adds a new group and finds all possible teams 1 mem, 2mem and three mem teams.

1) I have used Uniform Cost Search and selected a prority queue as my fringe
2) I select the one with least cost among the fringe and then explore its children and find thier costs.
3) I have Selected UniformCostSearch as it is a modification to BFS and its runtime to reach solution is faster than BFS.
4) I iniitially though of implementing the problem using BFS but with BFS I have to visit the entire graph and save all the solutions in a list
    and then find the optimal solution among.
5) With Uniform Cost Search I would be picking the Node with the least cost and then exploring it. It would take less steps to cover the entire graph.
6) I decide if I reach the goal if all the students are allocated to a group.
7) My successor function adds a new team every time with the remaining students and adds all the possibilities of the students like 1 person group,
    2person groups and 3 person groups and computes their costs and stores them in fringe.
8) The reason why I didn't chose Astar was I couldn't come up with a heuristic that can guess cost of the future teams. I felt a greedy algorithm like UCS could find the optimal route the fastest.
9) My cost functions uses the values 'k', 'm', 'n' and computes the costs based on their differences.
10) My initial fringe is an empty list with a uniform cost 1. My sucessir then adds the possible teams with the first student who gave prefernces.
11) Every state is a list of lists with each list being a team. ie [[<team1>],[team2],[team3]]
12) My fringe would be folding the above mentioned states with their costs as tuples.(1,[[team1],[team2],[team3]])

Refernces:
1) Canvas and lecture videos
2) Textbook Russel&Norvig-Artificial Intelligence A Modern Approach (3rd Edition)

'''

# put your group assignment problem here!
from Queue import PriorityQueue
import copy
import sys
prefernces = []
listOfStudents = []

#Reading the peferences of each student
def readingPrefernces(inputFileName):
    with open(inputFileName) as inputfile:
        for line in inputfile:
            tempList = line.strip().split(' ')
            prefernces.append(tempList)
            listOfStudents.append(tempList[0])

#Checking if the goal is reached or not. Checks if every student is in a group
def is_goal(s):
    goal = True
    listOfFinisedStudents = []
    for teams in s:
        for student in teams:
            listOfFinisedStudents.append(student)

    for student in listOfStudents:
        if student not in listOfFinisedStudents:
                return False
    return goal

#Add New team to given list every time
def addNewGroup(s):
    listOfGroups = copy.deepcopy(s[1])
    if(listOfGroups == []):
        listOfGroups.append([listOfStudents[0]])
    else:
        for student in listOfStudents:
            found = False
            for groups in listOfGroups:
                if student in groups:
                    found = True
                    break
            if found:
                continue
            else:
                listOfGroups.append([student])
                break

    return listOfGroups

#Gives all the possible list of groups ie., Single person group, 2 person and 3 person groups
def findPossibleTeamMembers(listOfGroups):
    groupToBeMade = listOfGroups[len(listOfGroups)-1]
    listOfUsedStudents = []
    for group in listOfGroups:
        for student in group:
            listOfUsedStudents.append(student)

    #Adding one team member
    listOfTwoPersonGroups = []
    for student in listOfStudents:
        if student not in listOfUsedStudents:
            tempList = [groupToBeMade[0], student]
            if(sorted(tempList) not in listOfTwoPersonGroups):
                listOfTwoPersonGroups.append(sorted(tempList))

    #Adding a third teammate to the list of two groups
    listOfThreePersonGroups = []
    for groups in listOfTwoPersonGroups:
        for student in listOfStudents:
            if student not in listOfUsedStudents and student not in groups:
                tempList = [groups[0],groups[1], student]
                if(sorted(tempList) not in listOfThreePersonGroups):
                    listOfThreePersonGroups.append(sorted(tempList))

    for groups in listOfTwoPersonGroups:
        listOfGroups.append(groups)

    for groups in listOfThreePersonGroups:
        listOfGroups.append(groups)

    return listOfGroups

# The successor function which adds a new group by calling addNewGroup
# Then adds all the possible groups to a list and returns it
def successors_ucs(s):
    listOfSuccessors = []
    listOfGroups = addNewGroup(s)
    possibleNewGroups = findPossibleTeamMembers(listOfGroups)
    for newgroups in possibleNewGroups:
        tempGroup = copy.deepcopy(s[1])
        if newgroups not in s[1]:
            tempGroup.append(newgroups)
            listOfSuccessors.append(tempGroup)

    return listOfSuccessors

#Gets the preferred Team size if student name is given
def findDesiredTeamSize(studentName):
    for prefernce in prefernces:
        if studentName == prefernce[0]:
            return int(prefernce[1])
    return 0

##Gets the preferred Team members as a list if student name is given
def findDesiredTeamMembers(studentName):
    for prefernce in prefernces:
        if studentName == prefernce[0]:
            c = 0
            if prefernce[2] == '_':
                return []
            else:
                list = prefernce[2].split(",")
                return list

#Gets the not preferred Team Members if student name is given
def findNotDesiredTeamMembers(studentName):
    for prefernce in prefernces:
        if studentName == prefernce[0]:
            c = 0
            if prefernce[3] == '_':
                return []
            else:
                list = prefernce[3].split(",")
                return list

#Finds the cost function of every state and return the number
def costFunction(s):
    totalCost = 0

    gradingCost = k * len(s)

    teamSizeComplaintCost = 0
    for student in listOfStudents:
        for teams in s:
            if student in teams:
                if len(teams)!= findDesiredTeamSize(student) and findDesiredTeamSize(student) != 0:
                    teamSizeComplaintCost = teamSizeComplaintCost + 1


    desiredTeamMemCompaintCost = 0
    for student in listOfStudents:
        costOfEachStudent = 0
        for teams in s:
            if student in teams:
                tempList = findDesiredTeamMembers(student)
                diff = 0
                if tempList == []:
                    diff = 0
                else:
                    # Subtract the templist with his team and multiply it desired team cost
                    diff = len(tempList) - len(set(tempList).intersection(teams))
                costOfEachStudent = diff * n
        desiredTeamMemCompaintCost = costOfEachStudent + desiredTeamMemCompaintCost

    notDesiredTeamComplaintCost = 0
    for student in listOfStudents:
        costOfEachStudent = 0
        for teams in s:
            if student in teams:
                tempList = findNotDesiredTeamMembers(student)
                # Subtract the templist with his team and multiply it desired team cost
                diff = 0
                if tempList == []:
                    diff = 0
                else:
                    # Subtract the templist with his team and multiply it desired team cost
                    diff = len(set(tempList).intersection(teams))
                costOfEachStudent = diff * m
        notDesiredTeamComplaintCost = costOfEachStudent + notDesiredTeamComplaintCost

    totalCost = gradingCost + teamSizeComplaintCost + desiredTeamMemCompaintCost + notDesiredTeamComplaintCost
    return totalCost

#The main search function.
def findSolution():
    fringe = PriorityQueue()
    initial_groups = []
    fringe.put((1, initial_groups))
    while fringe.qsize() > 0:
        popped = fringe.get()
        for s in successors_ucs(popped):
            if is_goal(s):
                return s
            fringe.put((costFunction(s), s))
    return False


inputFileName = sys.argv[1]
#Reading the input variables
k = int(sys.argv[2])
m = int(sys.argv[3])
n = int(sys.argv[4])
readingPrefernces(inputFileName)

solution = findSolution()
if solution == False:
    print 'Code broke!'
for team in solution:
    print (' ').join(team)
print costFunction(solution)
