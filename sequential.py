from pysat.formula import CNF
from pysat.solvers import Solver

def var(i, j, n):
    """Generate a unique variable index for the queen at (i, j)."""
    return i * n + j + 1

def sequential_at_most_one(cnf, variables):
    """Sequential encoding for at most one constraint."""
    n = len(variables)
    if n < 2:
        return
    aux_vars = [var(0, i + n + 1, n) for i in range(n - 1)]

    cnf.append([-variables[0], aux_vars[0]])
    for i in range(1, n - 1):
        cnf.append([-variables[i], aux_vars[i]])
        cnf.append([-aux_vars[i - 1], aux_vars[i]])
        cnf.append([-aux_vars[i - 1], -variables[i]])

    cnf.append([-variables[n - 1], -aux_vars[n - 2]])

def exactly_one(cnf, variables):
    """Ensure exactly one of the variables is true."""
    cnf.append(variables)
    sequential_at_most_one(cnf, variables)

def generate_clauses(n):
    """Generate CNF clauses for the N-Queens problem."""
    cnf = CNF()

    for i in range(n):
        row_vars = [var(i, j, n) for j in range(n)]
        col_vars = [var(j, i, n) for j in range(n)]
        exactly_one(cnf, row_vars)
        exactly_one(cnf, col_vars)

    for d in range(2 * n - 1):
        main_diag_vars = [var(i, d - i, n) for i in range(n) if 0 <= d - i < n]
        anti_diag_vars = [var(i, i - d + n - 1, n) for i in range(n) if 0 <= i - d + n - 1 < n]
        
        sequential_at_most_one(cnf, main_diag_vars)
        sequential_at_most_one(cnf, anti_diag_vars)

    return cnf

def solve_n_queens(n):
    """Solve the N-Queens problem using SAT solver."""
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

if __name__ == "__main__":
    n = 64
    solution = solve_n_queens(n)
    if solution:
        print(f"Solution for {n}-Queens (Optimized Sequential Encoding):")
        for row in solution:
            print(row)
    else:
        print(f"No solution exists for {n}-Queens.")
