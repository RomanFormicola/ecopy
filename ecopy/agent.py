import random
import json

class Agent:
    #properties: A dict of properties that the agent has, which right now is just init_energy
    #this seems slightly roundabout right now but will make things simpler in the future
    def __init__(self, x_pos: int, y_pos: str, a_id: int, tye: str, properties: dict):
        self.x = x_pos
        self.y = y_pos
        self.id = a_id
        self.fruitBasket = []
        self.properties = properties
        self.alive = True

        self.energy = properties['init_energy']

    def getBasket(self):
        fruitDisplay = []
        for fruit in self.fruitBasket:
            fruitDisplay.append(fruit.getMark())
        return fruitDisplay

    def getPos(self):
        return (self.x, self.y)
    
    def getMark(self):
        return "A" + str(self.id)

    def getGenus(self):
        return "AGENT"
    
    def isAlive(self):
        if(self.energy > 0):
            return True
        else:
            return False
    
    def getEnergy(self):
        return self.energy

    def eat(self, fruit):
        self.energy = self.energy + fruit.getEnergy()
        self.fruitBasket.remove(fruit)
        #print("Consumed: ", fruit.getEnergy(), "current energy: ", self.energy)

        

class randomAgent(Agent):

    def takeAction(self, field):

        if(self.isAlive()):
            #Eat all fruit in basket
            for fruit in self.fruitBasket:
                self.eat(fruit)

            #Move
            self.move(field)

            self.energy = self.energy - self.properties['energy_decay']

        
    def moveEnergyCost(self, new_x, new_y, field):
        vert = field.verticalDiff(self.x, self.y, new_x, new_y)

        return abs(vert)
        

    def move(self, field):
 
        d_x = random.randint(-1, 1)
        d_y = random.randint(-1, 1)

        new_x = self.x + d_x
        new_y = self.y + d_y

        f_x, f_y = field.getDimensions()

        if (new_x >= f_x or new_x < 0):
            new_x = self.x

        if(new_y >= f_y or new_y < 0):
            new_y = self.y

        #If the desired position is not occupied move there
        #else do nothing for now. variable cont is the genus of whatever occupies the position.

        cont = field.checkSpot(new_x, new_y)
        if(cont != "AGENT"):

            if(cont == "FRUIT"):
                self.fruitBasket.append(field.fruitHarvest(new_x, new_y))
                #print("AGENT ", self.getMark(), " HAS HARVESTED A FRUIT")
                #print(self.fruitBasket[0].getMark())

            #calculate and update energy cost of move
            self.energy = self.energy - self.moveEnergyCost(new_x, new_y, field)

            #update the agents position on the field and status
            field.updateAgentPos(self.x, self.y, new_x, new_y)
            self.x = new_x
            self.y = new_y
        
        
