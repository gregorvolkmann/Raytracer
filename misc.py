# -*- coding: utf-8 -*-

from objects import Vector

class Color(object):
    def __init__(self, r, g, b):
        self.r = int(r)
        self.g = int(g)
        self.b = int(b)

    def __add__(self, c):
        return Color(self.r+c.r, self.g+c.g, self.b+c.b)

    def __mul__(self, k):
        return Color(self.r*k, self.g*k, self.b*k)

    def intensity(self):
        i = (self.r+self.g+self.b) / 3
        return Color(i, i, i)

    def rgb(self):
        return (int(self.r), int(self.g), int(self.b))

class Material(object):
    def __init__(self, base_color, ambient_coefficient, diffuse_coefficient, specular_coefficient, roughness=32):
        self.base_color = base_color
        self.roughness = roughness
        self.ambient_coefficient = ambient_coefficient
        self.diffuse_coefficient = diffuse_coefficient
        self.specular_coefficient = specular_coefficient

    def baseColourAt(self, p):
        return self.base_color

class CheckerboardMaterial(Material):
    def __init__(self, base_color, ambient_coefficient, diffuse_coefficient, specular_coefficient, other_color, checkSize):
        Material.__init__(self, base_color, ambient_coefficient, diffuse_coefficient, specular_coefficient)
        self.other_color = other_color
        self.checkSize = checkSize

    def baseColourAt(self, p):
        v = Vector(p.x, p.y, p.z)
        v.scale(1.0 / self.checkSize)
        if (int(abs(v.x)+0.5) + int(abs(v.y)+0.5) + int(abs(v.z)+0.5)) % 2:
            return self.other_color
        return self.base_color
