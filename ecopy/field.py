import distributor
from matplotlib import pyplot as plt
from matplotlib import colors
from terrain import Terrain
import time
import random

class Land:
    #contents is a stack of fruit or empty (0)
    def __init__(self, type, contents):
        self.contents = contents
        self.depth = len(self.contents)
        self.type = type

    def getType(self):
        return self.type

    def getTop(self):
        return self.contents[self.depth - 1]
    
    def harvestTop(self):
        return self.contents.pop()
    
    def plant(self, fruit):
        self.contents.append(fruit)

class Field:

    def __init__(self, field_x: int, field_y: int, show_terrain: bool):
        self.matrix = []
        self.grid = []
        self.field_x = field_x
        self.field_y = field_y


        #The grid is just a 2d array of integers and is used exclusively for display purposes with matplotlib
        self.grid = [[0 for i in range(self.field_x)]
                     for j in range(self.field_y)]

        #The matrix contains the instances of fruit and agents as well as 0's which mark empty space
        self.matrix = [[0 for i in range(self.field_x)]
                     for j in range(self.field_y)]

        self.terrain = Terrain(self.field_x, self.field_y)
        self.terrain.create()
        if(show_terrain):
            self.terrain.display()

    def printField(self):
        for x in range(0, self.field_x):
            for y in range(0, self.field_y):
                if(self.matrix[x][y] == 0):
                    print(self.matrix[x][y], end=" ")
                else:
                    print(self.matrix[x][y].getMark(), end=" ")
            print("\n")

    def display(self, plt, cmap, delay: float):
        #grid = self.asGrid()
        plt.pcolor(self.grid, cmap=cmap, edgecolors='k', linewidths=3)
        plt.pause(delay)
        
    
    def asGrid(self):
        grid = [[0 for i in range(self.field_x)] for j in range(self.field_y)]
        for x in range(0, self.field_x):
            for y in range(0, self.field_y):
                if self.matrix[x][y] != 0:   
                    if self.matrix[x][y].getGenus() == 'AGENT':
                        grid[x][y] = 1
                    elif self.matrix[x][y].getGenus() == 'FRUIT':
                        grid[x][y] = 2
        return grid
    
    def checkSpot(self, pot_x: int, pot_y: int):
        if self.matrix[pot_x][pot_y] == 0:
            return "EMPTY"
        else:
            return self.matrix[pot_x][pot_y].getGenus()
    
    def fruitHarvest(self, x: int, y: int):
        if self.matrix[x][y] != 0 and self.matrix[x][y].getGenus() == "FRUIT":    
            return self.matrix[x][y]

    def addAgent(self, agent):
        x, y = agent.getPos()
        self.matrix[x][y] = agent
        self.grid[x][y] = 1

    def removeFromField(self, x: int, y: int):
        self.matrix[x][y] = 0
        self.grid[x][y] = 0

    def addFruit(self, fruit):
        x, y = fruit.getPos()
        self.matrix[x][y] = fruit
        self.grid[x][y] = 2

    def verticalDiff(self, old_x, old_y, new_x, new_y):
        return self.terrain.getZ(new_x, new_y) - self.terrain.getZ(old_x, old_y)
    
    def updateAgentPos(self, old_x: int, old_y: int, new_x: int, new_y: int):
        self.matrix[new_x][new_y] = self.matrix[old_x][old_y]
        self.matrix[old_x][old_y] = 0

        self.grid[new_x][new_y] = 1
        self.grid[old_x][old_y] = 0

        return self.verticalDiff(old_x, old_y, new_x, new_y) 

    def getDimensions(self):
        return (self.field_x, self.field_y)

