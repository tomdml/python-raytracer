from tuples import colour


class Canvas:
    """
    The Canvas is a rectangular grid of pixels with configurable size.
    The canvas is initialised with all pixels being black (0, 0, 0).
    """

    def __init__(self, width, height):
        self.width = width
        self.height = height

        # Initialise the pixel grid. All pixels start as black.
        self.pixels = [
            [colour(0, 0, 0) for _ in range(width)]
            for _ in range(height)
        ]

    def write_pixel(self, x, y, pixel):
        # We can only write to an integer location.
        x = round(x)
        y = round(y)

        # The location has to be inside the drawing area.
        if 0 <= x < self.width and 0 <= y < self.height:
            self.pixels[y][x] = pixel

    def pixel_at(self, x, y):
        return self.pixels[y][x]

    def to_ppm(self):
        """
        Represents the canvas in PPM format, as a string.
        This string can then be saved to a tempfile and displayed.
        """

        MAXIMUM_COLOUR_VALUE = 255

        PPM_HEADER = (
            "P3",
            f"{self.width} {self.height}",
            f"{MAXIMUM_COLOUR_VALUE}"
        )

        # The canvas object is responsible for serialising the colour objects.
        def colour_to_rgb(colour):

            def clamp(value, lo=0, hi=MAXIMUM_COLOUR_VALUE):
                if value < lo:
                    return lo

                if value > hi:
                    return hi

                return value

            r = clamp(round(colour.r * MAXIMUM_COLOUR_VALUE))
            g = clamp(round(colour.g * MAXIMUM_COLOUR_VALUE))
            b = clamp(round(colour.b * MAXIMUM_COLOUR_VALUE))

            return f'{r} {g} {b}'

        ppm_body = (
            ' '.join(colour_to_rgb(colour) for colour in row)
            for row in self.pixels
        )

        return '\n'.join((*PPM_HEADER, *ppm_body)) + '\n'
