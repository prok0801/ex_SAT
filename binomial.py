from pysat.formula import CNF
from pysat.solvers import Solver

def n_queens_binomial(n):
    # Initialize the CNF formula
    cnf = CNF()

    # Function to calculate a unique variable index for the queen at (i, j)
    def var(i, j):
        return i * n + j + 1

    # Constraint 1: Each row has exactly one queen
    for i in range(n):
        # Each row has at least one queen
        cnf.append([var(i, j) for j in range(n)])

        # Each row has at most one queen (no two queens in the same row)
        for j in range(n):
            for k in range(j + 1, n):
                cnf.append([-var(i, j), -var(i, k)])

    # Constraint 2: Each column has exactly one queen
    for j in range(n):
        # Each column has at least one queen
        cnf.append([var(i, j) for i in range(n)])

        # Each column has at most one queen (no two queens in the same column)
        for i in range(n):
            for k in range(i + 1, n):
                cnf.append([-var(i, j), -var(k, j)])

    # Constraint 3: No two queens on the same main diagonal
    for d in range(2 * n - 1):
        # Main diagonal from top left to bottom right
        diag1 = []
        diag2 = []
        for i in range(n):
            for j in range(n):
                if i - j == d - n + 1:
                    diag1.append(var(i, j))
                if i + j == d:
                    diag2.append(var(i, j))

        # No two queens on the same main diagonal
        for i in range(len(diag1)):
            for j in range(i + 1, len(diag1)):
                cnf.append([-diag1[i], -diag1[j]])

        # No two queens on the same anti-diagonal
        for i in range(len(diag2)):
            for j in range(i + 1, len(diag2)):
                cnf.append([-diag2[i], -diag2[j]])

    # Use the SAT solver
    with Solver(bootstrap_with=cnf) as solver:
        if solver.solve():
            # Get the solution from the solver
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
    n = 8  #
    solution = n_queens_binomial(n)
    if solution:
        print(f"Solution for {n}-Queens:")
        for row in solution:
            print(row)
    else:
        print(f"No solution exists for {n}-Queens.")
