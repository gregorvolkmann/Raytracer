# -*- coding: utf-8 -*-

import math

class Point(object):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return 'Point(%s,%s,%s)' % (self.x, self.y, self.z)

    def __add__(self, vector):
        return Point(self.x+vector.x, self.y+vector.y, self.z+vector.z)

    def __sub__(self, point):
        return Vector(self.x-point.x, self.y-point.y, self.z-point.z)

class Vector(Point):
    def __repr__(self):
        return 'Vector(%s,%s,%s)' % (self.x, self.y, self.z)

    # http://www.mathe-online.at/materialien/ursl/files/Rechnen.html
    def __add__(self, vector):
        return Vector(self.x+vector.x, self.y+vector.y, self.z+vector.z)

    def __mul__(self, n):
        return Vector(self.x*n, self.y*n, self.z*n)

    # http://www.lernort-mint.de/Mathematik/Vektoren/vektoren_division.html
    def __div__(self, n):
        return Vector(self.x/n, self.y/n, self.z/n)

    # skalarprodukt ⟨⟩
    def dot(self, v):
        return self.x*v.x + self.y*v.y + self.z*v.z

    def length(self):
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

    # http://massmatics.de/merkzettel/index.php#!339:Vektoren_normieren
    def normalized(self):
        return Vector(self.x/self.length(), self.y/self.length(), self.z/self.length())

    def scale(self, t):
        return Vector(self.x*t, self.y*t, self.z*t)

    # https://www.youtube.com/watch?v=UzWnp97GN9g
    def cross(self, v):
        return Vector(
            self.y*v.z - self.z*v.y,
            self.z*v.x - self.x*v.z,
            self.x*v.y - self.y*v.x,
        )

    # Script Seite 48
    def mirror(self, v):
        return self-v*self.dot(v)*2

class Color(object):
    def __init__(self, r, g, b):
        self.r = int(r)
        self.g = int(g)
        self.b = int(b)

    # FRAGEN
    # https://www.youtube.com/watch?v=LKnqECcg6Gw
    def __add__(self, c):
        return Color(self.r+c.r, self.g+c.g, self.b+c.b)

    def __mul__(self, k):
        return Color(self.r*k, self.g*k, self.b*k)

    def __div__(self, k):
        return Color(self.r/k, self.g/k, self.b/k)

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
    def __init__(self, base_color, ambient_coefficient, diffuse_coefficient, specular_coefficient, roughness, other_color, checkSize):
        Material.__init__(self, base_color, ambient_coefficient, diffuse_coefficient, specular_coefficient)
        self.other_color = other_color
        self.checkSize = checkSize

    def baseColourAt(self, p):
        v = Vector(p.x, p.y, p.z)
        v.scale(1.0 / self.checkSize)
        if (int(abs(v.x)+0.5) + int(abs(v.y)+0.5) + int(abs(v.z)+0.5)) % 2:
            return self.other_color
        return self.base_color
