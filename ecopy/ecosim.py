import sys
import random
import json
import csv
import distributor
from field import Field
from agent import Agent
from fruit import Fruit
from typing import List
from matplotlib import pyplot as plt
from matplotlib import colors
from distributor import getRandomNonOccupiedPos


#Initializes the field including the starting agent positions
def main():
    
    print(configfile)

    with open(sys.argv[1]) as configfile:
        config = json.load(configfile)
        field_x = config['field_x']
        field_y = config['field_y']
        iterations = config['iterations']
        show_terrain = True #config['show_terrain']

    field = Field(field_x, field_y, show_terrain)  

    #initialize agents
    for agentType in config['agents']:
        if agentType['distro'] == 'RANDOM':
            agents = distributor.randomAgentDistrobution(agentType['name'], agentType['number'], agentType['model'], agentType['properties'], field)

    #initialize fruit  
    for fruitType in config['fruit']:
        if fruitType['distro'] == 'RANDOM':
            distributor.randomFruitDistrobution(fruitType['name'], fruitType['number'], fruitType['properties'], field)
        elif fruitType['distro'] == 'HEATMAP':
            distributor.heatMapFruitDistrobution(fruitType['num_epic'], fruitType['initial_p'], fruitType['p_decay'], fruitType['name'], fruitType['properties'], field)


    #display
    grid = field.asGrid()
    plt.figure(figsize=(6, 6))
    cmap = colors.ListedColormap(['blue', 'red', 'green'])
    plt.pcolor(grid, cmap=cmap, edgecolors='k', linewidths=1)

    deadAgents = []

    for i in range(0, iterations):
        for agent in agents:
            agent.takeAction(field)
            if(not agent.isAlive()):
                field.removeFromField(agent.getPos()[0], agent.getPos()[1])
                deadAgents.append(agent)
                agents.remove(agent)
                
                if(not agents):
                    print("ALL AGENTS ARE DEAD")
                    break

        #print("----------------------------------")
        if(len(sys.argv) > 2 and sys.argv[2] == '-animate'):
            field.display(plt, cmap, 0.05)
        

    agentReport(agents, deadAgents)

def agentReport(agents, deadAgents):
    print("Alive:")
    for agent in agents:
        print("Agent:", agent.getMark(), " harvested:", agent.getBasket(), "Energy=", agent.getEnergy())
    
    print("Dead:")
    for agent in deadAgents:
        print("Agent:", agent.getMark(), " harvested:", agent.getBasket(), "Energy=", agent.getEnergy())


if __name__ == "__main__":
    main()
