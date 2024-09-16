from pysat.formula import CNF
from pysat.solvers import Solver

def n_queens_sequential(n):
    cnf = CNF()

    def var(i, j):
        return i * n + j + 1

    for i in range(n):
        # At least one queen in each row
        cnf.append([var(i, j) for j in range(n)])

        for j in range(n):
            for k in range(j + 1, n):
                cnf.append([-var(i, j), -var(i, k)])

    # Column constraints using sequential encoding (for simplicity shown similarly)
    for j in range(n):
        # At least one queen in each column
        cnf.append([var(i, j) for i in range(n)])

        # At most one queen in each column
        for i in range(n):
            for k in range(i + 1, n):
                cnf.append([-var(i, j), -var(k, j)])

    for d in range(2 * n - 1):
        main_diag = []
        anti_diag = []
        for i in range(n):
            for j in range(n):
                if i - j == d - n + 1:
                    main_diag.append(var(i, j))
                if i + j == d:
                    anti_diag.append(var(i, j))

        for i in range(len(main_diag)):
            for j in range(i + 1, len(main_diag)):
                cnf.append([-main_diag[i], -main_diag[j]])

        for i in range(len(anti_diag)):
            for j in range(i + 1, len(anti_diag)):
                cnf.append([-anti_diag[i], -anti_diag[j]])

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
    solution = n_queens_sequential(n)
    if solution:
        print(f"Solution for {n}-Queens (Sequential Encoding):")
        for row in solution:
            print(row)
    else:
        print(f"No solution exists for {n}-Queens.")
