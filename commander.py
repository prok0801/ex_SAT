from pysat.formula import CNF
from pysat.solvers import Solver

new_variables_count = 0

def var(i, j, n):
    return i * n + j + 1

def generate_new_variables(length):
    global new_variables_count
    start = new_variables_count + 1
    new_variables_count += length
    return [i for i in range(start, start + length)]

def at_most_k(cnf, variables, k):
    if k >= len(variables):
        return

    if k == 1:
        at_most_one(cnf, variables)
        return

    chunk_size = k + 1
    groups = [variables[i:i + chunk_size] for i in range(0, len(variables), chunk_size)]
    
    commanders = []
    for group in groups:
        if len(group) > 1:
            commander = generate_new_variables(1)[0]
            commanders.append(commander)
            for var in group:
                cnf.append([-var, commander])
            at_most_one(cnf, group)
    

    at_most_k(cnf, commanders, k)

def at_most_one(cnf, variables):
    for i in range(len(variables)):
        for j in range(i + 1, len(variables)):
            cnf.append([-variables[i], -variables[j]])

def exactly_one(cnf, variables):
    cnf.append(variables)
    at_most_one(cnf, variables)

def generate_clauses(n):
    cnf = CNF()

    for i in range(n):
        row_vars = [var(i, j, n) for j in range(n)]
        exactly_one(cnf, row_vars)

    for j in range(n):
        col_vars = [var(i, j, n) for i in range(n)]
        exactly_one(cnf, col_vars)

    for d in range(2 * n - 1):
        main_diag_vars = [var(i, d - i, n) for i in range(n) if 0 <= d - i < n]
        at_most_one(cnf, main_diag_vars)

    for d in range(2 * n - 1):
        anti_diag_vars = [var(i, i - d + n - 1, n) for i in range(n) if 0 <= i - d + n - 1 < n]
        at_most_one(cnf, anti_diag_vars)

    return cnf

def solve_n_queens(n):
    cnf = generate_clauses(n)

    with Solver(bootstrap_with=cnf) as solver:
        if solver.solve():
            model = solver.get_model()
            solution = []
            for i in range(n):
                row = ['.'] * n
                for j in range(n):
                    if var(i, j, n) in model:
                        row[j] = 'Q'
                solution.append(' '.join(row))
            return solution
        else:
            return None

def print_solution(solution):
    if solution is None:
        print("No solution found.")
    else:
        for row in solution:
            print(row)

if __name__ == "__main__":
    n = 8
    solution = solve_n_queens(n)
    print_solution(solution)
