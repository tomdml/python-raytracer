from matrix import Matrix
from tuples import colour

from math import floor


class Pattern:
    """
    #TODO: Patterns are implemented as if they are 'cut out' of 3d shapes with
    the given pattern. For more realistic surface mapped patterns,
    we'll need to implement UV mapping, which is a method to convert
    3D (x, y, z) points to 2D (u, v) coordinates.
    """

    def __init__(
        self,
        a=colour(1, 1, 1),
        b=colour(0, 0, 0),
        transform=Matrix.identity
    ):
        self.a = a
        self.b = b
        self.transform = transform

    def colour_at_object(self, _object, world_point):
        object_point = _object.transform.inverse * world_point

        return self.colour_at_point(object_point)

    def colour_at_point(self, object_point):
        local_point = self.transform.inverse * object_point

        c = self.colour_at(local_point)
        return c if isinstance(c, colour) else c.colour_at_point(local_point)


class StripePattern(Pattern):

    def colour_at(self, point):
        return self.a if floor(point.x) % 2 == 0 else self.b


class GradientPattern(Pattern):

    def colour_at(self, point):
        distance = self.b - self.a
        fraction = point.x - floor(point.x)

        return self.a + distance * fraction


class RingPattern(Pattern):

    def colour_at(self, point):
        return (
            self.a
            if floor(
                ((point.x ** 2) + (point.z ** 2)) ** 0.5
            ) % 2 == 0
            else self.b
        )


class RadialGradientPattern(Pattern):

    def colour_at(self, point):
        distance = self.b - self.a
        fraction = (((point.x ** 2) + (point.z ** 2)) ** 0.5) % 2

        return (
            self.a + distance * fraction
            if floor(fraction) == 0
            else self.a + distance * fraction
        )


class CheckersPattern(Pattern):

    def colour_at(self, point):
        return (
            self.a
            if (floor(point.x) + floor(point.y) + floor(point.z)) % 2 == 0
            else self.b
        )


class ImagePattern(Pattern):

    def colour_at(self, point):
        h = len(self.a)
        w = len(self.a[0])

        return self.a[floor((point.y + 1)/2 * -h)][floor((point.x + 1)/2 * w)]


class BlendedPattern(Pattern):

    def colour_at(self, point):
        return (
            self.a.colour_at_point(point) + self.b.colour_at_point(point)
        ) / 2


class _TestPattern(Pattern):

    def colour_at(self, point):
        return colour(point.x, point.y, point.z)
