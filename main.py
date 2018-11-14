import pgzrun
import random
import threading

WIDTH = 8*50
HEIGHT = 8*50
TITLE = "Test sandbox game"

t = 0

tcX = 0
tcY = 0

thatKey = []

blockAmount = 0

player = Actor("player") #Uses the pixel co-ords
player.left = 0
player.top = -0.45
pXVel = 0
pYVel = 0
jumpT = 0

grav = 0.5
res = 0.9

#World gen --
#random.seed(int(input("Seed: ")))
heightMap = {0:25}
for x in range(1,50):
    heightMap[x] = random.randint(heightMap[x-1]-1,heightMap[x-1]+1)

world = {}
worldType = {}
gapChanceList = [False]
for i in range(0,10):
    gapChanceList.append(True)
for x in range(0,50):
    for y in range(0,50):
        if random.choice(gapChanceList) and  y >= heightMap[x]:
            world[(x,y)] = True
            worldType[(x,y)] = "dirt"
        else:
            world[(x,y)] = False
            worldType[(x,y)] = "air"

#Main game --
def draw():
    screen.fill((102,191,255))
    for x in range(0,50):
        for y in range(0,50):
            if worldType[(x,y)] != "air":
                screen.blit(worldType[(x,y)]+".png",(x*8,y*8))
    player.draw()
    screen.draw.text(str(blockAmount),(10,10))
    

def update(dt):
    threading.Thread(target=ticker()).start()
    global t
    t+=dt
    global pXVel
    global pYVel
    global jumpT
    if keys.W in thatKey and jumpT < 10:
        pYVel -= 1
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
    if isCollide(player.left, player.top + pYVel, player.right, player.bottom + pYVel):
        pYVel = 0
        jumpT = 0
    
    #Applying Vels --
    player.left += pXVel
    player.top += pYVel

    #Is Stuck check --
    if isCollide(player.left,player.top,player.right,player.bottom) and thatKey != []:
        player.right += 1

def on_key_down(key):
    global thatKey
    thatKey.append(key)

def on_key_up(key):
    global thatKey
    if key in thatKey:
        thatKey.remove(key)

def tick(x,y):
    if worldType[(x,y)] == "dirt":
        try:
            if not world[(x,y-1)]:
                worldType[(x,y)] = "grass"
        except:
            worldType[(x,y)] = "grass"

def ticker():
    global tcX
    global tcY
    tick(tcX,tcY)
    tcY += 1
    if tcY == 50:
        tcY = 0
        tcX += 1
        if tcX == 50:
            tcX = 0 

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

def isSolid(x,y):
    try:
        return world[(x//8,y//8)]
    except:
        return False

def on_mouse_down(button,pos):
    if button == mouse.LEFT:
        addBlock(pos[0],pos[1])
    elif button == mouse.RIGHT:
        removeBlock(pos[0],pos[1])

def addBlock(x,y):
    global world
    global blockAmount
    if not world[(x//8,y//8)] and blockAmount > 0:
        world[(x//8,y//8)] = True
        worldType[(x//8,y//8)] = "dirt"
        blockAmount -= 1

def removeBlock(x,y):
    global world
    global blockAmount
    if world[(x//8,y//8)]:
        world[(x//8,y//8)] = False
        worldType[(x//8,y//8)] = "air"
        blockAmount += 1


pgzrun.go() #Run the game
