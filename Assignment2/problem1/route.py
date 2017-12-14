#!/usr/bin/env python
import sys
import math
from Queue import PriorityQueue

'''
To explore small portions graphs BFS and Uniform Cost Search (UCS)are optimal.
To explore large portions graphs A* gives the results but results may or may not be optimal 
DFS is not suitable for this kind of problem as it keeps exploring the graph.

Best Algorithm for each routing options:
A) Distance: 
    i)  For distance UCS gives the best route but takes a lot of time. 
    ii) BFS also gives the best route but takes a lot more time than Uniform Cost Search. They don't consider road segments or distance or time.
    iii)Astar will give the route taking a least amount of time but it may not be optimal. 
         If we are finding distances between a very long cities then Astar computes the route very quickly.
         The Heuristic function is distance between two nodes. 
    iv) DFS always gives the first found route between two cities which mostly is not optimal.

B) Segments:
    i) For road segments UCS gives the best route but takes a lot of time.
    ii) BFS and DFS don't consider road segments or distance or time.
    iii)For road segments Astar. I used to calculate the average road size of the all the US roads and 
        then divide the distance between current state and goak state and divide the road size to get approximate no.of segments.
        This heurisitc guesses the no.of edges required to reach goal.
    iv) This Heuristic may or may not give the optimal solution but can find solution faster than UCS as it explores less grpah space.

C) Time:
    i) For time I divide the distance by speed limit given. For road segments which don't have speed limit. I calculated average speed limit of all the road segments in US and use the mean value to fill the inconsistent data
    ii) BFS and DFS don't consider road segments or distance or time.
    iii)UCS gives shortest time taken to reach but takes a lot of time to reach goal state. In terms of code execution A* is optimal
    iv)For time Astar. divide the distance between current state and goal state and divide average speed limit.
        This heurisitc guesses the amount of time to be travelled.
    iv) This Heuristic may or may not give the optimal solution but can find solution faster than UCS as it explores less grpah space.

Best Algorithm in terms of computational time:
Astar is best in terms of computational time when the explored graph space is huge. UCS gives best route but it will take lot of time. 
This is because the graph to be explored is huge in UCS which is not in the case of A* which has to explore a small portion of graph.

Best Algorithm which takes least memory:
This would be DFS as it takes least amount of memory and the fringe containes only the explorations of one node completely at a time. But it mostly doesn't give optimal route.
I optimized the DFS by keeping track fo visited nodes.
BFS takes a lot memory to store all states so is not good memory wise
UCS takes less memory than BFS but in worst case both BFS and UCS takes Same space.
A* takes less space than BFS and UCS but in worst case can takes same space as BFS and UCS.

Heuristic Function:
For Distance: I took the distance between two points as my heuristic. For nodes which don't have gps coordinates I took its predecessor and find its distance to goal and then add the average road size to the distance.
For TIme: I took the average speed limit of all the US roads and divide the distance to be travelled by the avergae speed limit to get the minimum time.
            For routes which donot have speed limit I filled it with the averge speed limit of remaining routes.
For Segments: I took the average road size of all the US maps. Then divided the distance by avg road size to get the number of road segments to covered.  

Making Heuristic better:
I think I can make the heuristics better by having the gps locations of the junctions.
and also the speed limits of each junction.
When I compared my results with google maps I was getting a diff route than the maps suggested this is probably beacuse the google maps has a large dataset which even has the other roads(not only the highways)
I think by having a larger data set of all the roads may make the heuristic better in finding the optimal route.

Calculating distance between two gps coordinates:
I used haversine formula to calculate distance between two gps points. https://en.wikipedia.org/wiki/Haversine_formula


Refernces:
1) https://en.wikipedia.org/wiki/Haversine_formula
2) Found about haversine from https://stackoverflow.com/questions/27928/calculate-distance-between-two-latitude-longitude-points-haversine-formula
3) Canvas and lecture videos
4) Textbook Russel&Norvig-Artificial Intelligence A Modern Approach (3rd Edition)

'''

# put your routing program here!
routes = []
gpsCoordinates = []

#Reading the routes data into a list of lists with  each row being a route
def readingMapDataSets():
    with open('road-segments.txt') as inputfile:
        for line in inputfile:
            routes.append(line.strip().split(' '))

#Reading the GPS coordinates from city-gps file
def readingPlaceCoordinates():
    with open('city-gps.txt') as inputfile:
        for line in inputfile:
            gpsCoordinates.append(line.strip().split(' '))

#Finding X and Y coordinates for a city
def findXYCoordinate(city):
    for cities in gpsCoordinates:
        if city in cities:
            return cities
    return False

#This method is used to calculate distance between two GPS points in kms.
#It uses haversine formula to calculate the distance between points
#This code has been taken from https://stackoverflow.com/questions/4913349/haversine-formula-in-python-bearing-and-distance-between-two-gps-points

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])
    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    km = 6367 * c
    return km

