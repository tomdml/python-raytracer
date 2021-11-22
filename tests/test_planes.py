from shapes import Plane
from tuples import point, vector
from ray import ray


def test_the_normal_of_a_plane_is_constant_everywhere():
    p = Plane()
    n1 = p.normal_at(point(0, 0, 0))
    n2 = p.normal_at(point(10, 0, -10))
    n3 = p.normal_at(point(-5, 0, 150))

    assert n1 == n2 == n3 == vector(0, 1, 0)


def test_intersect_with_a_ray_parallel_to_the_plane():
    p = Plane()
    r = ray(point(0, 10, 0), vector(0, 0, 1))

    xs = p.intersect(r)

    assert not xs


def test_intersect_with_a_coplanar_ray():
    p = Plane()
    r = ray(point(0, 0, 0), vector(0, 0, 1))

    xs = p.intersect(r)

    assert not xs


def test_a_ray_intersecting_a_plane_from_above():
    p = Plane()
    r = ray(point(0, 1, 0), vector(0, -1, 0))

    xs = p.intersect(r)

    assert all([
        xs.count == 1,
        xs[0].t == 1,
        xs[0].object == p
    ])


def test_a_ray_intersecting_a_plane_from_below():
    p = Plane()
    r = ray(point(0, -1, 0), vector(0, 1, 0))

    xs = p.intersect(r)

    assert all([
        xs.count == 1,
        xs[0].t == 1,
        xs[0].object == p
    ])

