import time
import pgzrun
import random
import threading

import blocks
from blocks import Block

#Options-------------------#
seed = random.randint(0,999999)
worldWidth =50
worldHeight = 50
performance = 1 # 1 is normal, 2 for larger worlds and higher
#Options-------------------#

WIDTH = 8*worldWidth
HEIGHT = 8*worldHeight
TITLE = "Sandbox game"

t = 0

taX = 0
taY = worldHeight-1

thatKey = []

blocksStr = ["dirt","grass","log","leaves"]
blocksClass = [blocks.dirt,blocks.grass,blocks.log,blocks.leaves]
blocksAmt = len(blocksStr)-1
selNo = 0
selBlock = blocks.dirt
selBlockStr = "dirt"
inventory = {"dirt":0,"grass":0,"log":0,"leaves":0}

player = Actor("player") #Uses the pixel co-ords
player.left = 0
player.top = -0.45
pXVel = 0
pYVel = 0
jumpT = 10

grav = 0.5
res = 0.9

#Put here so it can be used in world gen --
def isSolid(x,y):
    try:
        return world[(x//8,y//8)].solid
    except:
        return True

#World gen --
random.seed(seed)
heightMap = {0:int(worldHeight/2)}
for x in range(1,worldWidth):
    heightMap[x] = random.randint(heightMap[x-1]-1,heightMap[x-1]+1)

def getWorldType(x,y): #X, Y in blocks not pixels
    try:
        return world[(x,y)].type
    except:
        return "dirt"

def getWorld(x,y): #X, Y in blocks not pixels
    try:
        if getWorldType(x,y) == "air":
            return False
        else:
            return True
    except:
        return True

def appIf(x, y): #X, Y in blocks not pixels
    global halfTrueThing
    x *= 8
    y *= 8
    if getWorld(x,y):
        halfTrueThing += 1
        if halfTrueThing == 2:
            halfTrueThing = 0
            gapChanceList.append(True)
    else:
        gapChanceList.append(False)
    
world = {}
for x in range(0,worldWidth):
    for y in range(0,worldHeight):
        gapChanceList = [False]
        halfTrueThing = 0
        for i in range(0,10):
            appIf(x-1,y)
            appIf(x+1,y)
            appIf(x,y+1)
            appIf(x,y-1)
            if random.choice(gapChanceList) and  y >= heightMap[x]:
                newBlock = Block()
                newBlock.solid = True
                if not getWorld(x,y-1):
                    newBlock.type = "grass"
                else:
                    newBlock.type = "dirt"
                world[(x,y)] = newBlock
            else:
                world[(x,y)] = blocks.air()
#Trees-
for x in range(0,worldWidth):
    for y in range(0,worldHeight):
        if y in range(heightMap[x]-1,heightMap[x]) and getWorldType(x,y+1)=="grass" and (getWorld(x-1,y)==False and getWorld(x+1,y)==False):
            highestYMod = 0
            for yMod in range(0,random.randint(4,6)):
                if yMod > highestYMod: highestYMod = yMod
                world[(x,y-yMod)] = blocks.log()
            for xLMod in range(-1,2):
                for yLMod in range(-1,1):
                    world[(x+xLMod,y-highestYMod+yLMod)] = blocks.leaves()




#Main game --
def draw():
    if int(t) % performance == 0:
        screen.fill((102,191,255))
        for x in range(0,worldWidth):
            for y in range(0,worldHeight):
                if world[(x,y)].type != "air":
                    screen.blit(world[(x,y)].type +".png",(x*8,y*8))
                    for i in range(1,world[(x,y)].darkness):
                        screen.blit("darkness.png",(x*8,y*8))
    player.draw()
    screen.draw.text(str(inventory),(10,10))
    screen.draw.text(str(selBlock),(10,30))
    

def update(dt):
    tickAll()
    global t
    t+=dt
    dt += 1
    global pXVel
    global pYVel
    global jumpT
    if keys.W in thatKey and jumpT < 10:
        pYVel -= 0.8
        jumpT += 1
    if keys.S in thatKey:
        pYVel += 0.25
    if keys.A in thatKey:
        pXVel -= 0.25
    if keys.D in thatKey:
        pXVel += 0.25
    
    pYVel += grav
    pXVel *= res
    pYVel *= res

    #Collission --
    if isCollide(player.left + pXVel, player.top, player.right + pXVel, player.bottom):
        pXVel = 0
        jumpT -= 0.3
    if isCollide(player.left, player.top + pYVel, player.right, player.bottom + pYVel):
        pYVel = 0
        jumpT = 0
    
    #Applying Vels --
    player.left += pXVel*dt
    player.top += pYVel*dt

    #Is Stuck check --
    if isCollide(player.left,player.top,player.right,player.bottom) and thatKey != []:
        player.left -= pXVel*1.5
        player.top -= pYVel*1.5
        pXVel = 0
        pYVel = 0

def on_key_down(key):
    global thatKey
    thatKey.append(key)

def on_key_up(key):
    global thatKey
    if key in thatKey:
        thatKey.remove(key)

# --
def tick(x,y):
    global world
    exec("""if blocks."""+world[(x,y)].type+""".hasUp == True: \n    blocks."""+ world[(x,y)].type +""".update((x,y),world)""")
    if world[(x,y)].type == "log":
        if not getWorld(x,y+1):
            removeBlock(x*8,y*8)

            
def tickAll():
    global taX
    currentDark = 0
    for taY in range(worldHeight-1,0,-1):
        if getattr(blocks, world[(taX,taY)].type).hasUp == True:
            tick(taX,taY)
        world[(taX,taY)].darkness = currentDark
        if world[(taX,taY)].solid:
            currentDark += 1
        else:
            currentDark = 0
    taX += 1
    if taX == worldWidth: taX = 0

def isCollide(x,y,xB,yB):
    xB -= 1
    yB -= 1
    if not isSolid(x,y):
        if not isSolid(xB,y):
            if not isSolid(x,yB):
                if not isSolid(xB,yB):
                    if not isSolid(x,y+7):
                        if not isSolid(xB,y+7):
                            return False
    return True

def on_mouse_down(button,pos):
    global selNo
    global selBlock
    global blocksAmt
    if button == mouse.LEFT:
        addBlock(pos[0],pos[1])
    elif button == mouse.RIGHT:
        removeBlock(pos[0],pos[1])
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

def addBlock(x,y):
    global world
    global inventory
    global selBlock
    x= x//8
    y = y//8
    if not getWorld(x,y) and inventory[selBlockStr] > 0:
        inventory[selBlockStr] -= 1
        exec("world[(x,y)] = blocks."+ selBlockStr +"()")

def removeBlock(x,y):
    global world
    global inventory
    x= x//8
    y = y//8
    if world[(x,y)].type != "air":
        inventory[ getWorldType(x,y) ] += 1
        world[(x,y)] = blocks.air()

pgzrun.go() #Run the game
