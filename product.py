from pysat.solvers import Solver
from math import sqrt

def var(i, j, n):
    return i * n + j + 1

def at_most_one(vars, solver):
    for i in range(len(vars)):
        for j in range(i + 1, len(vars)):
            solver.add_clause([-vars[i], -vars[j]])

def n_queens(n):
    solver = Solver()
    
    for i in range(n):
        row_vars = [var(i, j, n) for j in range(n)]
        solver.add_clause(row_vars) 
        at_most_one(row_vars, solver) 

    for j in range(n):
        col_vars = [var(i, j, n) for i in range(n)]
        solver.add_clause(col_vars)  
        at_most_one(col_vars, solver) 

    for d in range(-n + 1, n):
        diag1_vars = [var(i, i - d, n) for i in range(n) if 0 <= i - d < n]
        if len(diag1_vars) > 1:
            at_most_one(diag1_vars, solver)

    for d in range(2 * n - 1):
        diag2_vars = [var(i, d - i, n) for i in range(n) if 0 <= d - i < n]
        if len(diag2_vars) > 1:
            at_most_one(diag2_vars, solver)

    if solver.solve():
        model = solver.get_model()
        solution = []
        for i in range(n):
            for j in range(n):
                if model[var(i, j, n) - 1] > 0:
                    solution.append((i, j))
        solver.delete()
        return solution
    else:
        solver.delete()
        return None

if __name__ == "__main__":
    n = 8 
    solution = n_queens(n)
    
    if solution:
        print(f"Solution for {n}-Queens:")
        board = [["." for _ in range(n)] for _ in range(n)]
        for (i, j) in solution:
            board[i][j] = "Q"
        for row in board:
            print(" ".join(row))
    else:
        print(f"No solution found for {n}-Queens")
