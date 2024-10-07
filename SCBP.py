from typing import List
from pysat.solvers import Glucose3

id_variable = 0
sat_solver = Glucose3()

def pos_i(i, k, weight):
    return min(k, sum(weight[1:i+1]) if i < k else k)

def plus_clause(clause):

    sat_solver.add_clause(clause)
    print("Clause added:", clause)

def exactly_k(vars: List[int], weight: List[int], k):
    global id_variable
    n = len(vars) - 1
    id_variable = n

    map_register = [[0] * (k + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for j in range(1, pos_i(i, k, weight) + 1):
            id_variable += 1
            map_register[i][j] = id_variable

    for i in range(1, n + 1):
        for j in range(1, weight[i] + 1):
            if j <= pos_i(i, k, weight):
                plus_clause([-vars[i], map_register[i][j]])

    for i in range(2, n + 1):
        for j in range(1, pos_i(i - 1, k, weight) + 1):
            plus_clause([-map_register[i - 1][j], map_register[i][j]])

    for i in range(2, n + 1):
        for j in range(1, pos_i(i - 1, k, weight) + 1):
            if (j + weight[i]) <= k:
                plus_clause([-vars[i], -map_register[i - 1][j], map_register[i][j + weight[i]]])

    for i in range(1, n + 1):
        for j in range(pos_i(i - 1, k, weight) + 1, pos_i(i, k, weight) + 1):
            plus_clause([vars[i], -map_register[i][j]])

    if k > pos_i(n - 1, k, weight) and (k - weight[n] > 0):
        plus_clause([vars[n], map_register[n - 1][k - weight[n]]])
    else:
        plus_clause([map_register[n - 1][k], vars[n]])

    for i in range(2, n + 1):
        if k + 1 - weight[i] > 0 and k + 1 - weight[i] <= pos_i(i - 1, k, weight):
            plus_clause([-vars[i], -map_register[i - 1][k + 1 - weight[i]]])

    return n

def print_solution(n):
    print(f"Number of clauses: {sat_solver.nof_clauses()}")
    if sat_solver.solve():
        solution = sat_solver.get_model()
        if solution:
            print(f"Solution found: {solution}")
            for i in range(1, n + 1):
                print(f"X{i} = {int(solution[i - 1] > 0)}")
        else:
            print("No valid solution found.")
    else:
        print("UNSAT")

# Example usage: 5X1 + 3X2 + 7X3 + 4X4 + 6X5 + 2X6 = 15
n = exactly_k([0, 1, 2, 3, 4, 5, 6], [0, 5, 3, 7, 4, 6, 2], 15)
print_solution(n)
