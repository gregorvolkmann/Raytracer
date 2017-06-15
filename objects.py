# -*- coding: utf-8 -*-import mathfrom misc import *class Light(object):    def __init__(self, intensity):        self.intensity = intensity    def __repr__(self):        return 'Light(%s)' % (self.intensity)class PointLight(Point, Light):    def __init__(self, x, y, z, color):        self.color = color        Point.__init__(self, x, y, z)        Light.__init__(self, (x+y+z)/3)    def __repr__(self):        return 'PointLight(%s, %s)' % (Point.__repr__(self), self.intensity)class Ray(object):    def __init__(self, origin, direction):        self.origin = origin # point        self.direction = direction.normalized() # vector    def __repr__(self):        return 'Ray(%s,%s)' % (repr(self.origin), repr(self.direction))    def pointAtParameter(self, t):        return self.origin + self.direction.scale(t)class Camera(object):    def __init__(self, e, c, up, fov, image_width, image_height):        self.e = e      # camera point (eye)        self.c = c      # center point (center)        self.up = up    # camera up vector        self.fov = fov  # fieldofview (brennweite?)        self.f = (self.c-self.e) / (self.c-self.e).length()        self.s = (self.f.cross(self.up)) / self.f.cross(self.up).length()        self.u = self.s.cross(self.f)        self.alpha = self.fov / 2        self.height = 2 * math.tan(math.radians(self.alpha))        self.width = (image_width / image_height) * self.height        self.pixel_height = self.height / (image_height-1)        self.pixel_width = self.width / (image_width-1)    def __repr__(self):        return '''Camera(\n            e=%s,            c=%s,            up=%s,            fov=%s,            width=%s,            height=%s        )''' % (self.e, self.c, self.up, self.fov, self.width, self.height)class MaterialObject(object):    def __init__(self, material):        self.material = materialclass Plane(MaterialObject):    def __init__(self, point, normal, material):        self.point = point # point        self.normal = normal.normalized() # vector        MaterialObject.__init__(self, material)    def __repr__(self):        return 'Plane(%s,%s)' % (repr(self.point), repr(self.normal))    def intersectionParameter(self, ray):        op = ray.origin - self.point        a = op.dot(self.normal)        b = ray.direction.dot(self.normal)        if b:            return -a/b # t for e        else:            return None    def normalAt(self, p):        return self.normal    def colorAt(self, ray):        return self.material.baseColourAt(ray.pointAtParameter(self.intersectionParameter(ray)))class Sphere(MaterialObject):    def __init__(self, center, radius, material):        self.center = center # point self.radius = radius # scalar        self.radius = radius        MaterialObject.__init__(self, material)    def __repr__(self):        return 'Sphere(%s,%s)' % (repr(self.center), self.radius)    def intersectionParameter(self, ray):        co = self.center - ray.origin        v = co.dot(ray.direction)        discriminant = v*v - co.dot(co) + self.radius*self.radius        if discriminant < 0:            return None        else:            return v - math.sqrt(discriminant)    def normalAt(self, p):        return (p - self.center).normalized()    def colorAt(self, ray):        return self.material.base_colorclass Triangle(MaterialObject):    def __init__(self, a, b, c, material):        self.a = a # point        self.b = b # point        self.c = c # point        self.u = self.b - self.a # direction vector        self.v = self.c - self.a # direction vector        MaterialObject.__init__(self, material)    def __repr__(self):        return 'Triangle(%s,%s,%s)' % (repr(self.a), repr(self.b), repr(self.c))    def intersectionParameter(self, ray):        w = ray.origin - self.a        dv = ray.direction.cross(self.v)        dvu = dv.dot(self.u)        if dvu == 0.0:            return None        wu = w.cross(self.u)        r = dv.dot(w) / dvu        s = wu.dot(ray.direction) / dvu        if 0<=r and r<=1 and 0<=s and s<=1 and r+s <=1:            return wu.dot(self.v) / dvu        else:            return None    def normalAt(self, p):        return self.u.cross(self.v).normalized()    def colorAt(self, ray):        return self.material.base_color