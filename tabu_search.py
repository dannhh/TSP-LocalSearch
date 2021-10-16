import csv
import math
import time
from random import randint
from random import shuffle

data = []
lines = 0 #số thành phố

def read_data(path):
    global lines
    with open(path, "r") as f:
        source = csv.reader(f)
        for line in source:
            if line != "":
                data.append(list((line)))
                lines += 1
            else:
                break
    return

def getNeighborhood(state):
    return two_opt_swap(state)

def two_opt_swap(state):
    global neighborhoodSize
    neighbors = []

    for i in range(neighborhoodSize):
        node1 = 0
        node2 = 0
        
        while node1 == node2 or node1 == start_node or node2 == start_node:
            node1 = randint(1, len(state)-1)
            node2 = randint(1, len(state)-1)

        if node1 > node2:
            tmp = node1
            node1 = node2
            node2 = tmp

        temp = state[node1:node2]
        tempState = state[:node1] + temp[::-1] + state[node2:]
        neighbors.append(tempState)
    return neighbors

def fitness(state):
    cost = 0
    for i in range(lines):
        dist = int(data[state[i]][state[i+1]])
        if dist == trackless:
            return trackless
        else:
            cost += dist
    return cost

def tabu_search(path):
    read_data(path)
    #Khởi tạo lời giải ban đầu ngẫu nhiên
    s0 = list(range(lines))
    shuffle(s0)

    if int(s0[0]) != start_node:
        for i in range(len(s0)):
            if  int(s0[i]) == start_node:
                swap = s0[0]
                s0[0] = s0[i]
                s0[i] = swap
                break
    s0.append(start_node)

    sBest = s0              #lời giải tốt nhất
    cBest = fitness(sBest)  #chi phí của lời giải tốt nhất
    bestCandidate = s0      #ứng cử viên sáng giá
    tabuList = []
    tabuList.append(s0)
    stop = False            #điều kiện dừng
    bestCandidate_turn = 0  #Số vòng lặp cho một bestCandidate

    while not stop:
        sNeighborhood = getNeighborhood(bestCandidate)  #danh sách các lời giải ở vùng lân cận từ ứng cử viên
        bestCandidate = sNeighborhood[0]
        for sCandidate in sNeighborhood:
            if (sCandidate not in tabuList) and (fitness(sCandidate) < fitness(bestCandidate)):
                bestCandidate = sCandidate

        if(fitness(bestCandidate) < cBest):
            sBest = bestCandidate
            cBest = fitness(sBest)
            bestCandidate_turn = 0 
            
        tabuList.append(bestCandidate)

        if(len(tabuList) > maxTabuSize):
            tabuList.pop(0)

        if(bestCandidate_turn == stoppingTurn):
            stop = True
        
        bestCandidate_turn += 1
        #print(tabuList)
    return sBest, cBest

start_node = 0
maxTabuSize = 1000
neighborhoodSize = 400
stoppingTurn = 20
max_fitness = 0

trackless = 999999999

start_time = time.time()
sPath, cPath = tabu_search("att48_d.csv")
exec_time =  time.time() - start_time

print("time: ", exec_time,"seconds")
print("tour cost: ",cPath)
print("tour: ", sPath)
