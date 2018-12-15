#All the blocks
import random

from functions import *
import functions



#Base class
class Block():
    def __init__(self, bType="dirt", solid=True, dura=4):
        self.solid = solid
        self.type = bType
        self.durability = dura
        self.darkness = 0



#The types of blocks
class debug(Block):                         #
    hasUp = False                           #
    def __init__(self):                     #
        super().__init__("debug", False, 4) #Debug block

class air(Block):
    hasUp = False
    def __init__(self):
        super().__init__("air", False, -1) #Not Solid, Unbreakable

class stone(Block):
    hasUp = False
    def __init__(self):
        super().__init__("stone", True, 4)

class ore(Block):
    hasUp = False
    def __init__(self):
        super().__init__("ore", True, 4)

class dirt(Block):
    hasUp = True
    def __init__(self):
        super().__init__("dirt", True, 4)
    def update(pos, world):
        try:
            if world[pos[0], pos[1]-1].type == "air" or world[pos[0], pos[1]-1].type == "flower":
                world[pos].type = "grass"
        except:
            pass
        return world

class grass(Block):
    hasUp = True
    def __init__(self):
        super().__init__("grass", True, 4)
    def update(pos, world):
        try:
            if world[pos[0], pos[1]-1].type != "air" and world[pos[0], pos[1]-1].type != "flower":
                world[pos].type = "dirt"
        except:
            pass
        return world

class log(Block):
    hasUp = True
    def __init__(self):
        super().__init__("log", True, 4)
    def update(pos, world):
        if not (world[(pos[0], pos[1]+1)].type == "dirt" or world[(pos[0], pos[1]+1)].type == "grass" or world[(pos[0], pos[1]+1)].type == "log"):
            world[pos] = air()
        elif world[pos[0], pos[1]+1].type == "dirt" and world[pos[0], pos[1]-1].type == "air" and random.randint(0, 50) == 1:
            world = functions.tree(world, pos)
        return world

class leaves(Block):
    hasUp = True
    def __init__(self):
        super().__init__("leaves", False, 2)
    def update(pos, world):
        tlN = 0
        tl = False
        for xM in range(-1, 2):
            for yM in range(-2, 3):
                try:
                    if world[pos[0]+xM, pos[1]+yM].type == "log":
                        tlN += 1
                except:
                    pass
        if tlN > 0: tl = True
        if not tl:
            world[pos] = air()
        return world

class water(Block):
    hasUp = True
    def __init__(self):
        super().__init__("water", False, 4) #Not Solid
    def update(pos, world):
        try:
            if world[pos[0], pos[1]+1].type == "air":
                world[pos[0], pos[1]+1] = water()
                world[pos] = air()
            elif world[pos[0]+1, pos[1]].type == "air" and world[pos[0]+1, pos[1]-1].type != "water":
                world[pos[0]+1, pos[1]] = water()
                world[pos] = air()
            elif world[pos[0]-1, pos[1]].type == "air" and world[pos[0]-1, pos[1]-1].type != "water":
                world[pos[0]-1, pos[1]] = water()
                world[pos] = air()
        except:
            pass
        return world

class tap(Block):
    hasUp = True
    def __init__(self):
        super().__init__("tap", True, 4)
    def update(pos, world):
        if world[pos[0], pos[1]+1].type == "air":
            world[pos[0], pos[1]+1] = water()
        return world

class sand(Block):
    hasUp = True
    def __init__(self):
        super().__init__("sand", True, 2)
    def update(pos, world):
        if not world[pos[0], pos[1]+1].solid:
            underBlock = functions.getWorldLit(world,pos[0],pos[1]+1)
            world[pos[0], pos[1]+1] = sand()
            world[pos[0], pos[1]] = underBlock
        return world

class flower(Block):
    hasUp = True
    def __init__(self):
        super().__init__("flower", False, 1) #Not Solid
    def update(pos, world):
        if not ( functions.getWorldType(world, pos[0], pos[1]+1) == "grass" or functions.getWorldType(world, pos[0], pos[1]+1) == "dirt"):
            world[pos] = air()
        return world





if __name__ == "__main__":
    print("""
================================================
 || Hey! This is the wrong file, use main.py ||
================================================
""")
