class Fruit:
    def __init__(self, x_pos: int, y_pos: int, f_id: int, typename: str, properties: dict):
        self.x = x_pos
        self.y = y_pos
        self.id = f_id
        self.type = typename
        self.properties = properties

    def getPos(self):
        return (self.x, self.y)

    def getMark(self):
        return self.type + str(self.id)
    
    def getType(self):
        return self.type

    def getGenus(self):
        return "FRUIT"

    def getHarvestTime(self):
        return self.properties['harvest_time']

    def getEnergy(self):
        return self.properties['energy']