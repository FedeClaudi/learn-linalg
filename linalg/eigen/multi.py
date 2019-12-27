"""Algorithms for finding multiple eigenpairs.
"""

import numpy as np

from linalg import utils
from linalg.eigen import single
from linalg.qrdecomp import QR


def projected_iteration(A, k, max_iter=1000, sort=True):
  """Sequentially find the k eigenpairs of a symmetric matrix.

  Concretely, combines power iteration and deflation to find
  eigenpairs in order of decreasing magnitude.

  Args:
    A: a square symmetric array of shape (N, N).
    k (int): the number of eigenpairs to return.
    sort (bool): Whether to sort by decreasing eigenvalue magnitude.

  Returns:
    e, v: eigenvalues and eigenvectors. The eigenvectors are
      stacked column-wise.
  """
  assert utils.is_symmetric(A), "[!] Matrix must be symmetric."
  assert k > 0 and k <= A.shape[0], "[!] k must be between 1 and {}.".format(A.shape[0])

  eigvecs = np.zeros((A.shape[0], k))
  eigvals = np.zeros(A.shape[0])
  for i in range(k):
    v = np.random.randn(A.shape[0])
    for _ in range(max_iter):
      # project out computed eigenvectors
      proj_sum = np.zeros_like(v)
      for j in range(i):
        proj_sum += utils.projection(v, eigvecs[:, j])
      v -= proj_sum

      v_new = A @ v
      v_new = utils.normalize(v_new)
      if np.all(np.abs(v_new - v) < 1e-8):
        break
      v = v_new
    e = single.rayleigh_quotient(A, v)

    # store eigenpair
    eigvecs[:, i] = np.array(v)
    eigvals[i] = e

  # sort by largest absolute eigenvalue
  if sort:
    idx = np.abs(eigvals).argsort()[::-1]
    eigvecs = eigvecs[:, idx]
    eigvals = eigvals[idx]

  return eigvals, eigvecs


def hessenberg(A, calc_q=False):
  """Reduce a square matrix to upper Hessenberg form using Householder reflections.

  If the input matrix is symmetric, the resulting Hessenberg form is
  reduced to tridiagonal form.

  Args:
    A: A square matrix of shape (M, M).
    calc_q (bool): Whether to explicitly compute the product of
      similarity transform Householder matrices.

  Returns:
    A: The upper Hessenberg form of the matrix of shape (M, M).
    Q: The product of Householder matrices of shape (M, M). Only
      returned if `calc_q=True`.
  """
  assert utils.is_square(A), "[!] Matrix must be square."
  is_symm = utils.is_symmetric(A)
  A = np.array(A)
  M, _ = A.shape
  vs = []
  for i in range(M-2):
    a = A[i+1:, i]
    c = utils.l2_norm(a)
    s = utils.sign(a[0])
    e = utils.basis_vec(0, len(a), flat=True)
    v = a + s*c*e
    vs.append(v)
    # left transform
    for j in range(i, M):
      A[i+1:, j] = A[i+1:, j] - (2 * v.T @ A[i+1:, j]) / (v.T @ v) * v
    # right transform
    for j in range(i if is_symm else 0, M):
      A[j, i+1:M] = A[j, i+1:M] - 2 * ((A[j, i+1:M].T @ v) / (v.T @ v)) * v.T
  if calc_q:
    Q = np.eye(M)
    for i in range(M):
      for j, v in enumerate(reversed(vs)):
        Q[M-j-2:, i] -= (2 * v.T @ Q[M-j-2:, i]) / (v.T @ v) * v
    return A, Q
  return A


def qr_algorithm(A, hess=True, sort=True):
  """The de-facto algorithm for finding all eigenpairs of a symmetric matrix.

  Args:
    A: a square symmetric array of shape (N, N).
    hess (bool): Whether to compute the Hessenberg form
      of the matrix before starting the QR iterations.
    sort (bool): Whether to sort by decreasing eigenvalue magnitude.

  Returns:
    e, v: eigenvalues and eigenvectors. The eigenvectors are
      stacked column-wise.
  """
  assert utils.is_symmetric(A), "[!] Matrix must be symmetric."
  backup = np.array(A)
  if hess:
    A = hessenberg(A, calc_q=False)
  M = A.shape[0]
  for k in range(1000):
    mu = A[M-1, M-1]  # set the shift to be the last diagonal element
    Q, R = QR(A - mu * np.eye(M)).decompose()
    A_new = R @ Q + mu * np.eye(M)
    if np.all(np.abs(A_new - A) < 1e-8):
      break
    A = A_new
  mus = utils.diag(A)
  eigvecs = np.zeros_like(A)
  eigvals = np.zeros(A.shape[0])
  for i, mu in enumerate(mus):
    eigval, eigvec = single.rayleigh_quotient_iteration(backup, mu, max_iter=1)
    eigvecs[:, i] = eigvec
    eigvals[i] = eigval
  if sort:
    idx = np.abs(eigvals).argsort()[::-1]
    eigvecs = eigvecs[:, idx]
    eigvals = eigvals[idx]
  return eigvals, eigvecs


def eig(A, sort=True):
  """Compute the eigenvalues and right eigenvectors of a symmetric matrix.
  """
  eigvals, eigvecs = qr_algorithm(A, hess=True, sort=sort)
  return eigvals, eigvecs