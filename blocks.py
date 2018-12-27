#All the blocks
import random

from functions import *
import functions
import pygame



#Base class
class Block():
    def __init__(self, bType="dirt", solid=True, maxDura=4, power=False):
        self.solid = solid
        self.type = bType
        self.durability = maxDura
        self.maxDurability = maxDura
        self.darkness = 0
        self.power = power
        self.blob = 0



#The types of blocks
class debug(Block):                         #
    hasUp = False                           #
    def __init__(self):                     #
        super().__init__("debug", False, 4, False) #Debug block

class air(Block):
    hasUp = False
    def __init__(self):
        super().__init__("air", False, -1, False) #Not Solid, Unbreakable

class stone(Block):
    hasUp = False
    def __init__(self):
        super().__init__("stone", True, 4, False)

class ore(Block):
    hasUp = False
    def __init__(self):
        super().__init__("ore", True, 4, False)

class dirt(Block):
    hasUp = True
    def __init__(self):
        super().__init__("dirt", True, 3, False)
    def update(pos, world, groundItems):
        try:
            if world[pos[0], pos[1]-1].type == "air" or world[pos[0], pos[1]-1].type == "flower":
                world[pos].type = "grass"
        except:
            pass
        return world, groundItems

class grass(Block):
    hasUp = True
    def __init__(self):
        super().__init__("grass", True, 3, False)
    def update(pos, world, groundItems):
        try:
            if world[pos[0], pos[1]-1].type != "air" and world[pos[0], pos[1]-1].type != "flower":
                world[pos].type = "dirt"
        except:
            pass
        return world, groundItems

class log(Block):
    hasUp = True
    def __init__(self):
        super().__init__("log", True, 4, False)
    def update(pos, world, groundItems):
        if not (world[(pos[0], pos[1]+1)].type == "dirt" or world[(pos[0], pos[1]+1)].type == "grass" or world[(pos[0], pos[1]+1)].type == "log"):
            pygame.mixer.Sound("sounds\\falllog.wav").play()
            functions.removeBlock(world, groundItems, pos[0], pos[1])
        elif world[pos[0], pos[1]+1].type == "dirt" and world[pos[0], pos[1]-1].type == "air" and random.randint(0, 50) == 0:
            world = functions.tree(world, pos)
        return world, groundItems

class planks(Block):
    hasUp = False
    def __init__(self):
        super().__init__("planks", True, 4, False)

class wall(Block):
    hasUp = False
    def __init__(self):
        super().__init__("wall", False, 4, False)

class ladders(Block):
    hasUp = False
    def __init__(self):
        super().__init__("ladders", False, 2, False)

class chest(Block):
    hasUp = True
    def __init__(self):
        super().__init__("chest", False, 4, False)
    def update(pos, world, groundItems):
        if random.randint(0,50)==0:
            groundItems.append( functions.groundItem( ((pos[0]*8)+random.randint(-4,4), (pos[1]*8)+random.randint(-4,4)) , "stone"))
        return world,groundItems


class leaves(Block):
    hasUp = False #True
    def __init__(self):
        super().__init__("leaves", False, 2, False)
        self.distance = 1
    def update(pos, world, groundItems):
        if functions.getWorldType(world, pos[0], pos[1]-1)== "log" or functions.getWorldType(world, pos[0], pos[1]+1) == "log" or functions.getWorldType(world, pos[0]-1, pos[1]) == "log" or functions.getWorldType(world, pos[0]+1, pos[1]) == "log":
            world[pos].distance = 1
        else:
            smallest = 1000
            if functions.getWorldType(world, pos[0], pos[1]-1) == "leaves": smallest = world[pos[0], pos[1]-1].distance + 1
            if functions.getWorldType(world, pos[0]+1, pos[1]) == "leaves" and world[pos[0]+1, pos[1]].distance < smallest:
                smallest = world[pos[0]+1, pos[1]].distance + 1
            if functions.getWorldType(world, pos[0], pos[1]+1) == "leaves" and world[pos[0], pos[1]+1].distance < smallest:
                smallest = world[pos[0], pos[1]+1].distance + 1
            if functions.getWorldType(world, pos[0]-1, pos[1]) == "leaves" and world[pos[0]-1, pos[1]].distance < smallest:
                smallest = world[pos[0]-1, pos[1]].distance + 1
            else: smallest = 0
            world[pos].distance = smallest

        if world[pos].distance == 0 or world[pos].distance > 6:
            world[pos] = air()
        return world, groundItems

