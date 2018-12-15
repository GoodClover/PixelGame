import random

from functions import *
import functions

#Base class
class Entity():
    def __init__(self, eType="pig", pos=(0, 0), health=4):
        self.type = eType
        self.health = health
        self.pos = pos




#The entitys
class pig(Entity):
	grav = True
	hasUp = True
	def __init__(self):
		super().__init__("pig", (40, 10), 4)
	def update(self, world):
		self.pos = (self.pos[0]+random.randint(-2,2), self.pos[1])
		if not functions.isSolid(world, self.pos[0]//8, self.pos[1]//8):
			self.pos = (self.pos[0], self.pos[1]+1)
		return world, self







if __name__ == "__main__":
    print("""
================================================
 || Hey! This is the wrong file, use main.py ||
================================================
""")
