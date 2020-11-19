import cvxpy
import numpy as np


def main():
    mat = np.array([
        [70, 20, 10],
        [20, 50, 30],
        [10, 60, 30],
    ])

    # Room assignment
    n, r = mat.shape
    # Create two scalar optimization variables.
    mat_var = np.array([[cvxpy.Variable() for _ in range(r)] for _ in range(n)])

    constraints = []

    for idx_n in range(n):
        for idx_r in range(r):
            constraints.append(mat_var[idx_n, idx_r] >= 0)
            constraints.append(mat_var[idx_n, idx_r] <= 1)

    for idx_n in range(n):
        person_sum = 0
        for idx_r in range(r):
            person_sum += mat_var[idx_n, idx_r]
        constraints.append(person_sum == 1)

    for idx_r in range(r):
        room_sum = 0
        for idx_n in range(n):
            room_sum += mat_var[idx_n, idx_r]
        constraints.append(room_sum == 1)

    opt_eq = 0
    for idx_n in range(n):
        for idx_r in range(r):
            opt_eq += mat_var[idx_n, idx_r] * mat[idx_n, idx_r]

    obj = cvxpy.Maximize(opt_eq)

    # Form and solve problem.
    prob = cvxpy.Problem(obj, constraints)
    prob.solve()  # Returns the optimal value.

    for i in range(n):
        for j in range(r):
            print("{:.3f}".format(mat_var[i, j].value), end=';')
        print()


if __name__ == '__main__':
    main()
