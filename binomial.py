from pysat.formula import CNF
from pysat.solvers import Solver

def n_queens_binomial_optimized(n):
    cnf = CNF()

    def var(i, j):
        return i * n + j + 1

    # Constraint 1: Exactly one queen in each row
    for i in range(n):
        row_vars = [var(i, j) for j in range(n)]
        # At least one queen in each row
        cnf.append(row_vars)
        # At most one queen in each row using a more compact clause addition
        for j in range(n):
            for k in range(j + 1, n):
                cnf.append([-row_vars[j], -row_vars[k]])

    # Constraint 2: Exactly one queen in each column
    for j in range(n):
        col_vars = [var(i, j) for i in range(n)]
        # At least one queen in each column
        cnf.append(col_vars)
        # At most one queen in each column
        for i in range(n):
            for k in range(i + 1, n):
                cnf.append([-col_vars[i], -col_vars[k]])

    # Constraint 3: At most one queen on each main diagonal
    for d in range(-n + 1, n):
        diag1_vars = [var(i, i - d) for i in range(n) if 0 <= i - d < n]
        for i in range(len(diag1_vars)):
            for j in range(i + 1, len(diag1_vars)):
                cnf.append([-diag1_vars[i], -diag1_vars[j]])

    # Constraint 4: At most one queen on each anti-diagonal
    for d in range(2 * n - 1):
        diag2_vars = [var(i, d - i) for i in range(n) if 0 <= d - i < n]
        for i in range(len(diag2_vars)):
            for j in range(i + 1, len(diag2_vars)):
                cnf.append([-diag2_vars[i], -diag2_vars[j]])

    with Solver(bootstrap_with=cnf) as solver:
        if solver.solve():
            model = solver.get_model()
            solution = []
            for i in range(n):
                row = ['.'] * n
                for j in range(n):
                    if var(i, j) in model:
                        row[j] = 'Q'
                solution.append(' '.join(row))
            return solution
        else:
            return None

if __name__ == "__main__":
    n = 8 
    solution = n_queens_binomial_optimized(n)
    if solution:
        print(f"Solution for {n}-Queens (Optimized Binomial Encoding):")
        for row in solution:
            print(row)
    else:
        print(f"No solution exists for {n}-Queens.")
