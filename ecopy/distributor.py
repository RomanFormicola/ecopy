#Utility Functions for distributing elements across the field

import random
from typing import List
from fruit import Fruit
from agent import Agent
from agent import randomAgent

#Will Search forever if all positions occupied
def getRandomNonOccupiedPos(field):
    fieldx, fieldy = field.getDimensions()
    found = False

    pot_x = None
    pot_y = None

    while(not found):
        pot_x = random.randint(0, fieldx - 1)
        pot_y = random.randint(0, fieldy - 1)
        if field.checkSpot(pot_x, pot_y) == "EMPTY":
            found = True

    return (pot_x, pot_y)

def randomAgentDistrobution(typename: str, num: int, model: str, properties: dict, field): 
    agents = []
    for id in range(1, num + 1):
        x, y = getRandomNonOccupiedPos(field)

        if(model == "RANDOM"):
            newAgent = randomAgent(x, y, id, typename, properties)
            agents.append(newAgent)
            field.addAgent(newAgent)
        else:
            print("MODEL", model, "NOT FOUND")
            exit(2)

    return agents

def randomFruitDistrobution(typename: str, num: int, properties: dict, field): 
    for id in range(1, num + 1):
        x, y = getRandomNonOccupiedPos(field)
        newFruit = Fruit(x, y, id, typename, properties)
        field.addFruit(newFruit)

#Returns the 6 coordinates which surround a given position
def getSurroundingCoordinates(x: int, y: int):
    return [(x - 1, y - 1), (y - 1, x), (x + 1, y - 1), (x + 1, y), (x + 1, y + 1), 
            (y + 1, x), (x - 1, y + 1), (x - 1, y)]


#checks if a given coordinate is within the field bounds, returns true if it is
def withinField(coord, fieldDim):
    fieldx, fieldy = fieldDim
    if (coord[0] >= 0 and coord[0] < fieldx) and (coord[1] >= 0 and coord[1] < fieldy):
        return True
    return False


'''Recieves four coordinates which must be oriented as corners on a rectangular grid clockwise
starting from the top left corner and moving clockwise and returns an array of positions that 
passes through the corners through the corners, including the corners'''
def getRing(corners: List[int], fieldDim):
    #Check if coordinates are corners of a rectange
    ring = []
    if(len(corners) == 4):
        tLCorner = (corners[0][0] - 1, corners[0][1] - 1)
        tRCorner = (corners[1][0] + 1, corners[1][1] - 1)
        bRCorner = (corners[2][0] + 1, corners[2][1] + 1)
        bLCorner = (corners[3][0] - 1, corners[3][1] + 1) 
    else: 
        print('Wrong number of corners, corners = ', len(corners))
        return -1
    
    if tLCorner[0] <= tRCorner[0] and tLCorner[1] == tRCorner[1]:
        if(bLCorner[0] <= bRCorner[0] and bLCorner[1] == bRCorner[1]):
            if tLCorner[1] <= bLCorner[1]:
                #top left to top right
                for i in range( tLCorner[0], tRCorner[0] + 1):
                    if not withinField( (i, tLCorner[1]), fieldDim):
                        break
                    ring.append( (i, tLCorner[1]) )
                #top right to bottom right
                for i in range( tRCorner[1] + 1, bRCorner[1] + 1):
                    if not withinField((tRCorner[0], i), fieldDim):
                        break
                    ring.append( (tRCorner[0], i) )
                #bottom left to bottom right
                for i in reversed(range(bLCorner[0], bRCorner[0])):
                    if not withinField((i, bRCorner[1]), fieldDim):
                        break
                    ring.append( (i, bRCorner[1]) )
                #top left to bottom left
                for i in reversed(range( tLCorner[1] + 1, bLCorner[1])):
                    if not withinField((tLCorner[0], i), fieldDim):
                        break
                    ring.append( (tLCorner[0], i))
        
                return (ring, (tLCorner, tRCorner, bRCorner, bLCorner))
    
    print('Corners are not oriented properly ')


'''Heat Map Distrobution takes a number of fruit 'epicenters' (numEpicenter) and an initital 
probability (initialP) between 0 and 1, as well a pDecay between 0 and inititalP
the program loops around the fruit epicenter and places fruit with probability 
initalP - loop * pDecay'''
def heatMapFruitDistrobution(numEpicenters: int, initialP: float, pdecay: float, fruitType: str, properties: dict, field):
    fieldx, fieldy = field.getDimensions()

    for i in range(numEpicenters):

        e_x, e_y = getRandomNonOccupiedPos(field)
        corners = [(e_x, e_y), (e_x, e_y), (e_x, e_y), (e_x, e_y)]

        if random.uniform(0, 1) < initialP:
            f_id = int(str(e_x) + str(e_y))
            newFruit = Fruit(e_x, e_y, f_id, fruitType, properties)
            field.addFruit(newFruit)
        
        for i in range(max(fieldx - e_x, e_x, fieldy - e_y, e_y)):
            ring, corners = getRing(corners, (fieldx, fieldy))
            if( (initialP - i * pdecay) == 0):
                break
            for pos in ring:
                if random.uniform(0, 1) < initialP - (i * pdecay):
                    f_id = int(str(pos[0]) + str(pos[1]))
                    newFruit = Fruit(pos[0], pos[1], f_id, fruitType, properties)
                    field.addFruit(newFruit)



    


        


    

