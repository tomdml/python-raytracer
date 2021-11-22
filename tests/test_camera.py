from camera import Camera
from matrix import Matrix
from tuples import point, vector, colour
from world import default_world

from math import pi

import pytest


def root(n):
    return n ** 0.5


def test_constructing_a_camera():
    hsize = 160
    vsize = 120
    field_of_view = pi/2

    c = Camera(hsize, vsize, field_of_view)

    assert all([
        c.hsize == 160,
        c.vsize == 120,
        c.field_of_view == pi/2,
        c.transform == Matrix.identity
    ])


def test_the_pixel_size_for_a_horizontal_canvas():
    c = Camera(200, 125, pi/2)

    assert c.pixel_size == pytest.approx(0.01)


def test_the_pixel_size_for_a_vertical_canvas():
    c = Camera(125, 200, pi/2)

    assert c.pixel_size == pytest.approx(0.01)


def test_constructing_a_ray_through_the_center_of_the_canvas():
    c = Camera(201, 101, pi/2)

    r = c.ray_for_pixel(100, 50)

    assert all([
        r.origin == point(0, 0, 0),
        r.direction == vector(0, 0, -1)
    ])


def test_constructing_a_ray_through_a_corner_of_the_canvas():
    c = Camera(201, 101, pi/2)

    r = c.ray_for_pixel(0, 0)

    assert all([
        r.origin == point(0, 0, 0),
        r.direction == vector(0.66519, 0.33259, -0.66851)
    ])


def test_constructing_a_ray_when_the_camera_is_transformed():
    c = Camera(201, 101, pi/2)
    c.transform = Matrix.translate(0, -2, 5).rotate('y', pi/4)

    r = c.ray_for_pixel(100, 50)

    assert all([
        r.origin == point(0, 2, -5),
        r.direction == vector(root(2)/2, 0, -root(2)/2)
    ])


def test_rendering_a_world_with_a_camera():
    w = default_world()
    c = Camera(11, 11, pi/2)

    _from = point(0, 0, -5)
    to = point(0, 0, 0)
    up = vector(0, 1, 0)

    c.transform = Matrix.view_transform(_from, to, up)

    image = c.render(w)

    assert image.pixel_at(5, 5) == colour(0.38066, 0.47583, 0.2855)
