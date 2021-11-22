from matrix import Matrix
from ray import ray
from tuples import point
from canvas import Canvas

from math import tan


class Camera:

    def __init__(self, hsize, vsize, field_of_view, transform=Matrix.identity):
        self.hsize = hsize
        self.vsize = vsize
        self.field_of_view = field_of_view
        self.transform = transform

    @property
    def pixel_size(self):
        half_view = tan(self.field_of_view/2)
        aspect = self.hsize / self.vsize

        if aspect >= 1:
            self.half_width = half_view
            self.half_height = half_view / aspect
        else:
            self.half_width = half_view * aspect
            self.half_height = half_view

        return (self.half_width * 2) / self.hsize

    def ray_for_pixel(self, px, py):
        # the offset from the edge of the canvas to the pixel's center
        x_offset = (px + 0.5) * self.pixel_size
        y_offset = (py + 0.5) * self.pixel_size

        # the untransformed coordinates of the pixel in world space
        # camera looks towards -z, so +x is to the left.
        world_x = self.half_width - x_offset
        world_y = self.half_height - y_offset

        # using the camera matrix, transform the canvas point and the origin
        # and then compute the ray's direction vector.
        pixel = self.transform.inverse * point(world_x, world_y, -1)
        origin = self.transform.inverse * point(0, 0, 0)
        direction = (pixel - origin).norm

        return ray(origin, direction)

    def render(self, world):
        image = Canvas(self.hsize, self.vsize)

        for y in range(self.vsize):
            for x in range(self.hsize):
                ray = self.ray_for_pixel(x, y)
                colour = world.colour_at(ray)
                image.write_pixel(x, y, colour)

        return image

