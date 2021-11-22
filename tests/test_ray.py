from tuples import point, vector
from ray import ray
from matrix import Matrix


def test_creating_and_querying_a_ray():
    origin = point(1, 2, 3)
    direction = vector(4, 5, 6)

    r = ray(origin, direction)

    assert all([
        r.origin == origin,
        r.direction == direction
    ])


def test_computing_a_point_from_a_distance():
    r = ray(point(2, 3, 4), vector(1, 0, 0))

    assert all([
        r.position(0) == point(2, 3, 4),
        r.position(1) == point(3, 3, 4),
        r.position(-1) == point(1, 3, 4),
        r.position(2.5) == point(4.5, 3, 4)
    ])


def test_translating_a_ray():
    r = ray(point(1, 2, 3), vector(0, 1, 0))
    M = Matrix.identity.translate(3, 4, 5)

    r2 = r.transform(M)

    assert r2.origin == point(4, 6, 8) and \
        r2.direction == vector(0, 1, 0)


def test_scaling_a_ray():
    r = ray(point(1, 2, 3), vector(0, 1, 0))
    M = Matrix.identity.scale(2, 3, 4)

    r2 = r.transform(M)

    assert r2.origin == point(2, 6, 12) and \
        r2.direction == vector(0, 3, 0)
