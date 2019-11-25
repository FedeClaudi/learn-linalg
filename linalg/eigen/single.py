"""Single eigenvalue finding algorithms.
"""

import numpy as np

from linalg import utils
from linalg.ludecomp import LU
from linalg.solver import solve


def power_iteration(A, max_iter=1000):
  """Finds the largest eigenvector of a symmetric matrix.

  Args:
    A: a square symmetric array of shape (N, N).

  Returns:
    e, v: eigenvalue and eigenvector.
  """
  assert utils.is_symmetric(A), "[!] Matrix must be symmetric."
  v = np.random.randn(A.shape[0])
  for i in range(max_iter):
    v = A @ v
    v /= utils.l2_norm(v)
  e = rayleigh_quotient(A, v)
  return e, v


def inverse_iteration(A, max_iter=1000):
  """Finds the smallest eigenvector of a symmetric matrix.

  Args:
    A: a square symmetric array of shape (N, N).

  Returns:
    e, v: eigenvalue and eigenvector.
  """
  assert utils.is_symmetric(A), "[!] Matrix must be symmetric."
  v = np.random.randn(A.shape[0])
  PLU = LU(A.copy(), pivoting='partial').decompose()
  for i in range(max_iter):
    v = solve(PLU, v)
    v /= utils.l2_norm(v)
  e = rayleigh_quotient(A, v)
  return e, v


def rayleigh_quotient_iteration(A, mu, max_iter=1000):
  """Finds an eigenvalue closest to an initial eigenvalue guess.

  Args:
    A: a square symmetric array of shape (N, N).
    mu: an initial eigenvalue guess. If none, the smallest is found.

  Returns:
    e, v: eigenvalue and eigenvector.
  """
  assert utils.is_symmetric(A), "[!] Matrix must be symmetric."
  v = np.random.randn(A.shape[0])
  for i in range(max_iter):
    v = solve(A - mu*np.eye(A.shape[0]), v)
    v /= utils.l2_norm(v)
    mu = rayleigh_quotient(A, v)
  return mu, v


def rayleigh_quotient(A, x):
  """Computes the Rayleigh quotient.

  This is useful for determning an eigenvalue from
  an eigenvector, e.g. after using inverse iteration.
  """
  num = x.T @ A @ x
  denum = x.T @ x
  if np.isclose(x.T@x, 1.):
    return num
  return num / denum
