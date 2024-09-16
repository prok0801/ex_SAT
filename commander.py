from pysat.formula import CNF
from pysat.solvers import Solver

def add_commander_encoding(cnf, variables, group_size):
    if len(variables) <= 1:
        return

    commander_vars = []
    for i in range(0, len(variables), group_size):
        group = variables[i:i + group_size]
        if len(group) > 1:
            commander_var = cnf.nv + 1
            cnf.nv += 1  
            commander_vars.append(commander_var)

            for var in group:
                cnf.append([-var, commander_var])

            for j in range(len(group)):
                for k in range(j + 1, len(group)):
                    cnf.append([-group[j], -group[k]])

    if len(commander_vars) > 1:
        add_commander_encoding(cnf, commander_vars, group_size)


def solve_n_queens(n, group_size):
    cnf = CNF()
    cnf.nv = 0 
    variables = []

    for i in range(n):
        row_vars = []
        for j in range(n):
            var = cnf.nv + 1
            cnf.nv += 1
            row_vars.append(var)
        variables.append(row_vars)

    for i in range(n):
        cnf.append(variables[i])  # ALO
        add_commander_encoding(cnf, variables[i], group_size)  # AMO

        col_vars = [variables[j][i] for j in range(n)]
        cnf.append(col_vars)  # ALO
        add_commander_encoding(cnf, col_vars, group_size)  # AMO

    for d in range(2 * n - 1):
        diag1_vars = [variables[i][d - i] for i in range(max(0, d - n + 1), min(n, d + 1))]
        if len(diag1_vars) > 1:
            add_commander_encoding(cnf, diag1_vars, group_size)

        diag2_vars = [variables[i][n - d + i - 1] for i in range(max(0, d - n + 1), min(n, d + 1))]
        if len(diag2_vars) > 1:
            add_commander_encoding(cnf, diag2_vars, group_size)

    with Solver(bootstrap_with=cnf.clauses) as solver:
        if solver.solve():
            model = solver.get_model()
            solution = []
            for i in range(n):
                row = ""
                for j in range(n):
                    if model[variables[i][j] - 1] > 0:
                        row += "Q"
                    else:
                        row += "."
                solution.append(row)
            return solution
        else:
            return None


def print_solution(solution):
    if solution:
        for row in solution:
            print(row)
    else:
        print("No solution found.")


if __name__ == "__main__":
    n = 16
    group_size = 3
    solution = solve_n_queens(n, group_size)
    print_solution(solution)
