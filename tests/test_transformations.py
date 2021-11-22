from math import pi

from matrix import Matrix
from tuples import _tuple, point, vector


def sqrt(n):
    return n ** 0.5


def test_multiply_by_a_translation_Matrix():
    transform = Matrix.identity.translate(5, -3, 2)
    p = point(-3, 4, 5)

    assert transform * p == point(2, 1, 7)


def test_multiply_by_inverse_of_a_translation_Matrix():
    transform = Matrix.identity.translate(5, -3, 2)
    inv = transform.inverse
    p = point(-3, 4, 5)

    assert inv * p == point(-8, 7, 3)


def test_translation_does_not_affect_vectors():
    transform = Matrix.identity.translate(5, -3, 2)
    v = vector(-3, 4, 5)

    assert transform * v == v


def test_scaling_Matrix_applied_to_point():
    transform = Matrix.identity.scale(2, 3, 4)
    p = point(-4, 6, 8)

    assert transform * p == point(-8, 18, 32)


def test_scaling_Matrix_applied_to_vector():
    transform = Matrix.identity.scale(2, 3, 4)
    v = vector(-4, 6, 8)

    assert transform * v == vector(-8, 18, 32)


def test_scaling_by_the_inverse_of_a_scaling_Matrix():
    transform = Matrix.identity.scale(2, 3, 4)
    inv = transform.inverse
    v = vector(-4, 6, 8)

    assert inv * v == vector(-2, 2, 2)


def test_reflection_is_scaling_by_negative_value():
    transform = Matrix.identity.scale(-1, 1, 1)
    p = point(2, 3, 4)

    assert transform * p == point(-2, 3, 4)


def test_rotating_a_point_around_the_x_axis():
    p = point(0, 1, 0)
    half_quarter = Matrix.identity.rotate('x', pi / 4)
    full_quarter = Matrix.identity.rotate('x', pi / 2)

    assert all([
        half_quarter * p == point(0, sqrt(2)/2, sqrt(2)/2),
        full_quarter * p == point(0, 0, 1)
    ])


def test_inverse_of_x_rotation_rotates_in_opposite_direction():
    p = point(0, 1, 0)
    half_quarter = Matrix.identity.rotate('x', pi / 4)
    inv = half_quarter.inverse

    assert inv * p == point(0, sqrt(2)/2, -sqrt(2)/2)


def test_rotating_a_point_around_the_y_axis():
    p = point(0, 0, 1)
    half_quarter = Matrix.identity.rotate('y', pi / 4)
    full_quarter = Matrix.identity.rotate('y', pi / 2)

    assert all([
        half_quarter * p == point(sqrt(2)/2, 0, sqrt(2)/2),
        full_quarter * p == point(1, 0, 0)
    ])


def test_rotating_a_point_around_the_z_axis():
    p = point(0, 1, 0)
    half_quarter = Matrix.identity.rotate('z', pi / 4)
    full_quarter = Matrix.identity.rotate('z', pi / 2)

    assert all([
        half_quarter * p == point(-sqrt(2)/2, sqrt(2)/2, 0),
        full_quarter * p == point(-1, 0, 0)
    ])


def test_a_shear_transformation_moves_x_in_proportion_to_y():
    transform = Matrix.identity.shear(1, 0, 0, 0, 0, 0)
    p = point(2, 3, 4)

    assert transform * p == point(5, 3, 4)


def test_a_shear_transformation_moves_x_in_proportion_to_z():
    transform = Matrix.identity.shear(0, 1, 0, 0, 0, 0)
    p = point(2, 3, 4)

    assert transform * p == point(6, 3, 4)


def test_a_shear_transformation_moves_y_in_proportion_to_x():
    transform = Matrix.identity.shear(0, 0, 1, 0, 0, 0)
    p = point(2, 3, 4)

    assert transform * p == point(2, 5, 4)


def test_a_shear_transformation_moves_y_in_proportion_to_z():
    transform = Matrix.identity.shear(0, 0, 0, 1, 0, 0)
    p = point(2, 3, 4)

    assert transform * p == point(2, 7, 4)


def test_a_shear_transformation_moves_z_in_proportion_to_x():
    transform = Matrix.identity.shear(0, 0, 0, 0, 1, 0)
    p = point(2, 3, 4)

    assert transform * p == point(2, 3, 6)


def test_a_shear_transformation_moves_z_in_proportion_to_y():
    transform = Matrix.identity.shear(0, 0, 0, 0, 0, 1)
    p = point(2, 3, 4)

    assert transform * p == point(2, 3, 7)


def test_individual_transforms_are_applied_in_sequence():
    p = point(1, 0, 1)
    A = Matrix.identity.rotate('x', pi/2)
    B = Matrix.identity.scale(5, 5, 5)
    C = Matrix.identity.translate(10, 5, 7)

    p2 = A * p
    p3 = B * p2
    p4 = C * p3

    assert all([
        p2 == point(1, -1, 0),
        p3 == point(5, -5, 0),
        p4 == point(15, 0, 7)
    ])


def test_chained_transforms_are_applied_in_correct_order():
    p = point(1, 0, 1)
    T = Matrix              \
        .identity        \
        .rotate('x', pi/2)  \
        .scale(5, 5, 5)     \
        .translate(10, 5, 7)

    assert T * p == point(15, 0, 7)


def test_the_transformation_matrix_for_the_default_orientation():
    _from = point(0, 0, 0)
    to = point(0, 0, -1)
    up = vector(0, 1, 0)

    t = Matrix.view_transform(_from, to, up)

    assert t == Matrix.identity


def test_a_view_transform_looking_in_positive_z_direction():
    _from = point(0, 0, 0)
    to = point(0, 0, 1)
    up = vector(0, 1, 0)

    t = Matrix.view_transform(_from, to, up)

    assert t == Matrix.scale(-1, 1, -1)


def test_the_view_transformation_moves_the_world():
    _from = point(0, 0, 8)
    to = point(0, 0, 0)
    up = vector(0, 1, 0)

    t = Matrix.view_transform(_from, to, up)

    assert t == Matrix.translate(0, 0, -8)


def test_an_arbitrary_view_transformation():
    _from = point(1, 3, 2)
    to = point(4, -2, 8)
    up = vector(1, 1, 0)

    t = Matrix.view_transform(_from, to, up)

    print(t)

    assert t == Matrix([
        [-0.50709, 0.50709, 0.67612, -2.36643],
        [0.76772, 0.60609, 0.12122, -2.82843],
        [-0.35857, 0.59671, -0.71714, 0.00000],
        [0.00000, 0.00000, 0.00000, 1.00000]
    ])

