import cvxpy


def calcPareto(res_matrix: list):
    n, m = len(res_matrix), len(res_matrix[0])
    # Create two scalar optimization variables.
    mat_var = [[cvxpy.Variable() for _ in range(m)] for _ in range(n)]

    # Build two constraints.
    constraints = []
    # All vars are non-negative
    for i in range(n):
        for j in range(m):
            constraints.append(mat_var[i][j] >= 0)
            constraints.append(mat_var[i][j] <= 1)

    # Sum of each colmun is 1
    for i in range(m):
        sum_con = 0
        for j in range(n):
            sum_con += mat_var[j][i]
        constraints.append(sum_con == 1)

    # Build an objective function.
    sum_var = 0
    for i in range(n):
        tmp_sum = 0
        for j in range(m):
            tmp_sum += res_matrix[i][j] * mat_var[i][j]
        sum_var += cvxpy.log(tmp_sum)
    obj = cvxpy.Maximize(sum_var)

    # Form and solve problem.
    prob = cvxpy.Problem(obj, constraints)
    prob.solve()  # Returns the optimal value.

    # Print
    print("status:", prob.status)
    for i in range(n):
        print("Agent #{} ".format(i + 1), end='')
        for j in range(m):
            print(" gets {:.4f} of resource #{}".format(mat_var[i][j].value, j + 1), end='')
            print(', ' if (j + 1) != m else '.\n', end='')


def main():
    mat = [
        [81, 19, 0],
        [80, 0, 20],
    ]

    calcPareto(mat)

    mat = [
        [1, 19, 0, 2],
        [34, 9, 2, 30],
        [80, 0, 20, 10],
    ]

    calcPareto(mat)

    mat = [
        [2, 1000],
        [4, 1000],
        [6, 1000],
    ]

    calcPareto(mat)


if __name__ == '__main__':
    main()
