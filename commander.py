from pysat.formula import CNF
from pysat.solvers import Solver

def var(i, j, n):
    return i * n + j + 1

def add_commander_encoding(cnf, variables, group_size):
    if len(variables) <= 1:
        return
    groups = [variables[i:i + group_size] for i in range(0, len(variables), group_size)]
    commander_vars = []
    
    for group in groups:
        if len(group) > 1:
            commander_var = max(var for clause in cnf for var in clause) + 1
            commander_vars.append(commander_var)
            cnf.append(group + [-commander_var])
            
            for i in range(len(group)):
                for j in range(i + 1, len(group)):
                    cnf.append([-group[i], -group[j]])
                    
            for var in group:
                cnf.append([-commander_var, var])
                
    if commander_vars:
        add_commander_encoding(cnf, commander_vars, group_size)

def add_exactly_one(cnf, variables, group_size):
    cnf.append(variables)
    add_commander_encoding(cnf, variables, group_size)

def generate_clauses(n, group_size):
    cnf = CNF()
    for i in range(n):
        row_vars = [var(i, j, n) for j in range(n)]
        col_vars = [var(j, i, n) for j in range(n)]
        add_exactly_one(cnf, row_vars, group_size)
        add_exactly_one(cnf, col_vars, group_size)  

    for d in range(2 * n - 1):
        main_diag_vars = [var(i, d - i, n) for i in range(n) if 0 <= d - i < n]
        anti_diag_vars = [var(i, i - d + n - 1, n) for i in range(n) if 0 <= i - d + n - 1 < n]
        add_commander_encoding(cnf, main_diag_vars, group_size)
        add_commander_encoding(cnf, anti_diag_vars, group_size)

    return cnf

def solve_n_queens(n, group_size):
    cnf = generate_clauses(n, group_size)

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
    group_size = 3 
    solution = solve_n_queens(n, group_size)
    print_solution(solution)
