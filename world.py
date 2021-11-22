from tuples import point, colour
from shapes import Sphere
from matrix import Matrix
from materials import Material
from lights import point_light
from intersect import intersects, intersect
from ray import ray


class World:

    def __init__(self, objects=None, lights=None):
        self.objects = objects or []
        self.lights = lights or []

    def __iter__(self):
        return iter(self.objects)

    def __getitem__(self, key):
        return self.objects[key]

    def intersect_world(self, ray):
        return intersects(*[i for obj in self for i in obj.intersect(ray)])

    def shade_hit(self, comps):
        return sum(
            (
                comps.object.material.lighting(
                    comps.object,
                    light,
                    comps.point,
                    comps.eyev,
                    comps.normalv,
                    self.is_shadowed(comps.over_point, light)
                ) + self.reflected_colour(comps)
                for light in self.lights
            ),
            start=colour(0, 0, 0)
        )

    def colour_at(self, ray):
        xs = self.intersect_world(ray)

        if not xs.hit:
            return colour(0, 0, 0)

        comps = xs.hit.prepare_computations(ray)

        return self.shade_hit(comps)

    def is_shadowed(self, point, light):
        v = light.position - point
        distance = v.magnitude
        direction = v.norm

        r = ray(point, direction)
        xs = self.intersect_world(r)

        h = xs.hit

        return bool(h and h.t < distance)

    def reflected_colour(self, comps):
        if comps.object.material.reflective == 0:
            return colour(0, 0, 0)

        reflect_ray = ray(comps.over_point, comps.reflectv)
        c = self.colour_at(reflect_ray)

        return c * comps.object.material.reflective


def default_world():
    light = point_light(
        point(-10, 10, -10),
        colour(1, 1, 1)
    )
    s1 = Sphere(material=Material(
        colour=colour(0.8, 1.0, 0.6),
        diffuse=0.7,
        specular=0.2
    ))
    s2 = Sphere(transform=Matrix.identity.scale(0.5, 0.5, 0.5))

    return World(objects=[s1, s2], lights=[light])
