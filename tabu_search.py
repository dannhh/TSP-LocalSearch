import numpy as np
import time
from random import shuffle
import random
from enum import Enum
from itertools import cycle, dropwhile, islice

graph = []
lines = 0  #số thành phố

def cost(graph, route):
    cost = 0
    for i in range(0, len(graph)-1):
        cost += graph[route[i]][route[i + 1]]
    cost += graph[route[len(graph) - 1]][route[0]]
    return cost

# Two-opt function to create neighbors by swapping 2 edges
def two_opt(route):
    neighbors = [] 
    list = [] # list of distince random tuples
    count = 0
    while count != neighborhoodSize:
        i = random.randrange(1, len(route) - 2, 1)
        j = random.randrange(i + 1, len(route) - 1, 1)

        # check whether the list has already contained (i,j)
        if ([i, j]) not in list:
            list.append([i, j])
            count += 1
            
    # for each tuple (i, j), create new route and append to neighbors list 
    for (i, j) in list:
        temp = route[i:j + 1]
        temp.reverse()
        neighbor = route[:i] + temp + route[j + 1:]
        neighbors.append(neighbor)

    return neighbors

class OptCase(Enum):
    opt_case_1 = "opt_case_1"
    opt_case_2 = "opt_case_2"
    opt_case_3 = "opt_case_3"
    opt_case_4 = "opt_case_4"
    opt_case_5 = "opt_case_5"
    opt_case_6 = "opt_case_6"
    opt_case_7 = "opt_case_7"
    opt_case_8 = "opt_case_8"

# Three-opt function to create neighbors by swapping 3 edges
def three_opt(graph, route):
    # list of neighbor
    neighbor = []
    # dict to save value of each case
    moves_cost = {OptCase.opt_case_1: 0, OptCase.opt_case_2: 0, OptCase.opt_case_3: 0, OptCase.opt_case_4: 0, OptCase.opt_case_5: 0, OptCase.opt_case_6: 0, OptCase.opt_case_7: 0, OptCase.opt_case_8: 0}
    improved = True
    # route that has the best value
    best_found_route = route
    while improved:
        improved = False
        for (i, j, k) in possible_segments(len(graph)):
            # we check all the possible moves and save the result into the dict
            for opt_case in OptCase:
                moves_cost[opt_case] = get_cost_change(graph, best_found_route, opt_case, i, j, k)
            # we need the minimum value of substraction of old route - new route
            best_return = max(moves_cost, key=moves_cost.get)
            
            # the current best is better than the past
            if moves_cost[best_return] > 0:
                best_found_route = reverse_segments(best_found_route, best_return, i, j, k)

                # start with the same node -> we need to cycle the results.
                inf_cycle = cycle(best_found_route)
                drop_at_cond = dropwhile(lambda x: x != 0, inf_cycle)
                slice_route = islice(drop_at_cond, None, len(best_found_route))
                best_found_route = list(slice_route)
                # add to neighbor list
                neighbor.append(best_found_route)
                improved = True
                break
    # start with the same node -> we need to cycle the results.
    inf_cycle = cycle(best_found_route)
    drop_at_cond = dropwhile(lambda x: x != 0, inf_cycle)
    slice_route = islice(drop_at_cond, None, len(best_found_route))
    best_found_route = list(slice_route)
    neighbor.append(best_found_route)
    return neighbor


def possible_segments(N):
    """ Generate the combination of segments """
    segments = []
    count = 0
    while count != neighborhoodSize / 2:
        i = random.randrange(0, N - 4, 1)
        j = random.randrange(i + 2, N - 2, 1)
        k = random.randrange(j + 2, N, 1)
        # if tuple already in segment, generate the other
        if (i, j, k) not in segments:
            segments.append((i, j, k))
            count += 1

    return segments

