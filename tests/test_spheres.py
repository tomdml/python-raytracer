from ray import ray
from shapes import Sphere
from tuples import point, vector
from matrix import Matrix
from materials import Material

from math import pi


def test_a_ray_intersects_a_Sphere_at_two_points():
    r = ray(point(0, 0, -5), vector(0, 0, 1))
    s = Sphere()

    xs = s.intersect(r)

    assert all([
        xs.count == 2,
        xs[0].t == 4.0,
        xs[1].t == 6.0
    ])


def test_a_ray_intersects_a_Sphere_at_a_tangent():
    r = ray(point(0, 1, -5), vector(0, 0, 1))
    s = Sphere()

    xs = s.intersect(r)

    assert all([
        xs.count == 2,
        xs[0].t == 5.0,
        xs[1].t == 5.0
    ])


def test_a_ray_misses_a_Sphere():
    r = ray(point(0, 2, -5), vector(0, 0, 1))
    s = Sphere()

    xs = s.intersect(r)

    assert xs.count == 0


def test_a_ray_originates_inside_a_Sphere():
    r = ray(point(0, 0, 0), vector(0, 0, 1))
    s = Sphere()

    xs = s.intersect(r)

    assert all([
        xs.count == 2,
        xs[0].t == -1.0,
        xs[1].t == 1.0
    ])


def test_a_Sphere_is_behind_a_ray():
    r = ray(point(0, 0, 5), vector(0, 0, 1))
    s = Sphere()

    xs = s.intersect(r)

    assert all([
        xs.count == 2,
        xs[0].t == -6.0,
        xs[1].t == -4.0
    ])


def test_intersect_sets_the_object_on_the_intersection():
    r = ray(point(0, 0, -5), vector(0, 0, 1))
    s = Sphere()

    xs = s.intersect(r)

    assert all([
        xs.count == 2,
        xs[0].object is s,
        xs[1].object is s
    ])


def test_a_Spheres_default_transformation():
    s = Sphere()

    assert s.transform == Matrix.identity


def test_change_a_Spheres_transformation():
    s = Sphere()

    T = Matrix.identity.translate(2, 3, 4)

    s.transform = T

    assert s.transform == T


def test_intersecting_a_scaled_Sphere_with_a_ray():
    r = ray(point(0, 0, -5), vector(0, 0, 1))
    s = Sphere()

    s.transform = Matrix.identity.scale(2, 2, 2)
    xs = s.intersect(r)

    assert all([
        xs.count == 2,
        xs[0].t == 3,
        xs[1].t == 7
    ])


def test_intersecting_a_translated_Sphere_with_a_ray():
    r = ray(point(0, 0, -5), vector(0, 0, 1))
    s = Sphere()

    s.transform = Matrix.identity.translate(5, 0, 0)
    xs = s.intersect(r)

    assert xs.count == 0


def test_the_normal_on_a_Sphere_at_a_point_on_the_x_axis():
    s = Sphere()
    n = s.normal_at(point(1, 0, 0))

    assert n == vector(1, 0, 0)


def test_the_normal_on_a_Sphere_at_a_point_on_the_y_axis():
    s = Sphere()
    n = s.normal_at(point(0, 1, 0))

    assert n == vector(0, 1, 0)


def test_the_normal_on_a_Sphere_at_a_point_on_the_z_axis():
    s = Sphere()
    n = s.normal_at(point(0, 0, 1))

    assert n == vector(0, 0, 1)


def test_the_normal_on_a_Sphere_at_a_nonaxial_point():
    s = Sphere()
    r3 = (3 ** 0.5) / 3
    n = s.normal_at(point(r3, r3, r3))

    assert n == vector(r3, r3, r3)


def test_the_normal_is_a_normalised_vector():
    s = Sphere()
    r3 = (3 ** 0.5) / 3
    n = s.normal_at(point(r3, r3, r3))

    assert n == n.norm


def test_computing_the_normal_on_a_translated_Sphere():
    s = Sphere()
    T = Matrix.identity.translate(0, 1, 0)

    s.transform = T

    n = s.normal_at(point(0, 1.70711, -0.70711))

    assert n == vector(0, 0.70711, -0.70711)


def test_computing_the_normal_on_a_transformed_Sphere():
    s = Sphere()
    T = Matrix.identity.rotate('z', pi/5).scale(1, 0.5, 1)
    s.transform = T

    n = s.normal_at(point(0, (2 ** 0.5) / 2, -(2 ** 0.5) / 2))

    assert n == vector(0, 0.97014, -0.24254)


def test_a_Sphere_has_a_default_Material():
    s = Sphere()
    m = s.material

    assert m == Material()


def test_a_Sphere_may_be_assigned_a_Material():
    s = Sphere()
    m = Material()
    m.ambient = 1

    s.material = m
    assert s.material == m


