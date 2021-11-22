import pytest

from matrix import Matrix
from tuples import _tuple


def test_creating_and_inspecting_a_4x4_Matrix():
    M = Matrix((
        (1, 2, 3, 4),
        (5.5, 6.5, 7.5, 8.5),
        (9, 10, 11, 12),
        (13.5, 14.5, 15.5, 16.5)
    ))

    assert all([
        M[0, 0] == 1,
        M[0, 3] == 4,
        M[1, 0] == 5.5,
        M[1, 2] == 7.5,
        M[2, 2] == 11,
        M[3, 0] == 13.5,
        M[3, 2] == 15.5
    ])


def test_creating_and_inspecting_a_2x2_Matrix():
    M = Matrix((
        (-3, 5),
        (1, -2)
    ))

    assert all([
        M[0, 0] == -3,
        M[0, 1] == 5,
        M[1, 0] == 1,
        M[1, 1] == -2
    ])


def test_Matrix_comparison_identical_matrices():
    M1 = Matrix((
        (1, 2, 3, 4),
        (5.5, 6.5, 7.5, 8.5),
        (9, 10, 11, 12),
        (13.5, 14.5, 15.5, 16.5)
    ))

    M2 = Matrix((
        (1, 2, 3, 4),
        (5.5, 6.5, 7.5, 8.5),
        (9, 10, 11, 12),
        (13.5, 14.5, 15.5, 16.5)
    ))

    assert M1 == M2


def test_Matrix_comparison_different_matrices():
    M1 = Matrix((
        (1, 2, 3, 4),
        (5.5, 6.5, 7.5, 8.5),
        (9, 10, 11, 12),
        (13.5, 14.5, 15.5, 16.5)
    ))

    M2 = Matrix((
        (0, 2, 3, 4),
        (5.5, 6.5, 7.5, 8.5),
        (9, 10, 11, 12),
        (13.5, 14.5, 15.5, 16.5)
    ))

    assert M1 != M2


def test_multiplying_two_matrices():
    M1 = Matrix([
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 8, 7, 6],
        [5, 4, 3, 2]
    ])

    M2 = Matrix([
        [-2, 1, 2, 3],
        [3, 2, 1, -1],
        [4, 3, 6, 5],
        [1, 2, 7, 8]
    ])

    M3 = Matrix([
        [20, 22, 50, 48],
        [44, 54, 114, 108],
        [40, 58, 110, 102],
        [16, 26, 46, 42]
    ])

    assert M1 * M2 == M3


def test_Matrix_multiplied_by_tuple():
    A = Matrix([
        [1, 2, 3, 4],
        [2, 4, 4, 2],
        [8, 6, 4, 1],
        [0, 0, 0, 1]
    ])

    b = _tuple(1, 2, 3, 1)

    assert A * b == _tuple(18, 24, 33, 1)


def test_multiply_by_identity_Matrix():
    A = Matrix([
        [1, 2, 3, 4],
        [2, 4, 4, 2],
        [8, 6, 4, 1],
        [0, 0, 0, 1]
    ])

    assert A * Matrix.identity == A


def test_multiply_tuple_by_identity_Matrix():

    a = _tuple(1, 2, 3, 1)
    assert Matrix.identity * a == a


def test_transpose_a_Matrix():
    A = Matrix([
        [0, 9, 3, 0],
        [9, 8, 0, 8],
        [1, 8, 5, 3],
        [0, 0, 5, 8]
    ])

    T = Matrix([
        [0, 9, 1, 0],
        [9, 8, 8, 0],
        [3, 0, 5, 5],
        [0, 8, 3, 8]
    ])

    assert A.T == T


def test_transpose_the_identity_Matrix():
    assert Matrix.identity == Matrix.identity.T


def test_determinant_of_2x2_Matrix():
    A = Matrix([
        [1, 5],
        [-3, 2]
    ])

    assert A.determinant == 17


def test_subMatrix_of_a_3x3_Matrix_is_a_2x2_Matrix():
    A = Matrix([
        [1, 5, 0],
        [-3, 2, 7],
        [0, 6, -3]
    ])

    S = Matrix([
        [-3, 2],
        [0, 6]
    ])

    assert A.subMatrix(0, 2) == S


