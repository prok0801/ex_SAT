from pysat.formula import CNF
from pysat.solvers import Solver

def var(i, j, n):
    return i * n + j + 1

def binary_encoding(n):
    cnf = CNF()

    for i in range(n):
        row_vars = [var(i, j, n) for j in range(n)]
        cnf.append(row_vars)

        for j in range(n):
            for k in range(j + 1, n):
                cnf.append([-row_vars[j], -row_vars[k]])

    for j in range(n):
        column_vars = [var(i, j, n) for i in range(n)]
        cnf.append(column_vars)

        for i in range(n):
            for k in range(i + 1, n):
                cnf.append([-column_vars[i], -column_vars[k]])

    for d in range(-n + 1, n):
        main_diag_vars = [var(i, i - d, n) for i in range(n) if 0 <= i - d < n]
        for m in range(len(main_diag_vars)):
            for k in range(m + 1, len(main_diag_vars)):
                cnf.append([-main_diag_vars[m], -main_diag_vars[k]])

    for d in range(2 * n - 1):
        anti_diag_vars = [var(i, d - i, n) for i in range(n) if 0 <= d - i < n]
        for m in range(len(anti_diag_vars)):
            for k in range(m + 1, len(anti_diag_vars)):
                cnf.append([-anti_diag_vars[m], -anti_diag_vars[k]])

    return cnf

def solve_n_queens(n):
    cnf = binary_encoding(n)

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
