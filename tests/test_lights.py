from tuples import colour, point
from lights import point_light


def test_a_point_light_has_a_position_and_intensity():
    intensity = colour(1, 1, 1)
    position = point(0, 0, 0)
    light = point_light(position, intensity)

    assert light.position == position and light.intensity == intensity
