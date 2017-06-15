#!/usr/bin/python
# -*- coding: utf-8 -*-

# Code by Gregor Volkmann

from PIL import Image
from misc import *
from objects import *

SHADOW_CONST = 0.25
TOLERANCE = 5e-16
BACKGROUND_COLOR = Color(0, 0, 0)
MAXLEVEL = 1
REFLECTION = 0.5

image_width = 400
image_height = 400
image = Image.new('RGB', (image_width, image_height))

class Raytracer:
    def __init__(self, camera):
        self.camera = camera
        self.object_list = []

    def addObject(self, object):
        self.object_list.append(object)

    # http://effbot.org/imagingbook/image.htm
    def render_image(self):
        global image
        global BACKGROUND_COLOR
        for y in range(image_height):
            for x in range(image_width):
                ray = self.calc_ray(x, y)
                maxdist = float('inf')
                color = BACKGROUND_COLOR
                for object in filter(lambda x: not isinstance(x, Light), self.object_list):
                    hitdist = object.intersectionParameter(ray)
                    if hitdist:
                        if hitdist < maxdist and hitdist > 0:
                            maxdist = hitdist

                            p = ray.pointAtParameter(maxdist)
                            n = object.normalAt(p)
                            d = ray.direction

                            color = object.colorAt(ray)

                            # CALC LIGHT
                            for light in filter(lambda x: isinstance(x, Light), self.object_list):
                                l = (light - p).normalized()
                                lr = l.mirror(n)
                                light_ray = Ray(p, l)

                                # ambient
                                ca = object.colorAt(ray)
                                ka = object.material.ambient_coefficient
                                c_ambient = ca * ka
                                # diffuse
                                cin = light.color
                                kd = object.material.diffuse_coefficient
                                cos_fi = l.dot(n)
                                c_diffuse = cin * kd * cos_fi
                                # specular
                                if math.degrees(math.acos(light_ray.direction.dot(n))) > 90.0: # Strahl zeigt nach innen
                                    cin = Color(0, 0, 0)
                                else:
                                    cin = light.color
                                ks = object.material.specular_coefficient
                                cos_0_n = (lr.dot(d*-1))**object.material.roughness
                                c_specular = cin * ks * cos_0_n

                                # shadow
                                object_maxdist = float('inf')
                                for object in filter(lambda x: not isinstance(x, Light) and not x is object, self.object_list):
                                    object_dist = object.intersectionParameter(light_ray)
                                    if object_dist:
                                        if object_dist < object_maxdist and object_dist > TOLERANCE:
                                            object_maxdist = object_dist
                                            c_ambient *= SHADOW_CONST
                                            c_diffuse *= SHADOW_CONST
                                            c_specular = Color(0, 0, 0)
                                color = c_ambient + c_diffuse + c_specular
                image.putpixel((x, y), color.rgb())
        return image.rotate(180)

    # https://www.python.org/dev/peps/pep-0008/#other-recommendations
    def calc_ray(self, x, y):
        xcomp = self.camera.s.scale(x*self.camera.pixel_width - self.camera.width/2)
        ycomp = self.camera.u.scale(y*self.camera.pixel_height - self.camera.height/2)
        return Ray(self.camera.e, self.camera.f+xcomp+ycomp)

    def intersect(self, level, ray, max_level=MAXLEVEL):
        maxdist = float('inf')
        hitPointData = {}
        for object in filter(lambda x: not isinstance(x, Light), self.object_list):
            # Der Part damit sich die Kugeln nicht im Boden spiegeln bei MAXLEVEL = 1 (Lösungsansatz > 0)
            if not isinstance(object, Plane) and level==max_level:
                continue

            hitdist = object.intersectionParameter(ray)
            if level <= max_level:
                if hitdist and hitdist < maxdist and hitdist > 0:
                    maxdist = hitdist

                    objects = filter(lambda x: not isinstance(x, Light) and not x is object, self.object_list[:])
                    p = ray.pointAtParameter(hitdist)

                    hitPointData['object'] = object
                    hitPointData['objects'] = objects
                    hitPointData['p'] = p
                    hitPointData['ray'] = ray
        return hitPointData

    def traceRay(self, level, ray):
        hitPointData = self.intersect(level, ray, MAXLEVEL)
        if hitPointData:
            return self.shade(level, hitPointData)
        return BACKGROUND_COLOR

    def render_image_recursive(self):
        for y in range(image_height):
            for x in range(image_width):
                ray = self.calc_ray(x, y)
                color = self.traceRay(0, ray)
                image.putpixel((x, y), color.rgb())
        return image.rotate(180)

    def shade(self, level, hitPointData):
        directColor = self.computeDirectLight(hitPointData)

        reflectedRay = self.computeReflectedRay(hitPointData)
        reflectColor = self.traceRay(level+1, reflectedRay)

        # refractedRay = computeRefractedRay(hitPointData)
        # refractColor = traceRay(level+1, refractedRay)

        return directColor + reflectColor*REFLECTION # + refraction*refractedColor

    def computeDirectLight(self, hitPointData):
        # return hitPointData['object'].colorAt(hitPointData['ray'])


        p = hitPointData['p']
        object = hitPointData['object']
        n = hitPointData['object'].normalAt(hitPointData['p'])
        ray = hitPointData['ray']
        d = self.computeReflectedRay(hitPointData).direction

        # CALC LIGHT
        for light in filter(lambda x: isinstance(x, Light), self.object_list):
            l = (light - p).normalized()
            lr = l.mirror(n)
            light_ray = Ray(p, l)

            # ambient
            ca = object.colorAt(ray)
            ka = object.material.ambient_coefficient
            c_ambient = ca * ka
            # diffuse
            cin = light.color
            kd = object.material.diffuse_coefficient
            cos_fi = l.dot(n)
            c_diffuse = cin * kd * cos_fi
            # specular
            if math.degrees(math.acos(light_ray.direction.dot(n))) > 90.0: # Strahl zeigt nach innen
                cin = Color(0, 0, 0)
            else:
                cin = light.color
            ks = object.material.specular_coefficient
            cos_0_n = (lr.dot(d*-1))**object.material.roughness
            c_specular = cin * ks * cos_0_n

            # shadow
            object_maxdist = float('inf')
            for object in filter(lambda x: not isinstance(x, Light) and not x is object, self.object_list):
                object_dist = object.intersectionParameter(light_ray)
                if object_dist:
                    if object_dist < object_maxdist and object_dist > TOLERANCE:
                        object_maxdist = object_dist
                        c_ambient *= SHADOW_CONST
                        c_diffuse *= SHADOW_CONST
                        c_specular = Color(0, 0, 0)
            color = c_ambient + c_diffuse + c_specular
        return color

    def computeReflectedRay(self, hitPointData):
        return Ray(hitPointData['p'], hitPointData['ray'].direction.mirror(hitPointData['object'].normalAt(hitPointData['p'])))

