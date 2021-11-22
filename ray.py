class ray:

    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction

    def position(self, t):
        """
        Calculates the position of the ray at time t from the origin and
        direction.
        """

        return self.origin + self.direction * t

    def transform(self, M):
        """
        Makes the ray transformable with a transformation Matrix M.
        """

        origin = M * self.origin
        direction = M * self.direction

        return ray(origin, direction)
