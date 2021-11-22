from functools import cached_property
from math import cos, sin

from tuples import _tuple


class Matrix:

    @classmethod
    def zeroes(cls, n):
        """
        Alternative constructor for a square Matrix comprising only zeroes
        """

        return Matrix([[0]*n for _ in range(n)])

    @staticmethod
    def view_transform(_from, to, up):
        forward = (to - _from).norm
        upn = up.norm
        left = forward.cross(upn)
        true_up = left.cross(forward)

        orientation = Matrix([
            [left.x, left.y, left.z, 0],
            [true_up.x, true_up.y, true_up.z, 0],
            [-forward.x, -forward.y, -forward.z, 0],
            [0, 0, 0, 1]
        ])

        return orientation * Matrix.translate(-_from.x, -_from.y, -_from.z)

    # placeholder: identity is inserted as a class attr
    # after the class is created
    identity = ...

    def __init__(self, data):
        self.data = data

    def __str__(self):
        return '\n'.join(str(row) for row in self)

    def __getitem__(self, keys):
        """
        We use numpy-style [a, b] indexing for consistency with the
          learning material (And with numpy!)
        """

        if isinstance(keys, slice):
            return self.data[keys]
        else:
            r, c = keys
            return self.data[r][c]

    def __setitem__(self, keys, value):
        r, c = keys
        self.data[r][c] = value

    def __len__(self):
        return len(self.data)

    def __iter__(self):
        """
        Used to iterate directly over Matrix instead of Matrix.data
        """

        return iter(self.data)

    def __eq__(self, other):
        def nearly_equal(a, b):
            EPSILON = 0.001
            return abs(a - b) < EPSILON

        if isinstance(other, Matrix):
            return all(
                nearly_equal(cell, other_cell)
                for row, other_row in zip(self, other)
                for cell, other_cell in zip(row, other_row)
            )

    def __mul__(self, other):
        """
        While general algorithms exist, this implementation only requires
          4x4 Matrix multiplications and (4x4) * (4x1) vectors.
        """

        A = self
        B = other

        if isinstance(other, Matrix):

            M = Matrix.zeroes(4)

            for row in range(4):
                for col in range(4):
                    M[row, col] = (
                        A[row, 0] * B[0, col] +
                        A[row, 1] * B[1, col] +
                        A[row, 2] * B[2, col] +
                        A[row, 3] * B[3, col]
                    )

            return M

        if isinstance(other, _tuple):

            result = [0, 0, 0, 0]

            for row in range(4):
                result[row] = (
                    A[row, 0] * B.x +
                    A[row, 1] * B.y +
                    A[row, 2] * B.z +
                    A[row, 3] * B.w
                )

            return _tuple(*result)

    @cached_property
    def T(self):
        """ Matrix transpose with the zip(*data) method. """

        return Matrix([list(row) for row in zip(*self)])

    @cached_property
    def determinant(self):
        """
        The determinant is used to determine whether a system
          represented by a Matrix has a solution.
          if the determinant is 0, then the system has no solution.
        It is implemented recursively, with the base case of a [2 x 2] Matrix.
        """

        if len(self) == 2:
            [a, b], [c, d] = self
            return a * d - b * c

        return sum(
            cell * self.cofactor(0, cell_idx)
            for cell_idx, cell in enumerate(self.data[0])
        )

    def subMatrix(self, r, c):
        """
        Given a row r and a column c, build a new Matrix containing all
          rows and columns except r and c.
        """

        return Matrix([
            row[:c] + row[c+1:]
            for row in self[:r] + self[r+1:]
        ])

    def minor(self, r, c):
        """
        The minor of a Matrix at (r, c) is the determinant of
          the subMatrix at (r, c).
        """

        return self.subMatrix(r, c).determinant

    def cofactor(self, r, c):
        """
        The cofactor is the minor at (r, c)
          with a sign transformation applied as such:
        [ + - +
          - + -
          + - + ]
        """

        minor = self.minor(r, c)
        return +minor if (r + c) % 2 == 0 else -minor

    @cached_property
    def invertible(self):
        return self.determinant != 0

    @cached_property
    def inverse(self):
        """
        The algorithm to calculate the inverse of a Matrix is as follows:
          1. Construct a Matrix of cofactors at every point.
          2. Transpose the cofactor Matrix.
          3. Divide every element by the determinant.
        The code below rolls these steps into one,
          making for a more concise implementation.
        """

        if not self.invertible:
            raise ValueError('Matrix is not invertible.')

        M = Matrix.zeroes(len(self))

        for row in range(len(self)):
            for col in range(len(self)):
                c = self.cofactor(row, col)

                # Implicit transpose by swapping row, col for col, row
                M[col, row] = c / self.determinant

        return M

    def translate(self, x, y, z=0):
        """
        Given an input Matrix, produce a new Matrix representing the translation.
        NOTE: the transform Matrix is multiplied by the input Matrix,
        not the other way round, as the transform chain must be inverted.
        """
        if not isinstance(self, Matrix):
            x, y, z = self, x, y
            return Matrix.identity.translate(x, y, z)

        transform = Matrix([
            [1, 0, 0, x],
            [0, 1, 0, y],
            [0, 0, 1, z],
            [0, 0, 0, 1]
        ])

        return transform * self

    def scale(self, x, y, z=None):
        """
        Given an input Matrix, produce a new Matrix representing the scaling.
        NOTE: the transform Matrix is multiplied by the input Matrix,
        not the other way round, as the transform chain must be inverted.
        """

        if not isinstance(self, Matrix):
            x, y, z = self, x, y
            return Matrix.identity.scale(x, y, z)

        transform = Matrix([
            [x, 0, 0, 0],
            [0, y, 0, 0],
            [0, 0, z, 0],
            [0, 0, 0, 1]
        ])

        return transform * self

    def rotate(self, axis, r=None):
        """
        Given an input Matrix, an axis, and an angle in radians,
          create a transform Matrix representing rotation around the axis.
        NOTE: the transform Matrix is multiplied by the input Matrix,
        not the other way round, as the transform chain must be inverted.
        """

        if not isinstance(self, Matrix):
            axis, r = self, axis
            return Matrix.identity.rotate(axis, r)

        if axis == 'x':
            transform = Matrix([
                [   1   ,   0   ,    0   ,   0   ],
                [   0   , cos(r), -sin(r),   0   ],
                [   0   , sin(r),  cos(r),   0   ],
                [   0   ,   0   ,    0   ,   1   ]
            ])

        if axis == 'y':
            transform = Matrix([
                [  cos(r),   0   , sin(r),   0   ],
                [    0   ,   1   ,   0   ,   0   ],
                [ -sin(r),   0   , cos(r),   0   ],
                [    0   ,   0   ,   0   ,   1   ]
            ])

        if axis == 'z':
            transform = Matrix([
                [ cos(r), -sin(r),   0   ,   0   ],
                [ sin(r),  cos(r),   0   ,   0   ],
                [   0   ,    0   ,   1   ,   0   ],
                [   0   ,    0   ,   0   ,   1   ]
            ])

        return transform * self

    def shear(self, xy, xz, yx, yz, zx, zy):
        """
        Given an input Matrix, produce a new Matrix representing the shearing.
        NOTE: the transform Matrix is multiplied by the input Matrix,
        not the other way round, as the transform chain must be inverted.
        """

        if not isinstance(self, Matrix):
            xy, xz, yx, yz, zx, zy = self, xy, xz, yx, yz, zx
            return Matrix.identity.shear(xy, xz, yx, yz, zx, zy)

        transform = Matrix([
            [1 , xy, xz, 0],
            [yx, 1 , yz, 0],
            [zx, zy, 1 , 0],
            [0 , 0 , 0 , 1]
        ])

        return transform * self


Matrix.identity = Matrix([
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 1]
])