if __name__ == '__main__':
    camera = Camera(e=Point(0.0, 1.8, 10), c=Point(0, 3, 0), up=Vector(0, 1, 1), fov=45, image_width=400, image_height=400)
    print(camera)

    tracer = Raytracer(camera)

    plane = Plane(Point(0, 0, 0), Vector(0, 1, 0), CheckerboardMaterial(Color(255, 255, 255), 1.0, 0.6, 0.2, 40, Color(0, 0, 0), 1))
    sphere_red = Sphere(Point(1.5, 2, 0), 1,  Material(Color(255, 0, 0), 1.0, 0.6, 0.0, 7))
    sphere_green = Sphere(Point(-1.5, 2, 0), 1,  Material(Color(0, 255, 0), 1.0, 0.6, 0.5))
    sphere_blue = Sphere(Point(0, 4.5, 0), 1,  Material(Color(0, 0, 255), 1.0, 0.6, 0.2, 32))
    triangle = Triangle(Point(1.5, 2, 0), Point(-1.5, 2, 0), Point(0, 4.5, 0),  Material(Color(255, 255, 0), 1.0, 0.6, 0.2))
    light = PointLight(30, 30, 10, Color(255, 255, 255))

    tracer.addObject(plane)
    tracer.addObject(sphere_red)
    tracer.addObject(sphere_green)
    tracer.addObject(sphere_blue)
    tracer.addObject(triangle)
    tracer.addObject(light)

    for object in tracer.object_list:
        print(object)

    # img = tracer.render_image()
    img = tracer.render_image_recursive()
    img.show()
    img.save('img.bmp', 'BMP')