#This computes distance between two points
#If a location is not present it the computes between its previous location and add the mean distance of a road segment for entire US map
def findXYDistance(place, goalCity):
    averageRoadSizeInUs = averageRoadSegments()
    distance = 0
    goalCityCoordinates = findXYCoordinate(goalCity)
    for tobeFoundCity in place[::-1]:
        for cities in gpsCoordinates:
            if tobeFoundCity in cities:
                distance = distance + haversine(float(cities[1]), float(cities[2]), float(goalCityCoordinates[1]), float(goalCityCoordinates[2]))
                return distance
        distance = distance + averageRoadSizeInUs
    #This mostly never returns because this loop tries to find the distance from the previously visited location to the goal and adds average road size in US
    # to the distance for evey previously visited state
    return 50

#This method calculates the average value of a road segment in US map in kms and it is used when a location is not found in city-gps.txt
#If a location is not present it the computes between its previous location and add this value to it.
def averageRoadSegments():
    totalDistance = 0
    for route in routes:
        totalDistance = totalDistance + int(route[2])
    averageRoad = float(totalDistance)/len(routes)
    return averageRoad * 1.6

#FInds the average speed limit of entire US map
#This is used to fill the irregular data and in the heuristic function
def averageSpeedLimit():
    totalSpeed = 0
    for route in routes:
        if(route[3] == '0' or route[3] == ''):
            totalSpeed = totalSpeed + 50
        else:
            totalSpeed = totalSpeed + int(route[3])
    averageSpeed = float(totalSpeed) / len(routes)
    return averageSpeed

#The heuistic function has three different cost functions
#for distance it returns the distance between two points in kms
#for segments it divided the to be travelled distnace by the total number of segments(ie. the length ofall road segments)
# for time is caluclates the time estimate by dividing the distance to be covered by the average speed limit in US.
def heuristicFunction(route):
    if(cost_function == 'distance'):
        return findXYDistance(route, goalCity)
    elif(cost_function == 'segments'):
        return findXYDistance(route, goalCity)/len(routes)
    elif(cost_function == 'time'):
        return findXYDistance(route, goalCity)/averageSpeedLimit()

#Finds Lists  ofRoutes for BFS and DFS Implementations
def findListOfRoutes(locationRoute):
    possibleRouteList = []
    location = locationRoute[len(locationRoute)-1]
    for route in routes:
        if location in route and (route[0] not in locationRoute or route[1] not in locationRoute):
            tempRoute = []
            if(route[0]!=location):
                tempRoute.append(route[2])
                if(route[3]=='0' or route[3]==0 or route[3] ==''):
                    tempRoute.append(float(route[2])/50)
                else:
                    tempRoute.append(float(route[2])/int(route[3]))
                tempRoute.append(route[4])
                tempRoute.append(route[0])
            else:
                tempRoute.append(route[2])
                if (route[3] == '0' or route[3] == 0 or route[3] == ''):
                    tempRoute.append(float(route[2]) / 50)
                else:
                    tempRoute.append(float(route[2]) / int(route[3]))
                tempRoute.append(route[4])
                tempRoute.append(route[1])
            possibleRouteList.append(tempRoute)
    return possibleRouteList


#Checks if the algorithm has reached goal state or not
def is_goal(s):
    if goalCity in s:
        return True


def findcost(route):
    #print route
    if(cost_function=='distance'):
        return route[0]
    elif(cost_function=='segments'):
        return route[2]
    elif(cost_function=='time'):
        return route[1]
    else:
        return route[0]

#Finds Lists  of Routes for Uniformed Cost Search and A* Implementations
# This fringe for UCS and A*has an additional field to store no.of segements travelled. So, I made a diff function
def findListOfRoutes_ucs(locationRoute):
    possibleRouteList = []
    location = locationRoute[len(locationRoute)-1]
    for route in routes:
        if location in route and (route[0] not in locationRoute or route[1] not in locationRoute):
            tempRoute = []
            if(route[0]!=location):
                tempRoute.append(route[2])
                if(route[3]=='0' or route[3]==0):
                    tempRoute.append(float(route[2])/50)
                else:
                    tempRoute.append(float(route[2])/int(route[3]))
                tempRoute.append('1')
                tempRoute.append(route[4])
                tempRoute.append(route[0])
            else:
                tempRoute.append(route[2])
                if (route[3] == '0' or route[3] == 0):
                    tempRoute.append(float(route[2]) / 50)
                else:
                    tempRoute.append(float(route[2]) / int(route[3]))
                tempRoute.append('1')
                tempRoute.append(route[4])
                tempRoute.append(route[1])
            possibleRouteList.append(tempRoute)
    return possibleRouteList


#Successor function for DFS and BFS.
def successors(route):
    connectedRoutes = []
    for nextRoute in findListOfRoutes(route):
        if(nextRoute[len(nextRoute)-1] not in visited_nodes):
            tempRoute = list(route)
            tempRoute[0] = int(tempRoute[0]) + int(nextRoute[0])
            tempRoute[1] = float(tempRoute[1]) + float(nextRoute [1])
            tempRoute[2] = tempRoute[2] +"->"+nextRoute[2]
            tempRoute.append(nextRoute[len(nextRoute)-1])
            connectedRoutes.append(tempRoute)
    return connectedRoutes

