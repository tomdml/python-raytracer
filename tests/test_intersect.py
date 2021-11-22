from intersect import intersect, intersects
from shapes import Sphere, Plane
from ray import ray
from tuples import point, vector
from matrix import Matrix


def root(n):
    return n ** 0.5


def test_an_intersect_encapsulates_t_and_obj():
    s = Sphere()
    i = intersect(3.5, s)

    assert i.t == 3.5 and i.object == s


def test_aggregating_intersects():
    s = Sphere()
    i1 = intersect(1, s)
    i2 = intersect(2, s)

    xs = intersects(i1, i2)

    assert all([
        xs.count == 2,
        xs[0].t == 1,
        xs[1].t == 2
    ])


def test_hit_when_all_intersects_have_positive_t():
    s = Sphere()
    i1 = intersect(1, s)
    i2 = intersect(2, s)
    xs = intersects(i2, i1)

    assert xs.hit is i1


def test_hit_when_some_intersects_have_negative_t():
    s = Sphere()
    i1 = intersect(-1, s)
    i2 = intersect(1, s)
    xs = intersects(i2, i1)

    assert xs.hit is i2


def test_hit_when_all_intersects_have_negative_t():
    s = Sphere()
    i1 = intersect(-2, s)
    i2 = intersect(-1, s)
    xs = intersects(i2, i1)

    assert xs.hit is None


def test_hit_is_always_the_lowest_non_negative_intersect():
    s = Sphere()
    i1 = intersect(5, s)
    i2 = intersect(7, s)
    i3 = intersect(-3, s)
    i4 = intersect(2, s)
    xs = intersects(i1, i2, i3, i4)

    assert xs.hit is i4


def test_precomputing_the_state_of_an_intersection():
    r = ray(point(0, 0, -5), vector(0, 0, 1))
    shape = Sphere()
    i = intersect(4, shape)

    comps = i.prepare_computations(r)

    assert all([
        comps.t == i.t,
        comps.object == i.object,
        comps.point == point(0, 0, -1),
        comps.eyev == vector(0, 0, -1),
        comps.normalv == vector(0, 0, -1)
    ])


def test_the_hit_when_an_intersection_occurs_on_the_outside():
    r = ray(point(0, 0, -5), vector(0, 0, 1))
    shape = Sphere()
    i = intersect(4, shape)

    comps = i.prepare_computations(r)

    assert not comps.inside


def test_the_hit_when_an_intersection_occurs_on_the_inside():
    r = ray(point(0, 0, 0), vector(0, 0, 1))
    shape = Sphere()
    i = intersect(1, shape)

    comps = i.prepare_computations(r)

    assert all([
        comps.point == point(0, 0, 1),
        comps.eyev == vector(0, 0, -1),
        comps.inside,
        comps.normalv == vector(0, 0, -1)
    ])


def test_the_hit_should_offset_the_point():
    r = ray(point(0, 0, -5), vector(0, 0, 1))
    shape = Sphere(transform=Matrix.translate(0, 0, 1))
    i = intersect(5, shape)

    comps = i.prepare_computations(r)

    EPSILON = 0.000001

    assert all([
        comps.over_point.z < -EPSILON/2,
        comps.point.z > comps.over_point.z
    ])


def test_precomputing_the_reflection_vector():
    shape = Plane()
    r = ray(point(0, 1, -1), vector(0, -root(2)/2, root(2)/2))
    i = intersect(root(2), shape)

    comps = i.prepare_computations(r)

    assert comps.reflectv == vector(0, root(2)/2, root(2)/2)
