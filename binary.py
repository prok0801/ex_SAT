from pysat.formula import CNF
from pysat.solvers import Solver

def var(i, j, n):
    return i * n + j + 1

def binary_encoding(n):
    cnf = CNF()
    binary_vars = []

    num_binary_vars = n.bit_length()  # log2(n)

    for i in range(n):
        binary_vars.append([var(i, j, n) for j in range(n)])

    for i in range(n):
        cnf.append(binary_vars[i])

    for row in binary_vars:
        for j in range(len(row)):
            for k in range(j + 1, len(row)):
                cnf.append([-row[j], -row[k]])

    for j in range(n):
        column_vars = [var(i, j, n) for i in range(n)]
        cnf.append(column_vars) 
        for x in range(len(column_vars)):
            for y in range(x + 1, len(column_vars)):
                cnf.append([-column_vars[x], -column_vars[y]])  

    for d in range(2 * n - 1):
        main_diag_vars = [var(i, d - i, n) for i in range(n) if 0 <= d - i < n]
        anti_diag_vars = [var(i, i - d + n - 1, n) for i in range(n) if 0 <= i - d + n - 1 < n]

        for m in range(len(main_diag_vars)):
            for n in range(m + 1, len(main_diag_vars)):
                cnf.append([-main_diag_vars[m], -main_diag_vars[n]])

        for m in range(len(anti_diag_vars)):
            for n in range(m + 1, len(anti_diag_vars)):
                cnf.append([-anti_diag_vars[m], -anti_diag_vars[n]])

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