def get_cost_change(graph, route, case, i, j, k):
    """ Compare current solution with 7 possible 3-opt moves"""
    if (i - 1) < (k % len(route)):
        first_segment = route[k% len(route):] + route[:i]
    else:
        first_segment = route[k % len(route):i]
    second_segment = route[i:j]
    third_segment = route[j:k]

    current_cost = cost(graph, route)
    if case == OptCase.opt_case_1:
        # first case is the current solution ABC
        return 0
    elif case == OptCase.opt_case_2:
        # second case is the case A'BC
        solution = list(reversed(first_segment)) + second_segment + third_segment
        new_cost = cost(graph, solution)
        return current_cost - new_cost
    elif case == OptCase.opt_case_3:
        # ABC'
        solution = first_segment + second_segment + list(reversed(third_segment))
        new_cost = cost(graph, solution)
        return current_cost - new_cost
    elif case == OptCase.opt_case_4:
        # A'BC'
        solution = list(reversed(first_segment)) + second_segment + list(reversed(third_segment))
        new_cost = cost(graph, solution)
        return current_cost - new_cost
    elif case == OptCase.opt_case_5:
        # A'B'C
        solution = list(reversed(first_segment)) + list(reversed(second_segment)) + third_segment
        new_cost = cost(graph, solution)
        return current_cost - new_cost
    elif case == OptCase.opt_case_6:
        # AB'C
        solution = first_segment + list(reversed(second_segment)) + third_segment
        new_cost = cost(graph, solution)
        return current_cost - new_cost
    elif case == OptCase.opt_case_7:
        # AB'C'
        solution = first_segment + list(reversed(second_segment)) + list(reversed(third_segment))
        new_cost = cost(graph, solution)
        return current_cost - new_cost
    elif case == OptCase.opt_case_8:
        # A'B'C
        solution = list(reversed(first_segment)) + list(reversed(second_segment)) + list(reversed(third_segment))
        new_cost = cost(graph, solution)
        return current_cost - new_cost

def reverse_segments(route, case, i, j, k):
    if (i - 1) < (k % len(route)):
        first_segment = route[k % len(route):] + route[:i]
    else:
        first_segment = route[k % len(route):i]
    second_segment = route[i:j]
    third_segment = route[j:k]

    solution = route
    if case == OptCase.opt_case_1:
        # first case is the current solution ABC
        pass
    elif case == OptCase.opt_case_2:
        # A'BC
        solution = list(reversed(first_segment)) + second_segment + third_segment
    elif case == OptCase.opt_case_3:
        # ABC'
        solution = first_segment + second_segment + list(reversed(third_segment))
    elif case == OptCase.opt_case_4:
        # A'BC'
        solution = list(reversed(first_segment)) + second_segment + list(reversed(third_segment))
    elif case == OptCase.opt_case_5:
        # A'B'C
        solution = list(reversed(first_segment)) + list(reversed(second_segment)) + third_segment
    elif case == OptCase.opt_case_6:
        # AB'C
        solution = first_segment + list(reversed(second_segment)) + third_segment
    elif case == OptCase.opt_case_7:
        # AB'C'
        solution = first_segment + list(reversed(second_segment)) + list(reversed(third_segment))
    elif case == OptCase.opt_case_8:
        # A'B'C
        solution = list(reversed(first_segment)) + list(reversed(second_segment)) + list(reversed(third_segment))
    return solution


def getNeighborhood(graph, state):
    #return two_opt(state)
    return three_opt(graph, state)


def tabu_search(path):
    graph = np.loadtxt(path, delimiter=",")
    #Khởi tạo lời giải ban đầu ngẫu nhiên
    lines = len(graph)
    s0 = list(range(1, lines))
    # start node always node 0
    shuffle(s0)
    s0 = [0] + s0
    
    sBest = s0  #lời giải tốt nhất
    cBest = cost(graph, sBest)  #chi phí của lời giải tốt nhất
    bestCandidate = s0  #ứng cử viên sáng giá
    tabuList = []
    tabuList.append(s0)
    stop = False  #điều kiện dừng
    bestCandidate_turn = 0  #Số vòng lặp cho một bestCandidate

    while not stop:
        sNeighborhood = getNeighborhood(graph, bestCandidate)  #danh sách các lời giải ở vùng lân cận từ ứng cử viên
        bestCandidate = sNeighborhood[0]
        for sCandidate in sNeighborhood:
            if (sCandidate not in tabuList) and (cost(graph, sCandidate) < cost(graph, bestCandidate)):
                bestCandidate = sCandidate

        if (cost(graph, bestCandidate) < cBest):
            sBest = bestCandidate
            cBest = cost(graph, sBest)
            bestCandidate_turn = 0

        tabuList.append(bestCandidate)

        if (len(tabuList) > maxTabuSize):
            tabuList.pop(0)

        if (bestCandidate_turn == stoppingTurn):
            stop = True

        bestCandidate_turn += 1
        # print(tabuList)
    sBest.append(s0[0])
    return sBest, cBest


start_node = 0
maxTabuSize = 1000
neighborhoodSize = 100
stoppingTurn = 200

start_time = time.time()
sPath, cPath = tabu_search("att48_d.csv")
exec_time = time.time() - start_time

print("time: ", exec_time, "seconds")
print("tour cost: ", cPath)
print("tour: ", sPath)
