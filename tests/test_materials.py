from materials import Material
from tuples import colour, point, vector
from lights import point_light
from patterns import StripePattern
from shapes import Sphere

import pytest


@pytest.fixture
def m():
    return Material()


@pytest.fixture
def position():
    return point(0, 0, 0)


def test_the_default_Material():
    m = Material()

    assert all([
        m.colour == colour(1, 1, 1),
        m.ambient == 0.1,
        m.diffuse == 0.9,
        m.specular == 0.9,
        m.shininess == 200
    ])


def test_lighting_with_the_eye_between_the_light_and_the_surface(m, position):
    eyev = vector(0, 0, -1)
    normalv = vector(0, 0, -1)
    light = point_light(point(0, 0, -10), colour(1, 1, 1))

    result = m.lighting(Sphere(), light, position, eyev, normalv, False)

    assert result == colour(1.9, 1.9, 1.9)


def test_lighting_with_the_eye_between_light_and_surface_eye_offset_45deg(m, position):
    eyev = vector(0, (2 ** 0.5) / 2, -(2 ** 0.5) / 2)
    normalv = vector(0, 0, -1)
    light = point_light(point(0, 0, -10), colour(1, 1, 1))

    result = m.lighting(Sphere(), light, position, eyev, normalv, False)

    assert result == colour(1.0, 1.0, 1.0)


def test_lighting_with_eye_opposite_surface_light_offset_45deg(m, position):
    eyev = vector(0, 0, -1)
    normalv = vector(0, 0, -1)
    light = point_light(point(0, 10, -10), colour(1, 1, 1))

    result = m.lighting(Sphere(), light, position, eyev, normalv, False)

    assert result == colour(0.7364, 0.7364, 0.7364)


def test_lighting_with_eye_in_path_of_reflection_vector(m, position):
    eyev = vector(0, -(2 ** 0.5) / 2, -(2 ** 0.5) / 2)
    normalv = vector(0, 0, -1)
    light = point_light(point(0, 10, -10), colour(1, 1, 1))

    result = m.lighting(Sphere(), light, position, eyev, normalv, False)

    assert result == colour(1.6364, 1.6364, 1.6364)


def test_lighting_with_the_light_behind_the_surface(m, position):
    eyev = vector(0, 0, -1)
    normalv = vector(0, 0, -1)
    light = point_light(point(0, 0, 10), colour(1, 1, 1))

    result = m.lighting(Sphere(), light, position, eyev, normalv, False)

    assert result == colour(0.1, 0.1, 0.1)


def test_lighting_with_the_surface_in_shadow(m, position):
    eyev = vector(0, 0, -1)
    normalv = vector(0, 0, -1)
    light = point_light(point(0, 10, -10), colour(1, 1, 1))
    in_shadow = True

    result = m.lighting(Sphere(), light, position, eyev, normalv, True)

    assert result == colour(0.1, 0.1, 0.1)


def test_lighting_with_a_pattern_applied():
    m = Material(
            pattern=StripePattern(colour(1, 1, 1), colour(0, 0, 0)),
            ambient=1,
            diffuse=0,
            specular=0
        )

    eyev = vector(0, 0, -1)
    normalv = vector(0, 0, -1)
    light = point_light(point(0, 10, -10), colour(1, 1, 1))

    c1 = m.lighting(Sphere(), light, point(0.9, 0, 0), eyev, normalv, False)
    c2 = m.lighting(Sphere(), light, point(1.1, 0, 0), eyev, normalv, False)

    assert c1 == colour(1, 1, 1) and c2 == colour(0, 0, 0)


def test_reflectivity_for_the_default_material():
    m = Material()

    assert m.reflective == 0.0