def test_subMatrix_of_a_4x4_Matrix_is_a_3x3_Matrix():
    A = Matrix([
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 11, 12],
        [13, 14, 15, 16]
    ])

    S = Matrix([
        [6, 7, 8],
        [10, 11, 12],
        [14, 15, 16]
    ])

    assert A.subMatrix(0, 0) == S


def test_minor_of_3x3_Matrix():
    A = Matrix([
        [3, 5, 0],
        [2, -1, -7],
        [6, -1, 5]
    ])

    B = A.subMatrix(1, 0)

    assert all([
        B.determinant == 25,
        A.minor(1, 0) == 25
    ])


def test_cofactor_of_3x3_Matrix():
    A = Matrix([
        [3, 5, 0],
        [2, -1, -7],
        [6, -1, 5]
    ])

    assert all([
        A.minor(0, 0) == -12,
        A.cofactor(0, 0) == -12,
        A.minor(1, 0) == 25,
        A.cofactor(1, 0) == -25
    ])


def test_determinant_of_3x3_Matrix():
    A = Matrix([
        [1, 2, 6],
        [-5, 8, -4],
        [2, 6, 4]
    ])

    assert all([
        A.cofactor(0, 0) == 56,
        A.cofactor(0, 1) == 12,
        A.cofactor(0, 2) == -46,
        A.determinant == -196
    ])


def test_determinant_of_4x4_Matrix():
    A = Matrix([
        [-2, -8, 3, 5],
        [-3, 1, 7, 3],
        [1, 2, -9, 6],
        [-6, 7, 7, -9]
    ])

    assert all([
        A.cofactor(0, 0) == 690,
        A.cofactor(0, 1) == 447,
        A.cofactor(0, 2) == 210,
        A.cofactor(0, 3) == 51,
        A.determinant == -4071
    ])


def test_an_invertible_Matrix_for_invertibility():
    A = Matrix([
        [6, 4, 4, 4],
        [5, 5, 7, 6],
        [4, -9, 3, -7],
        [9, 1, 7, -6]
    ])

    assert all([
        A.determinant == -2120,
        A.invertible
    ])


def test_a_noninvertible_Matrix_for_invertibility():
    A = Matrix([
        [-4, 2, -2, -3],
        [9, 6, 2, 6],
        [0, -5, 1, -5],
        [0, 0, 0, 0]
    ])

    assert all([
        A.determinant == 0,
        not A.invertible
    ])


def test_a_noninvertible_Matrix_raises_a_ValueError():
    A = Matrix([
        [-4, 2, -2, -3],
        [9, 6, 2, 6],
        [0, -5, 1, -5],
        [0, 0, 0, 0]
    ])

    with pytest.raises(ValueError):
        A.inverse


def test_the_inverse_of_a_Matrix():
    A = Matrix([
        [-5, 2, 6, -8],
        [1, -5, 1, 8],
        [7, 7, -6, -7],
        [1, -3, 7, 4]
    ])

    B = A.inverse

    C = Matrix([
        [0.21805, 0.45113, 0.24060, -0.04511],
        [-0.80827, -1.45677, -0.44361, 0.52068],
        [-0.07895, -0.22368, -0.05263, 0.19737],
        [-0.52256, -0.81391, -0.30075, 0.30639]
    ])

    print(B.data)

    assert all([
        A.determinant == 532,
        A.cofactor(2, 3) == -160,
        B[3, 2] == -160/532,
        A.cofactor(3, 2) == 105,
        B[2, 3] == 105/532,
        B == C
    ])


def test_multiplying_a_product_by_its_inverse():
    A = Matrix([
        [3, -9, 7, 3],
        [3, -8, 2, -9],
        [-4, 4, 4, 1],
        [-6, 5, -1, 1]
    ])

    B = Matrix([
        [8, 2, 2, 2],
        [3, -1, 7, 0],
        [7, 0, 5, 4],
        [6, -2, 0, 5]
    ])

    C = A * B

    assert C * B.inverse == A

