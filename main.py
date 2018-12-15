import os
try:
    import pygame
    import pgzrun
except:
    print("Can't find libraries! Installing now.")
    os.system("pip3 install pgzero")
    import pygame
    import pgzrun
import random

from functions import *
import blocks
from blocks import Block
import menus
import entities

#Options------------------------#
seed = random.randint(0, 999999)
worldWidth  = 50
worldHeight = 50
shaders = False #Very slow
cursorBox = True
drawAir = False #Ugly
#Options------------------------#

WIDTH = 8*worldWidth
HEIGHT = 8*worldHeight
TITLE = "Sandbox game"
ICON = "icons/devIcon.png"

FONT, FONT_SIZE = "pocket_pixel", 16

menu = menus.testMenu()

pygame.mouse.set_visible(False)

t = 0
f = 0

fps = 0
fpsT = 0
fpsF = 0

taX = 0
taY = worldHeight-1

menuOpen = False
menuOpenDelay = 0

mousePos = (0, 0)
thatKey = []

blocksStr = ["dirt", "stone", "ore", "grass", "sand", "log", "leaves", "water", "tap", "flower"] #All types of block need to be in here!!!
blocksClass = []
for item in blocksStr:
    blocksClass.append(getattr(blocks, item))
blocksAmt = len(blocksStr)-1
selNo = 0
selBlock = blocks.dirt
selBlockStr = "dirt"
inventory = {}
for item in blocksStr:
    try: inventory[item]
    except KeyError:
        inventory[item] = 0

player = Actor("player") #Uses the pixel co-ords
player.left = 0
player.top = -0.45
pHealth = 8
pAir = 8
pXVel = 0
pYVel = 0
jumpT = 10

grav = 0.5
res = 0.9

