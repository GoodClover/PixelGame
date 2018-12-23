# I am planning to move all the functions into here, 
# so they can be imported into other files like blocks.py easily.
import random
import easygui
from copy import deepcopy

try: from blocks import Block
except: pass
try: import blocks
except: pass
try: import entities
except: pass

def isSolidP(world, x, y):
    try:
        return world[(x//8, y//8)].solid
    except:
        return True

def isSolid(world, x, y):
    try:
        return world[(x, y)].solid
    except:
        return True

def getWorldType(world, x, y): #X, Y in blocks not pixels
    try:
        return world[(x, y)].type
    except:
        return "dirt"

def getWorldPower(world, x, y): #X, Y in blocks not pixels
    try:
        return world[(x, y)].power
    except:
        return False

def getWorld(world, x, y): #X, Y in blocks not pixels
    try:
        if getWorldType(world, x, y) == "air":
            return False
        else:
            return True
    except:
        return True

def getWorldLit(world, x, y): #X, Y in blocks not pixels
    try:
        return world[(x,y)]
    except:
        return blocks.dirt()

def tick(world, x, y, inventory, groundItems):
    if getattr(blocks, getWorldType(world, x, y)).hasUp:
        world, groundItems = getattr(blocks, getWorldType(world, x, y)).update((x, y), world, groundItems)#, inventory)
    return world, groundItems

def addBlock(world, inventory, selBlockStr, x, y):
    if not getWorld(world, x, y) and inventory[selBlockStr] > 0:
        inventory[selBlockStr] -= 1
        world[(x, y)] = getattr(blocks, selBlockStr)()


class groundItem():
    def __init__(self,pos=(0,0),itemType="dirt"):
        self.pos = pos
        self.type = itemType

def removeBlock(world, groundItems, x, y):
    if world[(x, y)].type != "air":
        groundItems.append( groundItem( ( (x*8)+random.randint(-4,4), (y*8)+random.randint(-4,4), ), getWorldType(world,x,y)) )
        world[(x, y)] = blocks.air()    

recipies = {
    "tap":["ore","ore"],
    "planks":["log"],
    "wall":["planks"],
    "chest":["planks","planks","planks"],
    "ladders":["planks"],
    "battery":["ore","planks"],
    "piston":["battery","planks"],
    "sign":["planks"],
}
def craft(toCraft, inventory, amt=1):
    toCraft=toCraft.lower()
    canCraft = True
    imagInv = deepcopy(inventory)
    for i in range(0,amt):
        for reqItem in recipies[toCraft]:
            if imagInv[reqItem] <= 0:
                canCraft = False
            imagInv[reqItem] -= 1

    if canCraft:
        for i in range(0,amt):
            for reqItem in recipies[toCraft]:
                inventory[reqItem] -= 1
            inventory[toCraft] += 1
    elif not canCraft:
        easygui.msgbox("You do not have enough items!", "PixelGame - Crafting")
    return inventory

def tree(world, pos):
    highestYMod = 0
    for yMod in range(0, random.randint(4, 6)):
        if yMod > highestYMod: highestYMod = yMod
        world[(pos[0], pos[1]-yMod)] = blocks.log()
    for xLMod in range(-1, 2):
        for yLMod in range(-1, 1):
            world[(pos[0]+xLMod, pos[1]-highestYMod+yLMod)] = blocks.leaves()
    return world






if __name__ == "__main__":
    print("""
================================================
 || Hey! This is the wrong file, use main.py ||
================================================
""")
