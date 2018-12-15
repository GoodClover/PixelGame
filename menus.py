class button():
	def __init__(self, pos, w, h, code):
		self.pos = pos
		self.w = w
		self.h = h
		self.code = code


class menu():
	def __init__(self, img, pos):
		self.image = img
		self.pos = pos
		self.buttons = []


def addButton(theMenu, pos, w, h, code):
	theMenu.buttons.append(button(pos, w, h, code))








def printHi():
	print("Hello")

class testMenu(menu):
	def __init__(self):
		super().__init__("inv_menu", (0, 0))
		addButton(self, (99, 113), 57, 37, printHi)