from world import World, default_world
from tuples import point, colour, vector
from shapes import Sphere, Plane
from matrix import Matrix
from materials import Material
from lights import point_light
from ray import ray
from intersect import intersect


def root(n):
    return n ** 0.5


def test_creating_a_world():
    world = World()

    assert all([
        world.objects == [],
        world.lights == []
    ])


def test_the_default_world():
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

    w = default_world()

    assert all([
        w.lights == [light],
        s1 in w,
        s2 in w
    ])


def test_intersect_a_world_with_a_ray():
    w = default_world()
    r = ray(point(0, 0, -5), vector(0, 0, 1))

    xs = w.intersect_world(r)

    assert all([
        xs.count == 4,
        xs[0].t == 4,
        xs[1].t == 4.5,
        xs[2].t == 5.5,
        xs[3].t == 6
    ])


def test_shading_an_intersection():
    w = default_world()
    r = ray(point(0, 0, -5), vector(0, 0, 1))
    shape = w[0]
    i = intersect(4, shape)

    comps = i.prepare_computations(r)
    c = w.shade_hit(comps)

    assert c == colour(0.38066, 0.47583, 0.2855)


def test_shading_an_intersection_from_the_inside():
    w = default_world()
    w.lights[0] = point_light(point(0, 0.25, 0), colour(1, 1, 1))
    r = ray(point(0, 0, 0), vector(0, 0, 1))
    shape = w[1]
    i = intersect(0.5, shape)

    comps = i.prepare_computations(r)
    c = w.shade_hit(comps)

    assert c == colour(0.90498, 0.90498, 0.90498)


def test_the_colour_when_a_ray_misses():
    w = default_world()
    r = ray(point(0, 0, -5), vector(0, 1, 0))

    c = w.colour_at(r)

    assert c == colour(0, 0, 0)


def test_the_colour_when_the_ray_hits():
    w = default_world()
    r = ray(point(0, 0, -5), vector(0, 0, 1))

    c = w.colour_at(r)

    assert c == colour(0.38066, 0.47583, 0.2855)


def test_the_colour_with_an_intersection_behind_the_ray():
    w = default_world()
    outer = w[0]
    outer.material.ambient = 1
    inner = w[1]
    inner.material.ambient = 1
    r = ray(point(0, 0, 0.75), vector(0, 0, -1))

    c = w.colour_at(r)

    assert c == inner.material.colour


def test_no_shadow_when_nothing_is_collinear_with_point_and_light():
    w = default_world()
    p = point(0, 10, 0)

    assert w.is_shadowed(p, w.lights[0]) is False


def test_the_shadow_when_an_object_is_beween_the_point_and_the_light():
    w = default_world()
    p = point(10, -10, 10)

    assert w.is_shadowed(p, w.lights[0])


def test_there_is_no_shadow_when_an_object_is_behind_the_light():
    w = default_world()
    p = point(-20, 20, -20)

    assert w.is_shadowed(p, w.lights[0]) is False


def test_there_is_no_shadow_when_the_object_is_behind_the_point():
    w = default_world()
    p = point(-2, 2, -2)

    assert w.is_shadowed(p, w.lights[0]) is False


def test_shade_hit_is_given_an_intersection_in_shadow():
    lights = [
        point_light(point(0, 0, -10), colour(1, 1, 1))
    ]

    objects = [
        Sphere(),
        Sphere(transform=Matrix.translate(0, 0, 10))
    ]

    w = World(objects=objects, lights=lights)

    r = ray(point(0, 0, 5), vector(0, 0, 1))
    i = intersect(4, objects[1])

    comps = i.prepare_computations(r)
    c = w.shade_hit(comps)

    assert c == colour(0.1, 0.1, 0.1)


def test_the_reflected_colour_for_a_reflective_material():
    w = default_world()
    shape = Plane(
        material=Material(reflective=0.5),
        transform=Matrix.translate(0, -1, 0)
    )
    w.objects.append(shape)

    r = ray(point(0, 0, -3), vector(0, -root(2)/2, root(2)/2))
    i = intersect(root(2), shape)

    comps = i.prepare_computations(r)
    c = w.reflected_colour(comps)

    assert c == colour(0.19032, 0.2379, 0.14274)


def test_shade_hit_with_a_reflective_material():
    w = default_world()
    shape = Plane(
        material=Material(reflective=0.5),
        transform=Matrix.translate(0, -1, 0)
    )
    w.objects.append(shape)

    r = ray(point(0, 0, -3), vector(0, -root(2)/2, root(2)/2))
    i = intersect(root(2), shape)

    comps = i.prepare_computations(r)
    c = w.shade_hit(comps)

    assert c == colour(0.87677, 0.92436, 0.82918)
