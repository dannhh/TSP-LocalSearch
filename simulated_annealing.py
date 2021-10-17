import numpy as np
import math
import random
from enum import Enum

graph = np.loadtxt('C:\Test_code\\att48_d.csv', delimiter=",")
size = len(graph)
coolingRate = 2

def totalLength(path):
    cost = graph[path[len(path) - 1]][path[0]]
    for i in range(0, (len(path) - 1)):
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

def three_opt(route):
    #if route is None:
    #    route = christofides_tsp(graph)
    moves_cost = {OptCase.opt_case_1: 0, OptCase.opt_case_2: 0,
                  OptCase.opt_case_3: 0, OptCase.opt_case_4: 0, 
                  OptCase.opt_case_5: 0, OptCase.opt_case_6: 0, 
                  OptCase.opt_case_7: 0, OptCase.opt_case_8: 0}
                  
    improved = True
    best_found_route = route
    
    while improved:
        improved = False
        for (i, j, k) in possible_segments(len(graph)):
            # we check all the possible moves and save the result into the dict
            for opt_case in OptCase:
                moves_cost[opt_case] = get_cost_change(graph, best_found_route, opt_case, i, j, k)
            # we need the minimum value of substraction of old route - new route
            best_return = max(moves_cost, key = moves_cost.get)
            if moves_cost[best_return] > 0:
                best_found_route = reverse_segments(best_found_route, best_return, i, j, k)
                improved = True
                break

    # just to start with the same node -> we will need to cycle the results.
    return best_found_route

def possible_segments(N):
    """ Generate the combination of segments """
    #segments = ((i, j, k) for i in range(N) for j in range(i + 2, N-1) for k in range(j + 2, N - 1 + (i > 0)))
    segments = []
    count = 0
    while count != size:
      i = random.randrange(1, N - 4, 1)
      j = random.randrange(i + 2, N - 2, 1)
      k = random.randrange(j + 2, N, 1)
      if (i,j,k) not in segments:
        segments.append((i,j,k))
        count += 1

    return segments

def get_cost_change(graph, route, case, i, j, k):
    """ Compare current solution with 7 possible 3-opt moves"""
    A, B, C, D, E, F = route[i - 1], route[i], route[j - 1], route[j], route[k - 1], route[k % len(route)]

    if case == OptCase.opt_case_1:
        # first case is the current solution ABC
        return 0

    elif case == OptCase.opt_case_2:
        # second case is the case A'BC
        return graph[A, B] + graph[E, F] - (graph[B, F] + graph[A, E])

    elif case == OptCase.opt_case_3:
        # ABC'
        return graph[C, D] + graph[E, F] - (graph[D, F] + graph[C, E])

    elif case == OptCase.opt_case_4:
        # A'BC'
        return graph[A, B] + graph[C, D] + graph[E, F] - (graph[A, D] + graph[B, F] + graph[E, C])

    elif case == OptCase.opt_case_5:
        # A'B'C
        return graph[A, B] + graph[C, D] + graph[E, F] - (graph[C, F] + graph[B, D] + graph[E, A])

    elif case == OptCase.opt_case_6:
        # AB'C
        return graph[B, A] + graph[D, C] - (graph[C, A] + graph[B, D])

    elif case == OptCase.opt_case_7:
        # AB'C'
        return graph[A, B] + graph[C, D] + graph[E, F] - (graph[B, E] + graph[D, F] + graph[C, A])

    elif case == OptCase.opt_case_8:
        # A'B'C
        return graph[A, B] + graph[C, D] + graph[E, F] - (graph[A, D] + graph[C, F] + graph[B, E])

def reverse_segments(route, case, i, j, k):
    zero_segment = []
    if (i - 1) < (k % len(route)):
        zero_segment.append(route[0])
        first_segment = route[k% len(route):] + route[1:i]
    else:
        first_segment = route[k % len(route):i]
    second_segment = route[i:j]
    third_segment = route[j:k]

    if case == OptCase.opt_case_1:
        # first case is the current solution ABC
        pass
    elif case == OptCase.opt_case_2:
        # A'BC
        solution = zero_segment +  list(reversed(first_segment)) + second_segment + third_segment
    elif case == OptCase.opt_case_3:
        # ABC'
        solution = zero_segment + first_segment + second_segment + list(reversed(third_segment))
    elif case == OptCase.opt_case_4:
        # A'BC'
        solution = zero_segment +  list(reversed(first_segment)) + second_segment + list(reversed(third_segment))
    elif case == OptCase.opt_case_5:
        # A'B'C
        solution = zero_segment +  list(reversed(first_segment)) + list(reversed(second_segment)) + third_segment
    elif case == OptCase.opt_case_6:
        # AB'C
        solution = zero_segment + first_segment + list(reversed(second_segment)) + third_segment
    elif case == OptCase.opt_case_7:
        # AB'C'
        solution = zero_segment + first_segment + list(reversed(second_segment)) + list(reversed(third_segment))
    elif case == OptCase.opt_case_8:
        # A'B'C
        solution = zero_segment + list(reversed(first_segment)) + list(reversed(second_segment)) + list(reversed(third_segment))
    return solution

def solver():
    path = list(range(0, size))
    random.shuffle(path)
    
    currLength = totalLength(path)
    count = 0
    T = size * size
    threshold = math.sqrt(2)

    while count < 10 and T > 0.0005:

        count += 1

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

        T /= 1.005
    return path

print(graph)
res = solver()
print(res)
print(totalLength(res))

# p = [1, 8, 38, 31, 44, 18, 7, 28, 6, 37, 19, 27, 17, 43, 30, 36, 46, 3, 20, 47, 21, 32, 39, 48, 5, 42, 24, 10, 45, 35, 4, 26, 2, 29, 34, 41, 16, 22, 3, 23, 14, 25, 13, 11, 12, 15, 40, 9]
# p = [x - 1 for x in p]
# print(totalLength(p))
# print(three_opt(p))
# print(totalLength(p))