#Main game --
def draw():
    screen.fill((102, 191, 255))
    if not menuOpen:
        for x in range(0, worldWidth):
            for y in range(0, worldHeight):
                if drawAir or world[(x, y)].type != "air":
                    screen.blit(world[(x, y)].type, (x*8, y*8))
                if shaders:                                        #Shaders
                    for i in range(1, world[(x, y)].darkness//3):
                        screen.blit("darkness", (x*8, y*8))
        player.draw()                                              #Player
        screen.blit("sel_box", (6, 30))               #Selected block
        screen.blit(selBlockStr, (8, 32))
        screen.draw.text(str(inventory[selBlockStr])+" "+selBlockStr, (22, 28), FONT, FONT_SIZE)
    elif menuOpen:
        screen.blit(menu.image, menu.pos)

    for i in range(0, int(pHealth)*8, 8):         #Health meter
        screen.blit("health_meter.png", (8+i, 8))
    for i in range(0, int(pAir)*8, 8):            #Air meter
        screen.blit("air_meter.png", (8+i, 18))
    if cursorBox and not menuOpen:                               #Cursor
        screen.blit("cursor_box", (mousePos[0]-6, mousePos[1]-6))
    else:
        screen.blit("cursor", (mousePos[0]-6, mousePos[1]-6))
    screen.draw.text("FPS: "+str(int(fps)), (8, 46), FONT, FONT_SIZE)      #FPS

    

def update(dt):
    global pAir
    global pHealth
    global world
    global taX
    global inventory
    global t
    global f
    global fps
    global fpsT
    global fpsF
    global pXVel
    global pYVel
    global jumpT
    global mousePos
    global menuOpen
    global menuOpenDelay

    t += dt
    f += 1

    fpsT += dt
    fpsF += 1
    fps = fpsF/fpsT
    if fpsT >= 1:
        fpsT = 0
        fpsF = 0

    menuOpenDelay  -= dt

    dt += 1 #Temporary so the equations work a little nicer

    world, taX, inventory = tickAll(world, taX, inventory)

    if pHealth <= 0:
        for x in range(0, worldWidth):
            for y in range(0, worldHeight):
                world[x, y] = blocks.air()
        pXVel, pYVel = 0, 0
    if pAir <= 0:
        pAir = 0
        pHealth -= 0.02

    if keys.W in thatKey and jumpT < 10:
        if getWorldType(world, (player.left+4)//8, (player.top//8)+1) == "water":
            pYVel -= 0.2*dt
        else:
            pYVel -= 0.8*dt
            jumpT += 1
    if keys.S in thatKey:
        pYVel += 0.25*dt
    if keys.A in thatKey:
        pXVel -= 0.25*dt
    if keys.D in thatKey:
        pXVel += 0.25*dt
    
    if getWorldType(world, (player.left+4)//8, (player.top//8)+1) == "water":
        pAir -=0.02
        pYVel += grav*0.15
    else:
        pAir = 8
        pYVel += grav
    pXVel *= res
    pYVel *= res

    if pHealth <= 0:
        pXVel, pYVel = 0, 0

    #Collission --
    if isCollide(world, player.left + pXVel, player.top, player.right + pXVel, player.bottom):
        pXVel = 0
        jumpT -= 0.3
    if isCollide(world, player.left, player.top + pYVel, player.right, player.bottom + pYVel):
        pYVel = 0
        jumpT = 0
    
    #Applying Vels --
    player.left += pXVel*dt
    player.top += pYVel*dt

    #Is Stuck check --
    if isCollide(world, player.left, player.top, player.right, player.bottom) and thatKey != []:
        player.left -= pXVel*1.5
        player.top -= pYVel*1.5
        pXVel = 0
        pYVel = 0
        pHealth -= 0.1

    if keys.R in thatKey:
        for bX in range(0, worldWidth):
            for bY in range(0, worldHeight):
                removeBlock(world, inventory, bX*8, bY*8)
    if keys.E in thatKey and menuOpenDelay <= 0:
        menuOpenDelay = 0.2
        menuOpen = not menuOpen

def on_key_down(key):
    global thatKey
    thatKey.append(key)
            

def on_key_up(key):
    global thatKey
    if key in thatKey:
        thatKey.remove(key)
    
def tickAll(world, taX, inventory):
    currentDark = 0
    for taY in range(0, worldHeight):
        if getattr(blocks, world[(taX, taY)].type).hasUp == True:
            world = tick(world, taX, taY, inventory)
        world[(taX, taY)].darkness = currentDark
        if world[(taX, taY)].solid:
            currentDark += 1
    taX += 1
    if taX == worldWidth: taX = 0
    return world, taX, inventory

def isCollide(world, x, y, xB, yB):
    xB -= 1
    yB -= 1
    if not isSolidP(world, x, y):
        if not isSolidP(world, xB, y):
            if not isSolidP(world, x, yB):
                if not isSolidP(world, xB, yB):
                    if not isSolidP(world, x, y+7):
                        if not isSolidP(world, xB, y+7):
                            return False
    return True

def on_mouse_move(pos):
    global mousePos
    mousePos = pos

def on_mouse_down(button, pos):
    global selNo
    global selBlock
    global selBlockStr
    global blocksAmt
    global world
    global taX
    global inventory

    if button == mouse.LEFT and not menuOpen:
        sounds.thump.play()
        addBlock(world, inventory, selBlockStr, mousePos[0], mousePos[1])
        world, taX, inventory = tickAll(world, mousePos[0]//8, inventory)

    elif button == mouse.LEFT and menuOpen:
        for button in menu.buttons:
            if pos[0] > button.pos[0] and pos[0] < button.pos[0]+button.w:
                if pos[1] > button.pos[1] and pos[1] < button.pos[1]+button.h:
                    button.code()

    elif button == mouse.RIGHT and not menuOpen:
        sounds.pick1.play()
        if world[(mousePos[0]//8, mousePos[1]//8)].type != "air":
            selBlockStr = world[(mousePos[0]//8, mousePos[1]//8)].type
            selBlock = getattr(blocks, selBlockStr)
        removeBlock(world, inventory, mousePos[0], mousePos[1])
        world, taX, inventory = tickAll(world, mousePos[0]//8, inventory)

    elif button == mouse.WHEEL_UP:
        selNo += 1
        if selNo > blocksAmt:
            selNo = 0
        selBlock = blocksClass[selNo]
        selBlockStr = blocksStr[selNo]
    elif button == mouse.WHEEL_DOWN:
        selNo -= 1
        if selNo == -1:
            selNo = blocksAmt
        selBlock = blocksClass[selNo]
        selBlockStr = blocksStr[selNo]








#World gen --
random.seed(seed)
heightMap = {0:int(worldHeight/2)}
for x in range(1, worldWidth):
    heightMap[x] = random.randint(heightMap[x-1]-1, heightMap[x-1]+1)

def appIf(x, y): #X, Y in blocks not pixels
    global halfTrueThing
    global gapChanceList
    x *= 8
    y *= 8
    if getWorld(world, x, y):
        halfTrueThing += 1
        if halfTrueThing == 2:
            halfTrueThing = 0
            gapChanceList.append(True)
    else:
        gapChanceList.append(False)
    
world = {}
for x in range(0, worldWidth):
    for y in range(0, worldHeight):
        gapChanceList = [False]
        halfTrueThing = 0
        for i in range(0, 10):
            appIf(x-1, y)
            appIf(x+1, y)
            appIf(x, y+1)
            appIf(x, y-1)
        if random.choice(gapChanceList) and  y >= heightMap[x]:
            newBlock = Block()
            newBlock.solid = True
            if y <= heightMap[x]+5:
                newBlock.type = "dirt"
            else:
                newBlock.type = "stone"
            world[(x, y)] = newBlock
        else:
            world[(x, y)] = blocks.air()
        tick(world, x, y, inventory)
#Water --
for x in range(0, worldWidth):
    for y in range(0, worldHeight):
        if y >= worldHeight//2 and getWorldType(world, x, y) == "air" and y <= heightMap[x] and random.choice([True, True, True, False]):
            world[x, y] = blocks.water()
#Settle Water --
for i in range(0,25):
    for taX in range(0, worldWidth):
        world,taX,inventory = tickAll(world, taX, inventory)
#Sandify --
for x in range(0, worldWidth):
    for y in range(0, worldHeight):
        if getWorldType(world,x+1,y) == "water" or getWorldType(world,x-1,y) == "water" or getWorldType(world,x,y-1) == "water" or getWorldType(world,x+2,y) == "water" or getWorldType(world,x-2,y) == "water" or getWorldType(world,x,y-2) == "water":
            if getWorldType(world,x,y) != "air" and getWorldType(world,x,y) != "water":
                world[x,y] = blocks.sand()
#Add ore --
for x in range(0, worldWidth):
    for y in range(0, worldHeight):
        if getWorldType(world, x, y) == "stone" and random.choice([True,False,False,False,False,False,False,False]):
            world[x,y] = blocks.ore()
#Trees --
for x in range(0, worldWidth):
    for y in range(0, worldHeight):
        if y in range(heightMap[x]-1, heightMap[x]) and getWorldType(world, x, y+1)=="grass" and (getWorld(world, x-1, y)==False and getWorld(world, x+1, y)==False):
            highestYMod = 0
            for yMod in range(0, random.randint(4, 6)):
                if yMod > highestYMod: highestYMod = yMod
                world[(x, y-yMod)] = blocks.log()
            for xLMod in range(-1, 2):
                for yLMod in range(-1, 1):
                    world[(x+xLMod, y-highestYMod+yLMod)] = blocks.leaves()
#Flowers --
for x in range(0, worldWidth):
    for y in range(0, worldHeight):
        if getWorldType(world, x, y) == "grass" and getWorldType(world, x, y-1) == "air" and random.randint(0,3)==0:
            world[(x, y)] = blocks.flower()





print("\nPixelGame by GoodClover")
pgzrun.go() #Run the game
