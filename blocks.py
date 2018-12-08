#All the blocks


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
    def update(pos, world):                 #
        pass                                #

class air(Block):
    hasUp = False
    def __init__(self):
        super().__init__("air", False, -1) #Not Solid, Unbreakable
    def update(pos, world):
        pass

class dirt(Block):
    hasUp = True
    def __init__(self):
        super().__init__("dirt", True, 4)
    def update(pos, world):
        try:
            if not world[pos[0],pos[1]-1].solid:
                world[pos].type = "grass"
        except:
            pass


class grass(Block):
    hasUp = True
    def __init__(self):
        super().__init__("grass", True, 4)
    def update(pos, world):
        try:
            if world[pos[0],pos[1]-1].solid:
                world[pos].type = "dirt"
        except:
            pass

class log(Block):
    hasUp = True
    def __init__(self):
        super().__init__("log", True, 4)
    def update(pos, world):
        if world[(pos[0],pos[1]+1)].type == "air":
            world[pos] = air()

class leaves(Block):
    hasUp = True
    def __init__(self):
        super().__init__("leaves", False, 2)
    def update(pos, world):
        tlN = 0
        tl = False
        for xM in range(-1,2):
            for yM in range(-2,3):
                try:
                    if world[pos[0]+xM,pos[1]+yM].type == "log":
                        tlN += 1
                except:
                    pass
        if tlN > 0: tl = True
        if not tl:
            world[pos] = air()

class water(Block):
    hasUp = True
    def __init__(self):
        super().__init__("water", False, 4) #Not Solid
    def update(pos, world):
        try:
            if world[pos[0],pos[1]+1].type != "water":
                if world[pos[0],pos[1]+1].type == "air":
                    world[pos[0], pos[1]+1] = water()
                elif world[pos[0]+1,pos[1]].type == "air":
                    world[pos[0]+1, pos[1]] = water()
                elif world[pos[0]-1,pos[1]].type == "air":
                    world[pos[0]-1, pos[1]] = water()
        except:
            pass








if __name__ == "__main__":
    print("""
================================================
 || Hey! This is the wrong file, use main.py ||
================================================
""")
