import random

id_variable = 1

def exactly_k(var, k):
    global id_variable
    n = len(var) - 1
    map_register = [[0 for _ in range(k + 1)] for _ in range(n)]
    
    for i in range(1, n):
        for j in range(1, min(i, k) + 1):
            id_variable += 1
            map_register[i][j] = id_variable

    # (1): If a bit is true, the first bit of the corresponding register is true
    for i in range(1, n):
        plus_clause([-1 * var[i], map_register[i][1]])

    # (2): R[i - 1][j] = 1, R[i][j] = 1;
    for i in range(2, n):
        for j in range(1, min(i - 1, k) + 1):
            plus_clause([-1 * map_register[i - 1][j], map_register[i][j]])

    # (3): If bit i is on and R[i - 1][j - 1] = 1, R[i][j] = 1;
    for i in range(2, n):
        for j in range(2, min(i, k) + 1):
            plus_clause([-1 * var[i], -1 * map_register[i - 1][j - 1], map_register[i][j]])

    # (4): If bit i is off and R[i - 1][j] = 0, R[i][j] = 0;
    for i in range(2, n):
        for j in range(1, min(i - 1, k) + 1):
            plus_clause([var[i], map_register[i - 1][j], -1 * map_register[i][j]])

    # (5): If bit i is off, R[i][i] = 0;
    for i in range(1, k + 1):
        plus_clause([var[i], -1 * map_register[i][i]])

    # (6): If R[i - 1][j - 1] = 0, R[i][j] = 0;
    for i in range(2, n):
        for j in range(2, min(i, k) + 1):
            plus_clause([map_register[i - 1][j - 1], -1 * map_register[i][j]])

    # (7): Ensure exactly k condition with (At least k) & (At most k)
    # At least k
    plus_clause([map_register[n - 1][k]])
    # At most k
    for i in range(k + 1, n + 1):
        plus_clause([-1 * var[i], -1 * map_register[i - 1][k]])

def plus_clause(clause):
    print("Clause:", clause)

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

test_exactly_k()
