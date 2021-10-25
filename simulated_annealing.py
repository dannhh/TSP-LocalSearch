import numpy as np
import math
import random
from enum import Enum
from itertools import cycle, dropwhile, islice

#graph = np.loadtxt(r"C:\Users\Acer\Desktop\HK211\DAAI\TSP-LocalSearch\br17atsp.csv", delimiter=",")
# size = len(graph)
# coolingRate = 2
# graph = []

def totalLength(path):
    cost = graph[path[len(path) - 1]][path[0]]
    for i in range(0, (len(graph) - 1)):
        cost += graph[path[i]][path[i + 1]]
    return cost

class OptCase(Enum):
  opt_case_1 = "opt_case_1"
  opt_case_2 = "opt_case_2"
  opt_case_3 = "opt_case_3"
  opt_case_4 = "opt_case_4"
  opt_case_5 = "opt_case_5"
  opt_case_6 = "opt_case_6"
  opt_case_7 = "opt_case_7"
  opt_case_8 = "opt_case_8"

def two_opt(route):
    list = [] # list of distince random tuples
    count = 0
    while count != size:
        i = random.randrange(1, len(route) - 2, 1)
        j = random.randrange(i + 1, len(route) - 1, 1)

        # check whether the list has already contained (i,j)
        if ([i, j]) not in list:
            list.append([i, j])
            count += 1

    # for each tuple (i, j), create new route and append to neighbors list 
    best_neighbor_cost = math.inf
    best_neighbor_route = []
    for (i, j) in list:
        temp = route[i:j + 1]
        temp.reverse()
        neighbor = route[:i] + temp + route[j + 1:]
        new_cost = totalLength(neighbor)
        if new_cost < best_neighbor_cost:
          best_neighbor_cost = new_cost
          best_neighbor_route = neighbor

    return best_neighbor_route

def three_opt(route):
    # dict to save value of each case
    moves_cost = {OptCase.opt_case_1: 0, OptCase.opt_case_2: 0,
                  OptCase.opt_case_3: 0, OptCase.opt_case_4: 0, 
                  OptCase.opt_case_5: 0, OptCase.opt_case_6: 0, 
                  OptCase.opt_case_7: 0, OptCase.opt_case_8: 0}
                  
    improved = True
    # route that has the best value
    best_found_route = route
    
    while improved:
        improved = False
        for (i, j, k) in possible_segments(len(graph)):
            # we check all the possible moves and save the result into the dict
            for opt_case in OptCase:
                moves_cost[opt_case] = get_cost_change(best_found_route, opt_case, i, j, k)
            # we need the minimum value of substraction of old route - new route
            best_return = max(moves_cost, key = moves_cost.get)
            if moves_cost[best_return] > 0:
                best_found_route = reverse_segments(best_found_route, best_return, i, j, k)
                improved = True
                break

    # start with the same node -> we will need to cycle the results.
    inf_cycle = cycle(best_found_route)
    drop_at_cond = dropwhile(lambda x: x != 0, inf_cycle)
    slice_route = islice(drop_at_cond, None, len(best_found_route))
    best_found_route = list(slice_route)

    return best_found_route

def possible_segments(N):
    """ Generate the combination of segments """
    segments = []
    count = 0
    while count != size:
      i = random.randrange(0, N - 4, 1)
      j = random.randrange(i + 2, N - 2, 1)
      k = random.randrange(j + 2, N, 1)
      # if tuple already in segment, generate the other
      if (i,j,k) not in segments:
        segments.append((i,j,k))
        count += 1

    return segments

