# -*- coding: utf-8 -*-

class Color:
    def __init__(self, r, g, b):
        self.r = int(r)
        self.g = int(g)
        self.b = int(b)

    def rgb(self):
        return (int(self.r), int(self.g), int(self.b))
