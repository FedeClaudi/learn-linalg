import numpy as np

from sum import KahanSum
from functools import reduce


def l2_norm(x):
    """
    L2 or "euclidean" norm.
    """
    return np.sqrt(np.dot(x.T, x))


def norm(x, p):
    """
    Returns the p norm of a vector.
    """
    v = np.array(x).flatten()

    error_msg = "x must be 1D"
    assert v.ndim == 1, error_msg
    error_msg = "p must be >= 1"
    assert p >= 1, error_msg

    N = v.shape[0]

    summer = KahanSum()
    for i in range(N):
        summer.add(np.power(np.abs(v[i]), p))

    return np.power(summer.cur_sum(), 1./p)


def herm(A):
    """
    Returns the conjugate transpose of A.
    Equivalent to the H operator `A.H`.
    """
    return A.T.conj()


def is_hermitian(A):
    """
    Returns True if A is hermitian.
    """
    return np.allclose(A, A.T.conj())


def is_symmetric(A):
    """
    Returns True if A is symmetric.
    """
    return np.allclose(A, A.T)


def upper_diag(A, diag=False):
    """
    Grabs the super-diagonal elements of a
    square matrix A.
    """
    m = len(A)
    U = np.zeros_like(A)

    for i in range(m):
        l_b = i + 1
        if diag:
            l_b = i
        for j in range(l_b, m):
            U[i, j] = A[i, j]

    return U


def lower_diag(A, diag=False):
    """
    Grabs the sub-diagonal elements of a
    square matrix A.
    """
    m = len(A)
    L = np.zeros_like(A)

    for i in range(m):
        u_b = i
        if diag:
            u_b = i + 1
        for j in range(0, u_b):
            L[i, j] = A[i, j]

    return L


def unit_diag(A):
    """
    Fills the diagonal elements of a
    square matrix A with 1's.
    """
    m = len(A)

    for i in range(m):
        A[i, i] = 1

    return A


def multi_dot(l):
    """
    Performs consecutive dot products of the
    arrays in the list l from left to right.

    For example, given l = [A, B, C], returns
    `np.dot(np.dot(A, B), C)`.

    """
    return reduce(np.dot, l)


def basis_vec(k, n):
    """
    Creates the k'th standard basis vector in R^n.
    """

    error_msg = "[!] k cannot exceed {}.".format(n)
    assert (k < n), error_msg

    b = np.zeros([n, 1])
    b[k] = 1
    return b


def basis_arr(ks, n):
    """
    Creates an array of k'th standard basis vectors in R^n
    according to each k in ks.
    """

    error_msg = "[!] ks cannot exceed {}.".format(n)
    assert (np.max(ks) < n), error_msg

    b = np.zeros([n, n])
    for i, k in enumerate(ks):
        b[i, k] = 1
    return b
