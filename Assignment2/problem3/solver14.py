import heapq as fringe

list = []
initial_board = [[1,2,3],[4,5,6],[7,8,9],'R12']
initial_board1 = [[['1', '2', '3', '4'], ['5', '6', '7', '8'], ['9', '0', '10', '12'], ['13', '14', '15', '11']], 'R00']
# l1 =  [4, [[['1', '2', '3', '4'], ['5', '0', '7', '8'], ['9', '6', '10', '12'], ['13', '14', '15', '11']], 'R00', 'D13']]

fringe.heappush(list, [1, initial_board])
fringe.heappush(list, [2, initial_board])
fringe.heappush(list, [3, initial_board])

print fringe.heappop(list)

try:
    fringe.heappop(list)
except:
    print 'hi'

print float(2)/3