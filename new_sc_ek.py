import random

def exactly_k(var, k):
    global id_variable
    n = len(var) - 1  
    map_register = [[0 for _ in range(k + 1)] for _ in range(n + 1)]

    for i in range(1, n + 1):
        for j in range(1, min(i, k) + 1):
            id_variable += 1
            map_register[i][j] = id_variable

    # At least k: Generate ALO and AMO clauses
    for i in range(1, n + 1):
        plus_clause([var[i], -map_register[i][i]])

    for i in range(1, n + 1):
        plus_clause([-var[i], map_register[i][1]])

    for i in range(2, n + 1):
        for j in range(1, min(i, k) + 1):
            plus_clause([var[i], map_register[i - 1][j], -map_register[i][j]])
            plus_clause([-map_register[i - 1][j], map_register[i][j]])

    for i in range(2, n + 1):
        for j in range(2, min(i, k) + 1):
            plus_clause([-var[i], -map_register[i - 1][j - 1], map_register[i][j]])
            plus_clause([map_register[i - 1][j - 1], -map_register[i][j]])

    bonus = [[0 for _ in range(k + 1)] for _ in range(n - 1)]
    for id in range(n - 1):
        for i in range(1, k + 1):
            id_variable += 1
            bonus[id][i] = id_variable
        
        a = map_register[id + 1]
        b = [] if id == 0 else bonus[id - 1]

        for i in range(1, k + 1):
            plus_clause([-a[i], bonus[id][i]])
            if b: plus_clause([-b[i], bonus[id][i]])
            for j in range(1, k + 1):
                if i + j <= k: plus_clause([-a[i], -b[j], bonus[id][i + j]])
                if i + j == k + 1: plus_clause([-a[i], -b[j]])

    plus_clause([bonus[n - 2][k]])

def test_exactly_k():
    global id_variable
    id_variable = 1  
    num_vars = 4 
    variables = [0] + [i for i in range(1, num_vars + 1)]  

    test_cases = [
        ("Low", 1),
        ("Mid", num_vars // 2),
        ("High", num_vars)
    ]

    for label, k in test_cases:
        print(f"\nTesting with exactly k = {k} ({label} case)")
        exactly_k(variables, k)
        simulate_test_case(variables, k)

def simulate_test_case(variables, k):
    assigned_vars = [0] + [1 if i <= k else 0 for i in range(1, len(variables))]
    random.shuffle(assigned_vars[1:]) 
    print(f"Variable assignments for exactly k={k}: {assigned_vars[1:]}")

def plus_clause(clause):
    print("Clause:", clause)

test_exactly_k()