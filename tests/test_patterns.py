from tuples import colour, point
from patterns import *
from patterns import _TestPattern
from shapes import Sphere
from matrix import Matrix
from materials import Material

import pytest


@pytest.fixture(autouse=True)
def black():
    return colour.BLACK


@pytest.fixture(autouse=True)
def white():
    return colour.WHITE


def test_creating_a_stripe_pattern():
    pattern = StripePattern(white, black)

    assert pattern.a == white and pattern.b == black


def test_a_stripe_pattern_is_constant_in_y():
    pattern = StripePattern(white, black)

    assert all([
        pattern.colour_at(point(0, 0, 0)) == white,
        pattern.colour_at(point(0, 1, 0)) == white,
        pattern.colour_at(point(0, 2, 0)) == white
    ])


def test_a_stripe_pattern_is_constant_in_z():
    pattern = StripePattern(white, black)

    assert all([
        pattern.colour_at(point(0, 0, 0)) == white,
        pattern.colour_at(point(0, 0, 1)) == white,
        pattern.colour_at(point(0, 0, 2)) == white
    ])


def test_a_stripe_pattern_alternates_in_x():
    pattern = StripePattern(white, black)

    assert all([
        pattern.colour_at(point(0, 0, 0)) == white,
        pattern.colour_at(point(0.9, 0, 0)) == white,
        pattern.colour_at(point(1, 0, 0)) == black,
        pattern.colour_at(point(-0.1, 0, 0)) == black,
        pattern.colour_at(point(-1, 0, 0)) == black,
        pattern.colour_at(point(-1.1, 0, 0)) == white
    ])


def test_a_stripe_with_an_object_transformation():
    s = Sphere(
        transform=Matrix.scale(2, 2, 2),
        material=Material(
            pattern=StripePattern(colour.WHITE, colour.BLACK)
        )
    )

    c = s.material.pattern.colour_at_object(s, point(1.5, 0, 0))

    assert c == colour.WHITE


def test_a_stripe_with_a_pattern_transformation():
    s = Sphere(
        material=Material(
            pattern=StripePattern(
                colour.WHITE,
                colour.BLACK,
                transform=Matrix.scale(2, 2, 2)
            ),
        )
    )

    assert s.material.pattern.colour_at_object(s, point(1.5, 0, 0)) == colour.WHITE


def test_stripes_with_both_an_object_and_pattern_transform():
    s = Sphere(
        transform=Matrix.scale(2, 2, 2),
        material=Material(
            pattern=StripePattern(
                colour.WHITE,
                colour.BLACK,
                transform=Matrix.translate(0.5, 0, 0)
            )
        )
    )

    assert s.material.pattern.colour_at_object(s, point(2.5, 0, 0)) == colour.WHITE


def test_the_default_pattern_transformation():
    p = _TestPattern()
    assert p.transform == Matrix.identity


def test_aligning_a_transformation():
    p = _TestPattern(transform=Matrix.translate(1, 2, 3))

    assert p.transform == Matrix.translate(1, 2, 3)


def test_a_testpattern_with_an_object_transformation():
    s = Sphere(
        transform=Matrix.scale(2, 2, 2),
        material=Material(
            pattern=_TestPattern()
        )
    )

    c = s.material.pattern.colour_at_object(s, point(2, 3, 4))

    assert c == colour(1, 1.5, 2)


def test_a_testpattern_with_a_pattern_transformation():
    s = Sphere(
        material=Material(
            pattern=_TestPattern(
                transform=Matrix.scale(2, 2, 2)
            )
        )
    )

    c = s.material.pattern.colour_at_object(s, point(2, 3, 4))

    assert c == colour(1, 1.5, 2)


def test_a_testpattern_with_a_pattern_and_object_transformation():
    s = Sphere(
        transform=Matrix.scale(2, 2, 2),
        material=Material(
            pattern=_TestPattern(
                transform=Matrix.translate(0.5, 1, 1.5)
            )
        )
    )

    c = s.material.pattern.colour_at_object(s, point(2.5, 3, 3.5))

    assert c == colour(0.75, 0.5, 0.25)


def test_a_gradientpattern_linearly_interpolates_between_colours():
    p = GradientPattern(colour.WHITE, colour.BLACK)

    assert all([
        p.colour_at(point(0, 0, 0)) == colour.WHITE,
        p.colour_at(point(0.25, 0, 0)) == colour(0.75, 0.75, 0.75),
        p.colour_at(point(0.5, 0, 0)) == colour(0.5, 0.5, 0.5),
        p.colour_at(point(0.75, 0, 0)) == colour(0.25, 0.25, 0.25),
    ])


def test_a_ringpattern_should_extend_in_both_x_and_z():
    p = RingPattern(colour.WHITE, colour.BLACK)

    assert all([
        p.colour_at(point(0, 0, 0)) == colour.WHITE,
        p.colour_at(point(1, 0, 0)) == colour.BLACK,
        p.colour_at(point(0, 0, 1)) == colour.BLACK,
        p.colour_at(point(0.708, 0, 0.708)) == colour.BLACK
    ])


def test_a_checkers_pattern_repeats_in_x():
    pattern = CheckersPattern(white, black)

    assert all([
        pattern.colour_at(point(0, 0, 0)) == white,
        pattern.colour_at(point(0.99, 0, 0)) == white,
        pattern.colour_at(point(1.01, 0, 0)) == black
    ])


def test_a_checkers_pattern_repeats_in_y():
    pattern = CheckersPattern(white, black)

    assert all([
        pattern.colour_at(point(0, 0, 0)) == white,
        pattern.colour_at(point(0, 0.99, 0)) == white,
        pattern.colour_at(point(0, 1.01, 0)) == black
    ])


def test_a_checkers_pattern_repeats_in_z():
    pattern = CheckersPattern(white, black)

    assert all([
        pattern.colour_at(point(0, 0, 0)) == white,
        pattern.colour_at(point(0, 0, 0.99)) == white,
        pattern.colour_at(point(0, 0, 1.01)) == black
    ])