#Successor function for UCS.
def successors_ucs(routeWithEdgeCost):
    route = routeWithEdgeCost[1]
    connectedRoutes = []
    for nextRoute in findListOfRoutes_ucs(route):
        if (nextRoute[len(nextRoute) - 1] not in visited_nodes):
            tempRoute = list(route)
            tempRoute[0] = int(tempRoute[0]) + int(nextRoute[0])
            tempRoute[1] = float(tempRoute[1]) + float(nextRoute[1])
            tempRoute[2] = int(tempRoute[2]) + int(nextRoute[2])
            tempRoute[3] = tempRoute[3] + "->" + nextRoute[3]
            tempRoute.append(nextRoute[len(nextRoute) - 1])
            connectedRoutes.append(tempRoute)
    return connectedRoutes

#Successor function for A*.
def successors_Astar(routeWithHeuristic):
    route = routeWithHeuristic[1]
    connectedRoutes = []
    for nextRoute in findListOfRoutes_ucs(route):
        if (nextRoute[len(nextRoute) - 1] not in visited_nodes):
            tempRoute = list(route)
            tempRoute[0] = int(tempRoute[0]) + int(nextRoute[0])
            tempRoute[1] = float(tempRoute[1]) + float(nextRoute[1])
            tempRoute[2] = int(tempRoute[2]) + int(nextRoute[2])
            tempRoute[3] = tempRoute[3] + "->" + nextRoute[3]
            tempRoute.append(nextRoute[len(nextRoute) - 1])
            connectedRoutes.append(tempRoute)
    return connectedRoutes

#BFS Implementation
def findRoute_BFS():
    fringe = [['0','0','null', startCity]]
    while len(fringe) > 0:
        poppedEle = fringe.pop(0)
        visited_nodes.append(poppedEle[len(poppedEle)-1])
        for s in successors(poppedEle):
            if is_goal(s):
                return (s)
            fringe.append(s)
    return False

#DFS Implementation
def findRoute_DFS():
    fringe = [['0','0','null', startCity]]
    while len(fringe) > 0:
        poppedEle = fringe.pop()
        visited_nodes.append(poppedEle[len(poppedEle) - 1])
        for s in successors(poppedEle):
            if is_goal(s):
                return (s)
            fringe.append(s)
    return False

#uniform Cost Search
def findRoute_UCS():
    fringe = PriorityQueue()
    initial_pos = ['0', '0', '0', 'null', startCity]
    fringe.put((1, initial_pos))
    while fringe.qsize()>0:
        popped = fringe.get()
        visited_nodes.append(popped[1][len(popped[1])-1])
        for s in successors_ucs(popped):
            if is_goal(s):
                return s
            fringe.put((findcost(s),s))
    return False

#Astar algorithm Implementation
def findRoute_Astar():
    fringe = PriorityQueue()
    initial_pos = ['0', '0', '0', 'null', startCity]
    fringe.put((1, initial_pos))
    while fringe.qsize()>0:
        popped = fringe.get()
        visited_nodes.append(popped[1][len(popped[1])-1])
        for s in successors_Astar(popped):
            if is_goal(s):
                return s
            fringe.put((heuristicFunction(s),s))
    return False

def validatingInputLocation(place):
    for route in routes:
        if place in route:
            return True
    return False


readingMapDataSets()
readingPlaceCoordinates()
#startCity = 'Miami,_Florida'
#goalCity = 'San_Jose,_California'
startCity = sys.argv[1]
goalCity = sys.argv[2]
cost_function = sys.argv[4]
routing_algorithm = sys.argv[3]

#validating given inputs
if not (validatingInputLocation(startCity) and validatingInputLocation(goalCity)):
    print 'Invalid Start City or Goal city'
    exit()

if not (cost_function=='segments' or cost_function== 'distance' or cost_function == 'time'):
    print 'Invalid value for cost function'
    exit()

if not (routing_algorithm=='dfs' or routing_algorithm=='bfs' or routing_algorithm=='uniform' or routing_algorithm=='astar'):
    print 'Invalid value for routing algorithm'
    exit()

#To keep track of visited cities
visited_nodes = []
s1 = []
if(routing_algorithm=='dfs'):
    s1 = findRoute_DFS()
elif(routing_algorithm=='bfs'):
    s1 = findRoute_BFS()
elif(routing_algorithm=='uniform'):
    s1 = findRoute_UCS()
elif(routing_algorithm=='astar'):
    s1 = findRoute_Astar()

'''
Formatting the output
'''
#rounding the time taken
s1[1] = round(float(s1[1]),4)
#popping the no.of edges traversed and highway route taken
s1.pop(2)
if(routing_algorithm=='astar' or routing_algorithm == 'uniform'):
    s1.pop(2)
#Printing the output
print ' '.join(str(v) for v in s1)
