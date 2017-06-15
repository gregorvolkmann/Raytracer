#!/usr/bin/python
# -*- coding: utf-8 -*-

from PIL import Image
from objects import *
from misc import Color

image_width = 400
image_height = 400
image = Image.new('RGB', (image_width, image_height))
BACKGROUND_COLOR = Color(255, 255, 255)

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
                for object in self.object_list:
                    hitdist = object.intersectionParameter(ray)
                    if hitdist:
                        if hitdist < maxdist and hitdist > 0:
                            maxdist = hitdist
                            color = object.colorAt(ray)
                image.putpixel((x, y), color.rgb())
        return image

    # https://www.python.org/dev/peps/pep-0008/#other-recommendations
    def calc_ray(self, x, y):
        xcomp = self.camera.s.scale(x*self.camera.pixel_width - self.camera.width/2)
        ycomp = self.camera.u.scale(y*self.camera.pixel_height - self.camera.height/2)
        return Ray(self.camera.e, self.camera.f+xcomp+ycomp)

if __name__ == '__main__':
    camera = Camera(e=Point(0.0, 1.8, 10), c=Point(0, 3, 0), up=Vector(0, 1, 1), fov=45, image_width=400, image_height=400)
    print(camera)
    plane = Plane(Point(0, 0, 0), Vector(0, 1, 0))
    print(plane)

    tracer = Raytracer(camera)
    tracer.addObject(plane)

    img = tracer.render_image()
    img.show()
    img.save('img.jpg', 'JPEG')
