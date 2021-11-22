from tuples import colour


class Material:

    def __init__(
        self,
        colour=colour(1, 1, 1),
        ambient=0.1,
        diffuse=0.9,
        specular=0.9,
        shininess=200,
        reflective=0.0,
        pattern=None
    ):
        self.colour = colour
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
        self.shininess = shininess
        self.reflective = reflective
        self.pattern = pattern

    def __eq__(self, other):
        return all([
            self.colour == other.colour,
            self.ambient == other.ambient,
            self.diffuse == other.diffuse,
            self.specular == other.specular,
            self.shininess == other.shininess,
            self.reflective == other.reflective,
            self.pattern == other.pattern
        ])

    def lighting(self, _object, light, point, eyev, normalv, in_shadow):
        """
        Calculates the overall colour of a material.
        """

        if self.pattern is not None:
            colour = self.pattern.colour_at_object(_object, point)
        else:
            colour = self.colour

        black = colour.BLACK

        # combine the surface colour with the light's colour
        effective_colour = colour * light.intensity

        # calculate the ambient contribution
        ambient = effective_colour * self.ambient

        # exit early if in shadow
        if in_shadow:
            return ambient

        # find the direction of the light source
        lightv = (light.position - point).norm

        # light_dot_normal represents the cosine of the angle between the
        # light vector and the normal vector. A negative number means the
        # light is on the other side of the surface.
        light_dot_normal = lightv.dot(normalv)

        if light_dot_normal < 0:
            diffuse = black
            specular = black
        else:
            # compute the diffuse contribution
            diffuse = effective_colour * self.diffuse * light_dot_normal

            # reflect_dot_eye represents the cosine of the angle between the
            # reflection vector and the eye vector. A negative number means the
            # light reflects away from the eye.
            reflectv = (-lightv).reflect(normalv)
            reflect_dot_eye = reflectv.dot(eyev)

            if reflect_dot_eye <= 0:
                specular = black
            else:
                # compute the specular contribution
                factor = reflect_dot_eye ** self.shininess
                specular = light.intensity * self.specular * factor

        return ambient + diffuse + specular
