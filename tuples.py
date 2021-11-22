from functools import cached_property


class _tuple:
    """
    COORDINATE SYSTEM
    This implementation uses LEFT-HANDED coordinates.
    x-axis: positive to right
    y-axis: positive upwards
    z-axis: positive away
    """

    # Make access to the core variables significantly faster.
    __slots__ = ['x', 'y', 'z', 'w', '__dict__']

    def __init__(self, x, y, z, w):
        self.x = x
        self.y = y
        self.z = z
        self.w = w  # 0 for vectors, 1 for points.

    def __repr__(self):
        return f'_tuple({self.x}, {self.y}, {self.z}, {self.w})'

    def __eq__(self, other):
        # Required for floating-point comparisons.
        def nearly_equal(a, b):
            EPSILON = 0.0001
            return abs(a - b) < EPSILON

        return all((
            nearly_equal(self.x, other.x),
            nearly_equal(self.y, other.y),
            nearly_equal(self.z, other.z),
            nearly_equal(self.w, other.w)
        ))

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        z = self.z + other.z
        w = self.w + other.w

        if self.w == 1 and other.w == 1:
            raise ValueError('Cannot add two points.')

        return _tuple(x, y, z, w)

    def __sub__(self, other):
        if self.w == 0 and other.w == 1:
            raise ValueError('Cannot subtract a point from a vector.')

        return self + -other

    def __mul__(self, other):
        x = self.x
        y = self.y
        z = self.z
        w = self.w

        # Only implemented for scalar multiplication.
        if isinstance(other, (int, float)):
            return _tuple(x * other, y * other, z * other, w * other)

        if isinstance(other, _tuple):
            raise TypeError(
                'Cannot multiply _tuple and _tuple: Use .dot() or .cross().'
            )

    def __truediv__(self, other):
        # Only implemented for scalar division.
        x = self.x / other
        y = self.y / other
        z = self.z / other
        w = self.w / other

        return _tuple(x, y, z, w)

    def __neg__(self):
        x = -self.x
        y = -self.y
        z = -self.z
        w = -self.w

        return _tuple(x, y, z, w)

    @cached_property
    def magnitude(self):
        """ The length of a vector, also represented as |vector| """

        xx = self.x ** 2
        yy = self.y ** 2
        zz = self.z ** 2
        ww = self.w ** 2

        return (xx + yy + zz + ww) ** 0.5

    @cached_property
    def norm(self):
        """
        A vector normalised to magnitude 1.
        Allows us to keep calculations anchored to a common scale.
        """

        x = self.x
        y = self.y
        z = self.z
        w = self.w

        m = self.magnitude

        return _tuple(x / m, y / m, z / m, w / m)

    def dot(self, other):
        """
        The dot product is analogous to the angle between two vectors.
        The smaller the angle, the larger the dot product.
        For unit vectors, the dot product = the cos of the angle between them.
        """

        return (
            self.x * other.x +
            self.y * other.y +
            self.z * other.z +
            self.w * other.w
        )

    def reflect(self, normal):
        """
        Given a tuple and the normal of a surface,
          reflect the tuple as if it had bounced off the surface.
        """

        return self - normal * 2 * self.dot(normal)

    def cross(self, other):
        """
        The cross product produces a new vector
          that is perpendicular to the two input vectors.
        The order of operations is important here:
          a cross b = -(b cross a).
        NOTE: Only implemented for vectors, not tuples, as the
          4d cross product is significantly more complex
          and is not used in this project.
        """

        if self.w != 0:
            raise TypeError(
                'Cross product is only implemented for vectors where w=0'
            )

        s = self
        o = other

        return _tuple(
            s.y * o.z - s.z * o.y,
            s.z * o.x - s.x * o.z,
            s.x * o.y - s.y * o.x,
            w=0.0
        )


def vector(x, y, z):
    """
    Given x, y, z, return a _tuple where w=0.0.
    The w value indicates that this tuple represents a vector.
    """

    return _tuple(x, y, z, w=0.0)


def point(x, y, z):
    """
    Given x, y, z, return a _tuple where w=1.0.
    The w value indicates that this tuple represents a point.
    """

    return _tuple(x, y, z, w=1.0)


class colour(_tuple):
    """
    We inherit from _tuple to take advantage of the tuple arithmetic methods.
    Colours are not clamped or normalised by default.
    """

    def __init__(self, r, g, b):
        super().__init__(r, g, b, w=0)

    @property
    def r(self):
        return self.x

    @property
    def g(self):
        return self.y

    @property
    def b(self):
        return self.z

    def __repr__(self):
        return f'colour({self.r}, {self.g}, {self.b})'

    def __add__(self, other):
        r = self.r + other.r
        g = self.g + other.g
        b = self.b + other.b

        return colour(r, g, b)

    def __sub__(self, other):
        r = self.r - other.r
        g = self.g - other.g
        b = self.b - other.b

        return colour(r, g, b)

    def __mul__(self, other):
        """
        Multiplying a colour by a colour gives us the hadamard product.
        """

        if isinstance(other, colour):
            r = self.r * other.r
            g = self.g * other.g
            b = self.b * other.b

            return colour(r, g, b)

        if isinstance(other, (int, float)):
            r = self.r
            g = self.g
            b = self.b

            return colour(r * other, g * other, b * other)

    def __truediv__(self, other):
        r = self.r / other
        g = self.g / other
        b = self.b / other

        return colour(r, g, b)


colour.BLACK = colour(0, 0, 0)
colour.WHITE = colour(1, 1, 1)
