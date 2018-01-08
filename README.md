## linalg

Currently reinforcing my linear algebra and numerical analysis by reimplementing basic, fundamental algorithms in Python. My implementations are tested against `numpy` and `scipy` equivalents. Inspired by [Alex Nichol's Go repository](https://github.com/unixpickle/num-analysis).

## Contents

- [kahan](https://github.com/kevinzakka/linalg/tree/master/kahan): kahan summation for adding finite precision floating point numbers.
- [gelim](https://github.com/kevinzakka/linalg/tree/master/gelim): gaussian elimination with naive, partial and full pivoting for solving `Ax = b`.
- [ludecomp](https://github.com/kevinzakka/linalg/tree/master/ludecomp): `LU`, `PLU` and `PLUQ` decomposition for solving `Ax = b`.
- [determinant](https://github.com/kevinzakka/linalg/blob/master/ludecomp/determinant.py): compute the determinant (or log det) of a square matrix A using LU factorization.
- [cholesky](https://github.com/kevinzakka/linalg/tree/master/cholesky): cholesky decomposition for symmetric positive definite matrices A.
- [benchmarks](https://github.com/kevinzakka/linalg/tree/master/benchmarks): speed comparisons of different decompositions for solving `Ax = b`.
- [imagealign](https://github.com/kevinzakka/linalg/tree/master/imagealign): align a crooked image using least squares.

## Resources

- [Stanford CS 205A Notes](https://graphics.stanford.edu/courses/cs205a-13-fall/assets/notes/cs205a_notes.pdf)
- [Numerical Linear Algebra](https://www.amazon.com/Numerical-Linear-Algebra-Lloyd-Trefethen/dp/0898713617)
- [Numerical Recipes: The Art of Scientific Computing](http://numerical.recipes/)