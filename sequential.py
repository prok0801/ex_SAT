from pysat.formula import CNF
from pysat.solvers import Solver

# Global variable for counting auxiliary variables
new_variables_count = 0

def var(i, j, n):
    return i * n + j + 1

def generate_new_variables(length, n):
    global new_variables_count
    start = n ** 2 + new_variables_count
    new_variables_count += length
    return [i for i in range(start + 1, start + length + 1)]

def sequential_at_most_one(cnf, variables, n):
    if len(variables) < 2:
        return

    new_variables = generate_new_variables(len(variables) - 1, n)

    cnf.append([-variables[0], new_variables[0]])
    for i in range(1, len(variables) - 1):
        cnf.append([-variables[i], new_variables[i]])
        cnf.append([-new_variables[i - 1], new_variables[i]])
        cnf.append([-new_variables[i - 1], -variables[i]])
    cnf.append([-variables[-1], -new_variables[-1]])

def exactly_one(cnf, variables, n):
    cnf.append(variables)
    sequential_at_most_one(cnf, variables, n)

def generate_clauses(n):
    cnf = CNF()

    for i in range(n):
        row_vars = [var(i, j, n) for j in range(n)]
        exactly_one(cnf, row_vars, n)

    for j in range(n):
        col_vars = [var(i, j, n) for i in range(n)]
        exactly_one(cnf, col_vars, n)

    for d in range(2 * n - 1):
        main_diag_vars = [var(i, d - i, n) for i in range(n) if 0 <= d - i < n]
        sequential_at_most_one(cnf, main_diag_vars, n)

    for d in range(2 * n - 1):
        anti_diag_vars = [var(i, i - d + n - 1, n) for i in range(n) if 0 <= i - d + n - 1 < n]
        sequential_at_most_one(cnf, anti_diag_vars, n)

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