def get_cost_change(route, case, i, j, k):
    """ Compare current solution with 7 possible 3-opt moves"""
    if (i - 1) < (k % len(route)):
        first_segment = route[k% len(route):] + route[:i]
    else:
        first_segment = route[k % len(route):i]
    second_segment = route[i:j]
    third_segment = route[j:k]

    current_cost = totalLength(route)
    if case == OptCase.opt_case_1:
        # first case is the current solution ABC
        return 0
    elif case == OptCase.opt_case_2:
        # second case is the case A'BC
        solution = list(reversed(first_segment)) + second_segment + third_segment
        new_cost = totalLength(solution)
        return current_cost - new_cost
    elif case == OptCase.opt_case_3:
        # ABC'
        solution = first_segment + second_segment + list(reversed(third_segment))
        new_cost = totalLength(solution)
        return current_cost - new_cost
    elif case == OptCase.opt_case_4:
        # A'BC'
        solution = list(reversed(first_segment)) + second_segment + list(reversed(third_segment))
        new_cost = totalLength(solution)
        return current_cost - new_cost
    elif case == OptCase.opt_case_5:
        # A'B'C
        solution = list(reversed(first_segment)) + list(reversed(second_segment)) + third_segment
        new_cost = totalLength(solution)
        return current_cost - new_cost
    elif case == OptCase.opt_case_6:
        # AB'C
        solution = first_segment + list(reversed(second_segment)) + third_segment
        new_cost = totalLength(solution)
        return current_cost - new_cost
    elif case == OptCase.opt_case_7:
        # AB'C'
        solution = first_segment + list(reversed(second_segment)) + list(reversed(third_segment))
        new_cost = totalLength(solution)
        return current_cost - new_cost
    elif case == OptCase.opt_case_8:
        # A'B'C
        solution = list(reversed(first_segment)) + list(reversed(second_segment)) + list(reversed(third_segment))
        new_cost = totalLength(solution)
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
graph = []
size = 0
def solver(filename, opt):
    print(opt)
    global graph
    graph = np.loadtxt(filename, delimiter=",")
    # np.hstack((graph,graph2))
    print(graph)
    coolingRate = 0.9995
    global size
    size += len(graph)
    path = list(range(1, size))

    # Start node always 0
    random.shuffle(path)
    path = [0] + path
    
    currLength = totalLength(path)
    count = 0
    T = size * size
    threshold = math.sqrt(size)

    if opt == 2:
        while count < threshold and T > 0.0005:

            count += 1

            newPath = two_opt(path)
            # newPath = three_opt(path)
            newLength = totalLength(newPath)

            if newLength < currLength:
                path = newPath
                currLength = newLength
                count = 0
            else: 
                prob = math.exp(-(newLength - currLength)/T)

                if random.uniform(0, 1) <= prob:
                    path = newPath
                    currLength = newLength
                    count = 0

            T *= coolingRate
        # add the last node equal to start node to complete the route
        length = totalLength(path)
        path.append(0)
        return path, length
    
    if opt == 3:
        while count < threshold and T > 0.0005:

            count += 1

            # newPath = two_opt(path)
            newPath = three_opt(path)
            newLength = totalLength(newPath)

            if newLength < currLength:
                path = newPath
                currLength = newLength
                count = 0
            else: 
                prob = math.exp(-(newLength - currLength)/T)

                if random.uniform(0, 1) <= prob:
                    path = newPath
                    currLength = newLength
                    count = 0

            T *= coolingRate
        # add the last node equal to start node to complete the route
        length = totalLength(path)
        path.append(0)
        return path, length


# print(graph)
# res, length = solver(r"C:\Test_code\DoAn\br17atsp.csv", 2)
# print(res)
# print(length)
# path = solver()
# p = [1, 8, 38, 31, 44, 18, 7, 28, 6, 37, 19, 27, 17, 43, 30, 36, 46, 3, 20, 47, 21, 32, 39, 48, 5, 42, 24, 10, 45, 35, 4, 26, 2, 29, 34, 41, 16, 22, 3, 23, 14, 25, 13, 11, 12, 15, 40, 9]
# p = [x - 1 for x in p]
# print(totalLength(p))
# print(three_opt(p))
# print(totalLength(p))
