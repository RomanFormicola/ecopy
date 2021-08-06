'''This code was directly copied from https://github.com/hnhaefliger/pyTerrain and 
slightly modified for my purposes '''


import graphics.engine
import perlin
import math

class Terrain:
    def __init__(self, field_x, field_y):
        ############ Display variables

        self.scale = 6
        self.distance = 100

        ############ Land size

        self.width = field_x # map width
        self.length = field_y # map length
        ############ Noise variables

        self.n1div = 30 # landmass distribution
        self.n2div = 4 # boulder distribution
        self.n3div = 1 # rock distribution

        self.n1scale = 20 # landmass height
        self.n2scale = 2 # boulder scale
        self.n3scale = 0.5 # rock scale

        self.noise1 = perlin.noise(self.width / self.n1div, self.length / self.n1div) # landmass / mountains
        self.noise2 = perlin.noise(self.width / self.n2div, self.length / self.n2div) # boulders
        self.noise3 = perlin.noise(self.width / self.n3div, self.length / self.n3div) # rocks

        ############ z modifiers

        self.zroot = 2
        self.zpower = 2.5
        
        self.zmap = dict()

        ############ colors

        self.colors = {
            0: 'brown',
            1: 'yellow',
            20: 'green',
            25: 'gray',
            1000: 'white'
            }

        ############ 3D shapes

        self.points = []
        self.triangles = []

    ############

    def color(self, a, b, c): # check land type
        z = (self.points[a][2] + self.points[b][2] + self.points[c][2]) / 3 # calculate average height of triangle
        for color in self.colors:
            if z <= color:
                return self.colors[color]
                break

    def create(self):

        for x in range(self.width):
            for y in range(self.length):
                z = self.noise1.perlin(x / self.n1div, y / self.n1div) * self.n1scale # add landmass
                z += self.noise2.perlin(x / self.n2div, y / self.n2div) * self.n2scale # add boulders
                z += self.noise3.perlin(x / self.n3div, y / self.n3div) * self.n3scale # add rocks
                if z >= 0:
                    z = -math.sqrt(z)
                else:
                    z = ((-z) ** (1 / self.zroot)) ** self.zpower
                self.points.append([x, y, z])
                self.zmap[(x, y)] = z

        for x in range(self.width):
            for y in range(self.length):
                if 0 < x and 0 < y:
                    a, b, c = int(x * self.length + y), int(x * self.length + y - 1), int((x - 1) * self.length + y) # find 3 points in triangle
                    self.triangles.append([a, b, c, self.color(a, b, c)])
                        
                if x < self.width - 1 and y < self.length - 1:
                    a, b, c, = int(x * self.length + y), int(x * self.length + y + 1), int((x + 1) * self.length + y) # find 3 points in triangle
                    self.triangles.append([a, b, c, self.color(a, b, c)])
    def getZ(self, x, y):
        return self.zmap[(x, y)]

    ############

    def display(self):
        world = graphics.engine.Engine3D(self.points, self.triangles, scale=self.scale, distance=self.distance, width=1400, height=750, title='Terrain')
        world.rotate('x', -30)
        world.render()
        world.screen.window.mainloop()