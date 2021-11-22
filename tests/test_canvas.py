from canvas import Canvas
from tuples import colour


def test_creating_a_canvas():
    c = Canvas(10, 20)

    assert all(
        pixel == colour(0, 0, 0)
        for row in c.pixels
        for pixel in row
    ) and all([c.width == 10, c.height == 20])


def test_writing_to_canvas():
    c = Canvas(10, 20)
    red = colour(1, 0, 0)

    c.write_pixel(2, 3, red)

    assert c.pixel_at(2, 3) is red


def test_construct_ppm_header():
    c = Canvas(5, 3)

    assert c.to_ppm().splitlines()[:3] == [
        "P3",
        "5 3",
        "255"
    ]


def test_construct_ppm_body():
    c = Canvas(5, 3)

    c1 = colour(1.5, 0, 0)
    c2 = colour(0, 0.5, 0)
    c3 = colour(-0.5, 0, 1)

    c.write_pixel(0, 0, c1)
    c.write_pixel(2, 1, c2)
    c.write_pixel(4, 2, c3)

    assert c.to_ppm().splitlines()[3:] == [
        "255 0 0 0 0 0 0 0 0 0 0 0 0 0 0",
        "0 0 0 0 0 0 0 128 0 0 0 0 0 0 0",
        "0 0 0 0 0 0 0 0 0 0 0 0 0 0 255"
    ]


def test_ppm_ends_with_newline():
    c = Canvas(1, 1)

    assert c.to_ppm().endswith('\n')
