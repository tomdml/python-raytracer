import subprocess
import tempfile
from math import pi
from datetime import datetime

from tuples import point, colour, vector
from matrix import Matrix
from canvas import Canvas
from shapes import Sphere, Plane
from ray import ray
from materials import Material
from lights import point_light
from world import World, default_world
from camera import Camera
from patterns import *
from patterns import _TestPattern

import random

from PIL import Image
import numpy as np


def random_colour():
    return colour(random.random(), random.random(), random.random())


lights = [
    point_light(point(0, 10, -10), colour(1, 1, 1))
]

objects = [
    Plane(
        material=Material(
            reflective=0.6,
            pattern=StripePattern()
        )
    ),
    Sphere(
        transform=Matrix.translate(-1.2, 1, 0),
        material=Material(reflective=0.8)
    ),
    Sphere(
        transform=Matrix.translate(1.2, 1, 0),
        material=Material(
            reflective=0.8,
            pattern=StripePattern(colour(1, 1, 0), colour(1, 0, 0)))
    )
]

world = World(objects=objects, lights=lights)

camera = Camera(
    400,
    400,
    pi/3,
    transform=Matrix.view_transform(
        point(0, 1, -4), point(0, 1, 0), vector(0, 1, 0)
    )
)

time = datetime.now()
canvas = camera.render(world)
print(f'Finished in: {datetime.now() - time}')

ppm = canvas.to_ppm()
with tempfile.NamedTemporaryFile(mode='w+', suffix='.ppm') as fp:
    fp.write(ppm)
    subprocess.run(['open', '-W', fp.name])
