#!/usr/bin/python
# -*- coding: utf-8 -*-

from PIL import Image
from objects import *
from misc import *

image_width = 400
image_height = 400
image = Image.new('RGB', (image_width, image_height))
BACKGROUND_COLOR = Color(0, 0, 0)

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
                            light_maxdist = float('inf')
                            for light in filter(lambda x: isinstance(x, Light), self.object_list):
                                l = (light - p).normalized()
                                lr = l.mirror(n)
                                light_ray = Ray(p, l)
                                light_dist = (light - p).length()
                                # ambient
                                ca = object.colorAt(ray)
                                ka = object.material.ambient_coefficient
                                c_ambient = ca * ka

                                cin = light.color
                                # shadow
                                for object in filter(lambda x: not isinstance(x, Light) and x is not object, self.object_list):
                                    object_dist = object.intersectionParameter(light_ray)
                                    if object_dist:
                                        #     if object_dist > 5e-16:
                                        cin = object.colorAt(light_ray).intensity()



                                # diffuse
                                kd = object.material.diffuse_coefficient
                                cos_fi = l.dot(n)
                                c_diffuse = cin * kd * cos_fi
                                # specular
                                ks = object.material.specular_coefficient
                                cos_0_n = (lr.dot(d*-1))**object.material.roughness
                                c_specular = cin * ks * cos_0_n

                                color = c_ambient + c_diffuse + c_specular
                image.putpixel((x, y), color.rgb())
        return image.rotate(180)

    # https://www.python.org/dev/peps/pep-0008/#other-recommendations
    def calc_ray(self, x, y):
        xcomp = self.camera.s.scale(x*self.camera.pixel_width - self.camera.width/2)
        ycomp = self.camera.u.scale(y*self.camera.pixel_height - self.camera.height/2)
        return Ray(self.camera.e, self.camera.f+xcomp+ycomp)

if __name__ == '__main__':
    camera = Camera(e=Point(0.0, 1.8, 10), c=Point(0, 3, 0), up=Vector(0, 1, 1), fov=45, image_width=400, image_height=400)
    print(camera)

    tracer = Raytracer(camera)

    plane = Plane(Point(0, 0, 0), Vector(0, 1, 0), CheckerboardMaterial(Color(255, 255, 255), 1.0, 0.6, 0.2, Color(0, 0, 0), 1))
    sphere_red = Sphere(Point(1.5, 2, 0), 1,  Material(Color(255, 0, 0), 1.0, 0.6, 0.2))
    sphere_green = Sphere(Point(-1.5, 2, 0), 1,  Material(Color(0, 255, 0), 1.0, 0.6, 0.2))
    sphere_blue = Sphere(Point(0, 4.5, 0), 1,  Material(Color(0, 0, 255), 1.0, 0.6, 0.2))
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

    img = tracer.render_image()
    img.show()
    img.save('img.bmp', 'BMP')
