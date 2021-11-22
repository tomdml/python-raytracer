from operator import attrgetter
from collections import namedtuple


class intersect:
    """
    The intersect class stores data about a single intersection
      between a surface and a ray.
    """

    def __init__(self, t, obj):
        self.t = t
        self.object = obj

    def prepare_computations(self, ray):
        """
        Create a namedtuple for storing precomputed values relating
          to the intersection.
        """

        Comps = namedtuple('Comps', 't object point eyev normalv inside over_point reflectv')

        point = ray.position(self.t)
        normalv = self.object.normal_at(point)

        inside = normalv.dot(-ray.direction) < 0

        if inside:
            normalv = -normalv

        EPSILON = 0.00001
        over_point = point + normalv * EPSILON

        reflectv = ray.direction.reflect(normalv)

        comps = Comps(
            # Retain the intersection's properties for convenience
            t=self.t,
            object=self.object,

            # Store some useful values
            point=point,
            eyev=-ray.direction,
            normalv=normalv,
            inside=inside,
            over_point=over_point,
            reflectv=reflectv
        )

        return comps


class intersects:

    def __init__(self, *_intersects):
        self._intersects = sorted(_intersects, key=attrgetter('t'))

    def __iter__(self):
        return iter(self._intersects)

    def __bool__(self):
        return bool(self.count)

    @property
    def count(self):
        return len(self._intersects)

    @property
    def hit(self):
        """
        Returns the lowest non-negative intersect in intersects, or None
        """

        # todo: should it be > 0 or >= 0?
        positive_t = [i for i in self if i.t > 0]

        if positive_t:
            return min(positive_t, key=attrgetter('t'))

    def __getitem__(self, key):
        return self._intersects[key]
