from scipy.optimize import minimize, LinearConstraint

from basis_generator import cost

def optimizeBeta(H, beta, B, j):# -> tuple(float, float, float):

    x0 = [1/3] * (3 * (H.num_qubits - j))

    def f(x):
        beta_deformed = [beta[i] for i in range(j)]
        for probabilities in zip(x[0::3], x[1::3], x[2::3]):
            beta_deformed.append(probabilities)
        return cost(H, beta_deformed, B, j)

    result = minimize(f, x0, method='trust-constr', constraints=[constraints(H.num_qubits - j)])

    return result



# Constraints


def _lin_con_single(k, n):
    linear_constraint = [0]*(3*n)
    linear_constraint[k] = 1
    return linear_constraint


def _lin_con_triple(i, n):
    linear_constraint = [0]*(3*n)
    for var in [3*i, 3*i+1, 3*i+2]:
        linear_constraint[var] = 1
    return linear_constraint


def linear_constraint_matrix(n):
    # constraints to ensure \beta_{i,P} \ge 0 for all i,P
    mat1 = [_lin_con_single(k, n) for k in range(3*n)]
    # constraints to ensure \sum_P \beta_{i,P} = 1 for all i
    mat2 = [_lin_con_triple(i, n) for i in range(n)]
    return mat1+mat2


def lower_bounds(n):
    bounds_single = [0]*(3*n)
    bounds_triple = [1]*n
    return bounds_single+bounds_triple


def upper_bounds(n):
    return [1]*(4*n)


def constraints(n):
    # think of n as number of qubits minus j
    A = linear_constraint_matrix(n)
    lb = lower_bounds(n)
    ub = upper_bounds(n)
    return LinearConstraint(A, lb, ub)
