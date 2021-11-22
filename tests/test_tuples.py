import pytest

from tuples import _tuple, vector, point, colour


def test_a_point_is_a_tuple_with_w_1():
    t = point(4.3, -4.2, 3.1)

    assert all([
        t.x == 4.3,
        t.y == -4.2,
        t.z == 3.1,
        t.w == 1.0,
        t == _tuple(4.3, -4.2, 3.1, 1.0)
    ])


def test_a_vector_is_a_tuple_with_w_0():
    t = vector(4.3, -4.2, 3.1)

    assert all([
        t.x == 4.3,
        t.y == -4.2,
        t.z == 3.1,
        t.w == 0.0,
        t == _tuple(4.3, -4.2, 3.1, 0.0)
    ])


def test_adding_two_tuples():
    t1 = _tuple(3, -2, 5, 1)
    t2 = _tuple(-2, 3, 1, 0)

    assert t1 + t2 == _tuple(1, 1, 6, 1)


def test_adding_point_and_vector():
    p = point(1, 2, 3)
    v = vector(4, 5, 6)

    assert p + v == point(5, 7, 9)


def test_adding_vector_and_vector():
    v1 = vector(1, 1, 1)
    v2 = vector(2, 3, 4)

    assert v1 + v2 == vector(3, 4, 5)


def test_cannot_add_two_points():
    p1 = point(1, 2, 3)
    p2 = point(4, 5, 6)

    with pytest.raises(ValueError):
        p1 + p2


def test_subtracting_two_points():
    p1 = point(3, 2, 1)
    p2 = point(5, 6, 7)

    assert p1 - p2 == vector(-2, -4, -6)


def test_subtracting_two_vectors():
    v1 = vector(3, 3, 3)
    v2 = vector(1, 2, 3)

    assert v1 - v2 == vector(2, 1, 0)


def test_subtracting_a_vector_from_a_point():
    v = vector(1, 2, 3)
    p = point(0, 0, 0)

    assert p - v == point(-1, -2, -3)


def test_subtracting_a_point_from_a_vector():
    v = vector(1, 2, 3)
    p = point(0, 0, 0)

    with pytest.raises(ValueError):
        v - p


def test_cannot_multiply_a_point_by_a_vector():
    v = vector(1, 2, 3)
    p = point(0, 0, 0)

    with pytest.raises(TypeError):
        v * p


def test_negating_tuple():
    t = _tuple(1, 2, 3, 1)

    assert -t == _tuple(-1, -2, -3, -1)


def test_multiply_tuple_by_scalar():
    t = _tuple(1, 2, 3, 0)

    assert t * 3.5 == _tuple(3.5, 7, 10.5, 0)


def test_multiply_tuple_by_fraction():
    t = _tuple(1, 2, 3, 0)

    assert t * 0.5 == _tuple(0.5, 1, 1.5, 0)


def test_divide_tuple_by_scalar():
    t = _tuple(1, 2, 3, 0)

    assert t / 2 == _tuple(0.5, 1, 1.5, 0)


def test_cannot_multiply_two_tuples():
    t1 = _tuple(1, 2, 3, 4)
    t2 = _tuple(1, 2, 3, 4)

    with pytest.raises(TypeError):
        t1 * t2


def test_magnitude_of_vector_1_0_0():
    v = vector(1, 0, 0)

    assert v.magnitude == 1


def test_magnitude_of_vector_1_2_3():
    v = vector(1, 2, 3)

    assert v.magnitude == 14 ** 0.5


def test_magnitude_of_vector_minus_1_2_3():
    v = vector(-1, -2, -3)

    assert v.magnitude == 14 ** 0.5


def test_normalizing_vector_4_0_0():
    v = vector(4, 0, 0)

    assert v.norm == vector(1, 0, 0)


def test_normalizing_vector_1_2_3():
    v = vector(1, 2, 3)

    assert v.norm == vector(
        1 / 14 ** 0.5,
        2 / 14 ** 0.5,
        3 / 14 ** 0.5
    )


def test_magnitude_of_normalised_vector():
    v = vector(1, 2, 3)

    assert v.norm.magnitude == 1


def test_dot_product_of_two_tuples():
    v1 = vector(1, 2, 3)
    v2 = vector(2, 3, 4)

    assert all([
        v1.dot(v2) == 20,
        v2.dot(v1) == 20
    ])


def test_cross_product_of_two_vectors():
    v1 = vector(1, 2, 3)
    v2 = vector(2, 3, 4)

    assert all([
        v1.cross(v2) == vector(-1, 2, -1),
        v2.cross(v1) == vector(1, -2, 1)
    ])


def test_colours_are_tuples():
    c = colour(-0.5, 0.4, 1.7)

    assert all([
        c.r == -0.5,
        c.g == 0.4,
        c.b == 1.7,
        isinstance(c, _tuple)
    ])


def test_adding_colours():
    c1 = colour(0.9, 0.6, 0.75)
    c2 = colour(0.7, 0.1, 0.25)

    assert c1 + c2 == colour(1.6, 0.7, 1)


def test_subtracting_colours():
    c1 = colour(0.9, 0.6, 0.75)
    c2 = colour(0.7, 0.1, 0.25)

    assert c1 - c2 == colour(0.2, 0.5, 0.5)


def test_multiply_colour_by_scalar():
    c = colour(0.2, 0.3, 0.4)

    assert c * 2 == colour(0.4, 0.6, 0.8)


def test_multiply_two_colours():
    c1 = colour(1, 0.2, 0.4)
    c2 = colour(0.9, 1, 0.1)

    assert c1 * c2 == colour(0.9, 0.2, 0.04)


def test_reflecting_a_vector_approaching_at_45deg():
    v = vector(1, -1, 0)
    n = vector(0, 1, 0)

    r = v.reflect(n)

    assert r == vector(1, 1, 0)


def test_reflecting_a_vector_off_a_slanted_surface():
    v = vector(0, -1, 0)
    n = vector((2 ** 0.5) / 2, (2 ** 0.5) / 2, 0)

    r = v.reflect(n)

    assert r == vector(1, 0, 0)
