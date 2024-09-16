from pysat.formula import CNF
from pysat.solvers import Solver

def var(i, j, n):
    return i * n + j + 1

def add_at_most_one_product(cnf, variables):
    for i in range(len(variables) - 1):
        for j in range(i + 1, len(variables)):
            cnf.append([-variables[i], -variables[j]])

def add_exactly_one(cnf, variables):
    cnf.append(variables)
    add_at_most_one_product(cnf, variables)

def generate_clauses(n):
    cnf = CNF()

    for i in range(n):
        row_vars = [var(i, j, n) for j in range(n)]
        col_vars = [var(j, i, n) for j in range(n)]
        add_exactly_one(cnf, row_vars) 
        add_exactly_one(cnf, col_vars)  

    for d in range(2 * n - 1):
        main_diag_vars = [var(i, d - i, n) for i in range(n) if 0 <= d - i < n]
        anti_diag_vars = [var(i, i - d + n - 1, n) for i in range(n) if 0 <= i - d + n - 1 < n]
        add_at_most_one_product(cnf, main_diag_vars)
        add_at_most_one_product(cnf, anti_diag_vars)

    return cnf

def solve_n_queens(n):
    cnf = generate_clauses(n)

    with Solver(bootstrap_with=cnf) as solver:
        if solver.solve():
            model = solver.get_model()
            return format_solution(model, n)
        return None

def format_solution(model, n):
    board = [['.'] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if var(i, j, n) in model:
                board[i][j] = 'Q'
    return [' '.join(row) for row in board]

def print_solution(solution):
    if solution:
        for row in solution:
            print(row)
    else:
        print("No solution found.")

if __name__ == "__main__":
    n = 8 
    solution = solve_n_queens(n)
    print_solution(solution)
