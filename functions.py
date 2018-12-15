# I am planning to move all the functions into here, 
# so they can be imported into other files like blocks.py easily.
import random

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

def tick(world, x, y, inventory):
    if getattr(blocks, world[(x, y)].type).hasUp:
        world = getattr(blocks, world[(x, y)].type).update((x, y), world)#, inventory)
    return world

def addBlock(world, inventory, selBlockStr, x, y):
    x = x//8
    y = y//8
    if not getWorld(world, x, y) and inventory[selBlockStr] > 0:
        inventory[selBlockStr] -= 1
        world[(x, y)] = getattr(blocks, selBlockStr)()

def removeBlock(world, inventory, x, y):
    x = x//8
    y = y//8
    if world[(x, y)].type != "air":
        inventory[ getWorldType(world, x, y) ] += 1
        world[(x, y)] = blocks.air()    


#Trees-

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