class water(Block):
    hasUp = True
    def __init__(self):
        super().__init__("water", False, -1, False) #Not Solid, unbreakable
    def update(pos, world, groundItems):
        try:
            if world[pos[0], pos[1]+1].type == "air":
                pygame.mixer.Sound("sounds\\waterpour.wav").play()
                world[pos[0], pos[1]+1] = water()
                world[pos] = air()
            elif world[pos[0]+1, pos[1]].type == "air" and world[pos[0]+1, pos[1]-1].type != "water":
                #pygame.mixer.Sound("sounds\\waterpour.wav").play()
                world[pos[0]+1, pos[1]] = water()
                world[pos] = air()
            elif world[pos[0]-1, pos[1]].type == "air" and world[pos[0]-1, pos[1]-1].type != "water":
                #pygame.mixer.Sound("sounds\\waterpour.wav").play()
                world[pos[0]-1, pos[1]] = water()
                world[pos] = air()
        except:
            pass
        return world, groundItems

class tap(Block):
    hasUp = True
    def __init__(self):
        super().__init__("tap", True, 4, False)
    def update(pos, world, groundItems):
        if functions.getWorldType(world, pos[0], pos[1]+1) == "air":
            world[pos[0], pos[1]+1] = water()
        return world, groundItems

class sand(Block):
    hasUp = True
    def __init__(self):
        super().__init__("sand", True, 2, False)
    def update(pos, world, groundItems):
        if not functions.isSolid(world,pos[0], pos[1]+1):
            underBlock = functions.getWorldLit(world,pos[0],pos[1]+1)
            world[pos[0], pos[1]+1] = sand()
            world[pos[0], pos[1]] = underBlock
        return world, groundItems

class flower(Block):
    hasUp = True
    def __init__(self):
        super().__init__("flower", False, 1, False) #Not Solid
    def update(pos, world, groundItems):
        if not ( functions.getWorldType(world, pos[0], pos[1]+1) == "grass" or functions.getWorldType(world, pos[0], pos[1]+1) == "dirt"):
            world[pos] = air()
        return world, groundItems

class top_hat(Block):
    hasUp = True
    def __init__(self):
        super().__init__("top_hat", False, 1, False)
    def update(pos, world, groundItems):
        if not functions.isSolid(world,pos[0], pos[1]+1):
            underBlock = functions.getWorldLit(world,pos[0],pos[1]+1)
            world[pos[0], pos[1]+1] = top_hat()
            world[pos[0], pos[1]] = underBlock
        return world, groundItems

class clock(Block):
    hasUp = False
    def __init__(self):
        super().__init__("clock", True, 4, True)

class piston(Block):
    hasUp = True
    def __init__(self):
        super().__init__("piston", True, 4, False)
    def update(pos, world, groundItems):
        if functions.getWorldPower(world, pos[0]-1, pos[1]) or functions.getWorldPower(world, pos[0]+1, pos[1]) or functions.getWorldPower(world, pos[0], pos[1]-1) or functions.getWorldPower(world, pos[0], pos[1]+1):
            if functions.isSolid(world, pos[0]+1, pos[1]) and not functions.getWorld(world, pos[0]+2, pos[1]):
                pygame.mixer.Sound("sounds\\piston.wav").play()
                moveBlock = functions.getWorldLit(world, pos[0]+1, pos[1])
                world[pos[0]+1, pos[1]] = air()
                world[pos[0]+2, pos[1]] = moveBlock
        return world, groundItems

class sign(Block):
    hasUp = False
    def __init__(self):
        super().__init__("sign", False, 2, False)
        self.text = easygui.enterbox("Sign text: ", "PixelGame - New Sign")

class tnt(Block):
    hasUp = True
    def __init__(self):
        super().__init__("tnt", True, 1, False)
    def update(pos, world, groundItems):
        if functions.getWorldPower(world, pos[0]-1, pos[1]) or functions.getWorldPower(world, pos[0]+1, pos[1]) or functions.getWorldPower(world, pos[0], pos[1]-1) or functions.getWorldPower(world, pos[0], pos[1]+1):
            pygame.mixer.Sound("sounds\\boom.wav").play()
            world[pos] = air()
            for xMod in range(-5,5):
                for yMod in range(-5,5):
                    if random.randint(0,4) != 0:
                        functions.removeBlock(world, groundItems, pos[0]+xMod, pos[1]+yMod )
        return world, groundItems

class pipe(Block):
    hasUp = False
    def __init__(self):
        super().__init__("pipe", True, 3, False)








if __name__ == "__main__":
    print("""
================================================
 || Hey! This is the wrong file, use main.py ||
================================================
""")
