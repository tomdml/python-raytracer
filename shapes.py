from tuples import point, vector
from intersect import intersect, intersects
from matrix import Matrix
from materials import Material


class Shape():

    def __init__(
        self,
        transform=Matrix.identity,
        material=None,
    ):
        self.transform = transform
        self.material = material or Material()

    def __eq__(self, other):
        return all([
            type(self) == type(other),
            self.transform == other.transform,
            self.material == other.material,
        ])

    def intersect(self, ray):
        local_ray = ray.transform(self.transform.inverse)
        return intersects(
            *[
                intersect(t, self)
                for t in self._intersect(local_ray)
            ]
        )

    def normal_at(self, point):
        local_point = self.transform.inverse * point
        local_normal = self._normal_at(local_point)
        world_normal = self.transform.inverse.T * local_normal

        # Hack - If there's a transation in the transform, w will get changed.
        world_normal.w = 0

        return world_normal.norm


class Sphere(Shape):

    def _intersect(self, ray):
        """
        Given a sphere and a ray, determine whether the ray intersects.
        Shape.intersect converts the ray to world space.
        Wiki: Line-Sphere intersection
        """

        sphere_to_ray = ray.origin - point(0, 0, 0)

        a = ray.direction.dot(ray.direction)
        b = 2 * ray.direction.dot(sphere_to_ray)
        c = sphere_to_ray.dot(sphere_to_ray) - 1

        discriminant = b**2 - 4 * a * c

        if discriminant < 0:
            return intersects()

        t1 = (-b - discriminant**0.5) / (2 * a)
        t2 = (-b + discriminant**0.5) / (2 * a)

        return t1, t2

    def _normal_at(self, object_point):
        """
        Assuming the point is on the surface of the Sphere,
        calculate the normal at said point.
        """
        object_normal = object_point - point(0, 0, 0)

        return object_normal


class Plane(Shape):

    def _intersect(self, ray):
        """
        Given a plane and a ray, determine whether the ray intersects.
        Shape.intersect converts the ray to world space.
        """
        EPSILON = 0.000001

        if abs(ray.direction.y) < EPSILON:
            return intersects()

        return (-ray.origin.y / ray.direction.y,)

        # sphere_to_ray = ray.origin - point(0, 0, 0)

        # a = ray.direction.dot(ray.direction)
        # b = 2 * ray.direction.dot(sphere_to_ray)
        # c = sphere_to_ray.dot(sphere_to_ray) - 1

        # discriminant = b**2 - 4 * a * c

        # if discriminant < 0:
        #     return intersects()

        # t1 = (-b - discriminant**0.5) / (2 * a)
        # t2 = (-b + discriminant**0.5) / (2 * a)

        # return intersects(
        #         intersect(t1, self),
        #         intersect(t2, self)
        #     )

    def _normal_at(self, object_point):
        """
        The normal of the xz plane is always in the y direction.
        """

        return vector(0, 1, 0)
