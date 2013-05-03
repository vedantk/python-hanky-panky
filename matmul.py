#!/usr/bin/python

import copy
import operator

def rows(X):
    return len(X)

def cols(X):
    return len(X[0])

def sane_rows_p(X):
    return all((len(X[k]) == len(X[0])
                for k in range(1, len(X))))

def multiply_p(A, B):
    return cols(A) == rows(B) and sane_rows_p(A) and sane_rows_p(B)

def even_square_p(X):
    return (not (rows(X) & 1)) and len(X) == len(X[0])

def new_matrix(n, m):
    return [copy.copy([0 for j in range(m)]) for i in range(n)]

def dotproduct(l, r):
    return sum([a * b for (a, b) in zip(l, r)])

def naive(A, B):
    nr_rows = rows(A)
    nr_cols = cols(B)
    result = new_matrix(nr_rows, nr_cols)
    for i in range(nr_rows):
        for j in range(nr_cols):
            result[i][j] = dotproduct([A[i][z] for z in range(cols(A))],
                                      [B[z][j] for z in range(rows(B))])
    return result

def matop(L, R, op):
    N = rows(L)
    f = operator.add if op == '+' else operator.sub
    return [[f(L[i][j], R[i][j]) for j in range(N)] for i in range(N)]

matadd = lambda L, R: matop(L, R, '+')
matsub = lambda L, R: matop(L, R, '-')

def matinject(result, X, z):
    N = rows(X)
    for i in range(N):
        for j in range(N):
            k, l = z[i][j]
            result[k][l] = X[i][j]

def strassen(L, R):
    if rows(L) == 2:
        return naive(L, R)

    N = rows(L)
    N2 = N // 2
    Aij = [[(i, j) for j in range(N2)] for i in range(N2)]
    Bij = [[(i, j) for j in range(N2, N)] for i in range(N2)]
    Cij = [[(i, j) for j in range(N2)] for i in range(N2, N)]
    Dij = [[(i, j) for j in range(N2, N)] for i in range(N2, N)]

    get = lambda X, z: [[X[idx[0]][idx[1]] for idx in row] for row in z]

    A, B, C, D, E, F, G, H = map(get,
                                 [L] * 4 + [R] * 4,
                                 [Aij, Bij, Cij, Dij] * 2)

    P1 = strassen(A, matsub(F, H))
    P2 = strassen(matadd(A, B), H)
    P3 = strassen(matadd(C, D), E)
    P4 = strassen(D, matsub(G, E))
    P5 = strassen(matadd(A, D), matadd(E, H))
    P6 = strassen(matsub(B, D), matadd(G, H))
    P7 = strassen(matsub(A, C), matadd(E, F))
    
    result = new_matrix(N, N)
    matinject(result, matadd(matsub(matadd(P5, P4), P2), P6), Aij)
    matinject(result, matadd(P1, P2), Bij)
    matinject(result, matadd(P3, P4), Cij)
    matinject(result, matsub(matsub(matadd(P1, P5), P3), P7), Dij)
    return result

def matmul(A, B):
    if not multiply_p(A, B):
        raise Exception('Matrix dimensions do not match.')

    if even_square_p(A) and even_square_p(B) and rows(A) == rows(B):
        return strassen(A, B)
    else:
        return naive(A, B)

if __name__ == '__main__':
    mat = matmul([[1, 0, 0], [0, 1, 0], [0, 0, 1]],
                 [[1, 1, 1], [0, 0, 0], [1, 0, 1]])
    print(mat)

    mat = matmul([[1, 0, 0, 0],
                  [0, 1, 0, 0],
                  [0, 0, 1, 0],
                  [0, 0, 0, 1]],
                 [[1, 1, 1, 1],
                  [0, 0, 0, 0],
                  [1, 0, 1, 0],
                  [0, 1, 0, 1]])
    print(mat)
