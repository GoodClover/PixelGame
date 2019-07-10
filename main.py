credits = "Error, \"credits.txt\" not found!"
with open("credits.txt", "r") as file:
    credits = file.read()

#Scroll down for options

#Librares
print("Loading libraries...")
import os
import sys
try:
    import pygame
    import pgzrun
    import pickle
    import easygui
except ImportError:
    print("\nCan't find libraries!")
    if input("Do you want to auto install them now? (Y/N)").upper() == "Y":
        print("Installing libraries...")
        try:
            os.system("python -m pip install --upgrade pip")
        except:
            #This is incase that the command dosn't work
            pass
        os.system("pip3 install pgzero")
        os.system("pip3 install pickle")
        os.system("pip3 install easygui")
        import pygame
        import pgzrun
        import pickle
        import easygui
        print("Installed libraries")
    else:
        print("\nIf you want to play they need to be intalled.")
        print("""Libraries:
         - "pgzero" (pygame included)
         - "pickle"
         - "easygui"
        """)
        input("Press enter to continue with the error...")
        raise
import random
import time

from functions import *
import blocks
from blocks import Block
import entities

#Loading
print("Loaded libraries!")
print("\n"+credits+"\n")
print("Loading game...")

#Options------------------------#
seed = 0
worldWidth  = 200
worldHeight = 50
shaders = False #Very slow
transparency = True
blob = True
blobOthers = False
HEIGHT = 300 #If the games slow change this e.g 1080 is 1080p
drawBG = True
rowsPerUpdate = 30
cursorBox = True
drawAir = False #Ugly
scroll = True
noGrav = False
zoomWindow = True
#Options------------------------#

WIDTH = (HEIGHT//9)*16
TITLE = "PixelGame - Oliver Simmons"
ICON = "icons/devIcon.png"

FONT, FONT_SIZE, FONT_COLOUR = "pocket_pixel", 16, (25, 25, 25)

pygame.mouse.set_visible(False)

t = 0
f = 0

fps = 0
fpsT = 0
fpsF = 0

taX = 0
taY = worldHeight-1

dustParticles = []
clouds = []
for i in range(0,WIDTH//40):
    clouds.append( ( random.randint(-59,WIDTH), random.randint(0,HEIGHT//1.5), random.randint(1,5)/10 ) )

menuOpen = False
menuOpenDelay = 0

mousePos = (0, 0)
thatKey = []

blocksStr = [
    "dirt",
    "stone",
    "ore",
    "grass",
    "sand",
    "log",
    "planks",
    "wall",
    "ladders",
    "chest",
    "leaves",
    "tap",
    "water",
    "flower",
    "top_hat",
    "clock",
    "piston",
    "sign",
    "tnt",
    "pipe",
    "debug",
    ] #All types of block need to be in here!!!
blocksClass = []
blocksImage = {}
blocksBlob = {}
for item in blocksStr:
    blocksClass.append(getattr(blocks, item))
    if transparency:
        blocksImage[item] = pygame.image.load("images/"+item+".png").convert_alpha()
        try:
            for i in range(0,16):
                blocksBlob[item,i] = pygame.image.load("images/"+item+"/"+str(i)+".png").convert_alpha()
        except: pass
    else:
        blocksImage[item] = pygame.image.load("images/"+item+".png").convert()
        try:
            for i in range(0,16):
                blocksBlob[item,i] = pygame.image.load("images/"+item+"/"+str(i)+".png").convert()
        except: pass
darkness = pygame.image.load("images/darkness.png").convert_alpha()

blocksAmt = len(blocksStr)-1
selNo = 0
selBlock = blocks.dirt
selBlockStr = "dirt"

inventory = {}
totalInventory = 0
for item in blocksStr:
    try: inventory[item]
    except KeyError:
        inventory[item] = 0

groundItems = []
groundItems.append(groundItem((8,8),"top_hat"))

player = Actor("player") #Uses the pixel co-ords
player.left = (worldWidth*8)/2
player.top = 0
pHealth = 8
pAir = 8
pXVel = 0
pYVel = 0
jumpT = 10

scrollX = 0
scrollY = 0

grav = 0.5
res = 0.9

facingLeft = True

#Main game --
def draw():
    screen.fill((102, 191, 255))
    if drawBG:
        screen.blit("sun", (0,0))
        for cloud in clouds:
            screen.blit("cloud", (cloud[0], cloud[1]) )
    if not menuOpen:
        for x in range(0, worldWidth):
            for y in range(0, worldHeight):
                if drawAir or world[(x, y)].type != "air":
                    if ((y*8)-scrollY > -8) and ((y*8)-scrollY < HEIGHT+8):
                        if ((x*8)-scrollX > -8) and ((x*8)-scrollX < WIDTH+8):
                            if blob: #Blob --
                                #screen.blit("blob/"+str(world[(x, y)].blob), ( (x*8)-scrollX, (y*8)-scrollY) )
                                try: screen.blit( blocksBlob[world[(x, y)].type, world[(x, y)].blob] , ( (x*8)-scrollX, (y*8)-scrollY) )
                                except: screen.blit( blocksImage[world[(x, y)].type] , ( (x*8)-scrollX, (y*8)-scrollY) )
                            else:
                                screen.blit( blocksImage[world[(x, y)].type] , ( (x*8)-scrollX, (y*8)-scrollY) )
                            if world[(x, y)].durability < world[(x, y)].maxDurability and world[(x, y)].durability >= 0:
                                screen.blit("dura"+str(world[(x, y)].durability), ( (x*8)-scrollX, (y*8)-scrollY) )
                            if shaders: #Shaders --
                                for i in range(1, world[(x, y)].darkness//3):
                                    screen.blit(darkness, ( (x*8)-scrollX, (y*8)-scrollY) )

        for dust in dustParticles:
            pos = (dust[0]-scrollX, dust[1]-scrollY)
            screen.draw.line(pos, pos, dust[4])

        for gItem in groundItems:
            screen.blit(gItem.type, (gItem.pos[0]-scrollX, gItem.pos[1]-scrollY) )

        #player.draw()                                              #Player
        if pXVel <= 0:
            if getWorldType(world, (player.left+4)//8, (player.top+17)//8) == "air":
                screen.blit("player-j", (player.left-scrollX-1, player.top-scrollY-1))
            elif getWorldType(world, (player.left+4)//8, (player.top+17)//8) == "water":
                screen.blit("player-s", (player.left-scrollX-1, player.top-scrollY-1))
            else: screen.blit("player", (player.left-scrollX-1, player.top-scrollY-1))
            screen.blit("arms", (player.left-scrollX-3-1, player.top-scrollY-1))
            if int(t) % 3 == 0: screen.blit("eyelid", (player.left-scrollX-1, player.top-scrollY-1))
        elif pXVel > 0:
            if getWorldType(world, (player.left+4)//8, (player.top+17)//8) == "air":
                screen.blit("player-r-j", (player.left-scrollX-1, player.top-scrollY-1))
            elif getWorldType(world, (player.left+4)//8, (player.top+17)//8) == "water":
                screen.blit("player-r-s", (player.left-scrollX-8-1, player.top-scrollY-1))
            else: screen.blit("player-r", (player.left-scrollX-1, player.top-scrollY-1))
            screen.blit("arms", (player.left-scrollX-3-1, player.top-scrollY-1))
            if int(t) % 3 == 0: screen.blit("eyelid-r", (player.left-scrollX-1, player.top-scrollY-1))
        if inventory["top_hat"] >= 1: screen.blit("top_hat", (player.left-scrollX-1, player.top-scrollY-4-1))

    global menuOpenDelay       #Screenshot
    if keys.F11 in thatKey and menuOpenDelay <= 0:
        menuOpenDelay = 0.2
        cTime = time.ctime()
        cTime = cTime.replace(":",";")
        cTime = cTime[:10]+" - "+cTime[11:]
        pygame.image.save(screen.surface, "screenshots/screenshot - "+cTime+".png")
        #screenshot - DDD MMM DD - HH;MM;SS YYYY
        #screenshot - Mon Jan 01 - 13;30;59 2018.png
        #Semicolons because colons arent allowed in Windows

    #GUI things
    if not menuOpen:
        screen.blit("sel_box", (6, 30))               #Selected block
        screen.blit(selBlockStr, (8, 32))
        screen.draw.text(str(inventory[selBlockStr])+" "+selBlockStr, (22, 28), FONT, FONT_SIZE, color=FONT_COLOUR)
    elif menuOpen:
        pass ################################

    for i in range(0, int(pHealth)*8, 8):         #Health meter
        screen.blit("health_meter.png", (8+i, 8))
    for i in range(0, int(pAir)*8, 8):            #Air meter
        screen.blit("air_meter.png", (8+i, 18))
    if cursorBox and not menuOpen:                               #Cursor
        screen.blit("cursor_box", (mousePos[0]-6, mousePos[1]-6))
    if zoomWindow and not menuOpen:
        screen.blit("zoom_window", (mousePos[0]+6+1, mousePos[1]-6-32)) #The area is 8x8 -> 32x32
        preZoomSurface = pygame.Surface((8,8))
        zoomSurface = pygame.Surface((32,32))
        preZoomSurface.blit(screen.surface, (0,0), (mousePos[0]-4, mousePos[1]-4, 8, 8) )
        zoomSurface.blit(pygame.transform.scale( preZoomSurface, (32,32) ), (0,0))
        screen.blit(zoomSurface, (mousePos[0]+6+3, mousePos[1]-6-32+2))
    screen.blit("cursor", (mousePos[0]-6, mousePos[1]-6))
    if getWorldType(world, (mousePos[0]+scrollX)//8, (mousePos[1]+scrollY)//8 ) == "sign":
        screen.draw.text(world[(mousePos[0]+scrollX)//8, (mousePos[1]+scrollY)//8].text, (mousePos[0]+7, mousePos[1]-3), FONT, FONT_SIZE, color=FONT_COLOUR)

    screen.draw.text("FPS: "+str(int(fps)), (8, 46), FONT, FONT_SIZE, color=FONT_COLOUR)      #FPS
    #screen.blit("debug", (int(player.left-scrollX), int(player.top-scrollY)))



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
    global pXVel, pYVel
    global jumpT
    global mousePos
    global menuOpen
    global menuOpenDelay
    global player
    global scrollX, scrollY
    global dustParticles
    global groundItems
    global facingLeft
    global clouds
    global zoomWindow
    global cursorBox
    global noGrav
    global blob, blobOthers
    global selNo, selBlockStr, selBlock
    global totalInventory
    global shaders
    global transparency

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

    totalInventory = 0
    for i in inventory:
        totalInventory += inventory[i]

    for taX in range(taX, taX+rowsPerUpdate):
        ptaX = taX
        if ptaX > worldWidth-1:
            ptaX = 0
        world,taX,inventory,groundItems = tickAll(world, ptaX, inventory, groundItems)

    newDP = []
    for dust in dustParticles:
        if dust[3] < 0: dust = ( dust[0]+random.randint(0,2), dust[1], dust[2], dust[3], dust[4] )
        elif dust[3] > 0: dust = ( dust[0]+random.randint(-2,0), dust[1], dust[2], dust[3], dust[4] )
        dust = ( dust[0], dust[1]-random.randint(0,3), dust[2]-random.randint(0,3), dust[3], dust[4] )
        if dust[2] > 0:
            newDP.append(dust)
    dustParticles = newDP

    newClouds = []
    for cloud in clouds:
        if cloud[0] > WIDTH:
            cloud = (-70, random.randint(0,HEIGHT//2), random.randint(1,5)/10)
        newClouds.append( (cloud[0]+cloud[2], cloud[1], cloud[2]) )
    clouds = newClouds

    for gItem in groundItems: #Ground items calcs
        if player.colliderect( Rect(gItem.pos, (8,8)) ):
            inventory[gItem.type] += 1
            groundItems.remove(gItem)
        elif isSolid(world, gItem.pos[0]//8, gItem.pos[1]//8) or isSolid(world, (gItem.pos[0]+7)//8, (gItem.pos[1]+7)//8) or isSolid(world, (gItem.pos[0]+7)//8, gItem.pos[1]//8) or isSolid(world, gItem.pos[0]//8, (gItem.pos[1]+7)//8):
            gItem.pos = (gItem.pos[0]-1, gItem.pos[1]-1)
        elif isSolid(world, gItem.pos[0]//8, gItem.pos[1]//8)==False and isSolid(world, (gItem.pos[0]+8)//8, (gItem.pos[1]+8)//8)==False and isSolid(world, (gItem.pos[0]+8)//8, gItem.pos[1]//8)==False and isSolid(world, gItem.pos[0]//8, (gItem.pos[1]+8)//8)==False:
            gItem.pos = (gItem.pos[0], gItem.pos[1]+1)

    if pHealth <= 0:
        exit()
    if pAir <= 0:
        pAir = 0
        pHealth -= 0.02

    if keys.W in thatKey:
        if not noGrav:
            if getWorldType(world, (player.left+4)//8, (player.top//8)+1) == "water":
                pYVel -= 0.2*dt
            elif getWorldType(world, (player.left+4)//8, (player.top//8)+1) == "ladders":
                pYVel -= 0.2*dt
            elif  jumpT < 10 or noGrav:
                pYVel -= 0.8*dt
                jumpT += 1
        else:
            pYVel -= 0.25*dt
    if keys.S in thatKey:
        pYVel += 0.25*dt
    if keys.A in thatKey:
        pXVel -= 0.25*dt
        facingLeft = True
        if isSolid(world, (player.left+4)//8, (player.top+16)//8):
            dustParticles.append( ((scrollX+WIDTH/2)+random.randint(-2,6), (scrollY+HEIGHT/2)+14, 50, pXVel, screen.surface.get_at((int(player.left-scrollX+4), int(player.top-scrollY+17)))[:3] ))
    if keys.D in thatKey:
        pXVel += 0.25*dt
        facingLeft = False
        if isSolid(world, (player.left+4)//8, (player.top+16)//8):
            dustParticles.append( ((scrollX+WIDTH/2)+random.randint(-2,6), (scrollY+HEIGHT/2)+14, 50, pXVel, screen.surface.get_at((int(player.left-scrollX+4), int(player.top-scrollY+17)))[:3] ))

    if not noGrav:
        if getWorldType(world, (player.left+4)//8, (player.top//8)+1) == "water":
            pAir -=0.02
            pYVel += grav*0.15
        elif getWorldType(world, (player.left+4)//8, (player.top//8)+1) == "ladders":
            pYVel += grav*0.10
        else:
            pAir = 8
            pYVel += grav
    pXVel *= res
    pYVel *= res

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
    if scroll:
        scrollX = player.left-(WIDTH)/2
        scrollY = player.top-(HEIGHT)/2
    else:
        scrollX = 0
        scrollY = 0

    #Is Stuck check --
    if isCollide(world, player.left, player.top, player.right, player.bottom):
        player.left -= pXVel*dt*1.5
        player.top -= pYVel*dt*1.5
        pXVel = 0
        pYVel = 0

    if keys.F6 in thatKey:
        for bX in range(0, worldWidth):
            for bY in range(0, worldHeight):
                removeBlock(world, groundItems, bX, bY)
        for gItem in groundItems:
            gItem.pos = (player.left, HEIGHT)
    if keys.G in thatKey and menuOpenDelay <= 0:
        menuOpenDelay = 0.2
        menuOpen = not menuOpen

    if keys.Q in thatKey:
        if inventory[selBlockStr] > 0 and menuOpenDelay <= 0:
            menuOpenDelay = 0.2
            if facingLeft:
                groundItems.append( groundItem( (player.left-12, player.top), selBlockStr ) )
            elif not facingLeft:
                groundItems.append( groundItem( (player.left+12, player.top), selBlockStr ) )
            inventory[selBlockStr] -= 1

    if keys.E in thatKey and menuOpenDelay <= 0:
        menuOpenDelay = 0.2
        toCraft = easygui.enterbox("What to craft: ", TITLE+" - Crafting")
        howMany = easygui.enterbox("How many: ", TITLE+" - Crafting")
        if howMany == "":
            howMany = 1
        howMany = int(howMany)
        inventory = craft(toCraft, inventory, howMany)

    if keys.LSHIFT in thatKey and menuOpenDelay <= 0:
        menuOpenDelay = 0.2
        zoomWindow = not zoomWindow

    if keys.LCTRL in thatKey and menuOpenDelay <= 0:
        menuOpenDelay = 0.2
        cursorBox = not cursorBox

    if keys.O in thatKey:                                           #Save/Load worlds --
        worldName = easygui.diropenbox("Open: ", "PixelGame - Open", "user/worlds").replace("\\","/") #"Test_World"
        print("\nLoading world...")
        with open(worldName+"/level.pig","rb") as file:
            world = pickle.load(file)
        with open(worldName+"/inventory.pig","rb") as file:
            pickledFile = pickle.load(file)
            for type in pickledFile:
                inventory[type] = pickledFile[type]
        with open(worldName+"/playerActorX.pig","rb") as file:
            player.left = pickle.load(file)
        with open(worldName+"/playerActorY.pig","rb") as file:
            player.top = pickle.load(file)
        with open(worldName+"/gItems.pig","rb") as file:
            groundItems = pickle.load(file)
        print("Loaded world...")
    elif keys.P in thatKey:
        worldName = easygui.diropenbox("Save: ", "PixelGame - Save", "user/worlds") #"Test_World"
        print("\nSaving world...")
        with open(worldName+"/level.pig","wb") as file:
            file.write(bytes())
            pickle.dump(world, file, pickle.HIGHEST_PROTOCOL)
        with open(worldName+"/inventory.pig","wb") as file:
            file.write(bytes())
            pickle.dump(inventory, file, pickle.HIGHEST_PROTOCOL)
        with open(worldName+"/playerActorX.pig","wb") as file:
            file.write(bytes())
            pickle.dump(player.left, file, pickle.HIGHEST_PROTOCOL)
        with open(worldName+"/playerActorY.pig","wb") as file:
            file.write(bytes())
            pickle.dump(player.top, file, pickle.HIGHEST_PROTOCOL)
        with open(worldName+"/gItems.pig","wb") as file:
            file.write(bytes())
            pickle.dump(groundItems, file, pickle.HIGHEST_PROTOCOL)
        print("Saved world...")

    if keys.SLASH in thatKey:
        commandStr = easygui.enterbox("Commands", "PixelGame - Cheaty menu")
        command = commandStr.split()
        if command[0] == "give":
            inventory[command[1]] += int(command[2])
        elif command[0] == "fly":
            noGrav = not noGrav
        elif command[0] == "blob":
            blob = not blob
        elif command[0] == "blobOthers":
            blobOthers = not blobOthers
        elif command[0] == "transparency":
            transparency = not transparency
            for item in blocksStr:
                if transparency:
                    blocksImage[item] = pygame.image.load("images/"+item+".png").convert_alpha()
                    try:
                        for i in range(0,16):
                            blocksBlob[item,i] = pygame.image.load("images/"+item+"/"+str(i)+".png").convert_alpha()
                    except: pass
                else:
                    blocksImage[item] = pygame.image.load("images/"+item+".png").convert()
                    try:
                        for i in range(0,16):
                            blocksBlob[item,i] = pygame.image.load("images/"+item+"/"+str(i)+".png").convert()
                    except: pass
        elif command[0] == "shaders":
            shaders = not shaders
        elif command[0] == "itemsHere":
            for gItem in groundItems:
                gItem.pos = (player.left, player.top)
        else:
            easygui.msgbox("Invalid command", "PixelGame - Cheaty menu")

def tickAll(world, taX, inventory, groundItems):
    taX = int(taX)
    currentDark = 0
    for taY in range(0, worldHeight):
        if getattr(blocks, getWorldType(world, taX, taY)).hasUp:
            world, groundItems = tick(world, taX, taY, inventory, groundItems)
        world[(taX, taY)].darkness = currentDark
        if world[(taX, taY)].solid:
            currentDark += 1
        #Blob -\
        if blobOthers:
            world[(taX, taY)].blob = 0
            if getWorld(world, taX, taY-1):
                world[(taX, taY)].blob += 1
            if getWorld(world, taX+1, taY):
                world[(taX, taY)].blob += 2
            if getWorld(world, taX, taY+1):
                world[(taX, taY)].blob += 4
            if getWorld(world, taX-1, taY):
                world[(taX, taY)].blob += 8
        else:
            world[(taX, taY)].blob = 0
            if isSolid(world, taX, taY-1) == isSolid(world, taX, taY) and getWorldType(world, taX, taY-1) != "air":
                world[(taX, taY)].blob += 1
            if isSolid(world, taX+1, taY) == isSolid(world, taX, taY) and getWorldType(world, taX+1, taY) != "air":
                world[(taX, taY)].blob += 2
            if isSolid(world, taX, taY+1) == isSolid(world, taX, taY) and getWorldType(world, taX, taY+1) != "air":
                world[(taX, taY)].blob += 4
            if isSolid(world, taX-1, taY) == isSolid(world, taX, taY) and getWorldType(world, taX-1, taY) != "air":
                world[(taX, taY)].blob += 8
    taX += 1
    if taX == worldWidth: taX = 0
    return world, taX, inventory, groundItems

def on_key_down(key):
    global thatKey
    thatKey.append(key)


def on_key_up(key):
    global thatKey
    if key in thatKey:
        thatKey.remove(key)

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
    global groundItems

    if button == mouse.LEFT and not menuOpen:
        sounds.thump.play()
        usePos = ( (mousePos[0]+scrollX)//8, (mousePos[1]+scrollY)//8 )
        addBlock(world, inventory, selBlockStr, usePos[0], usePos[1])
        world, taX, inventory, groundItems = tickAll(world, usePos[0], inventory, groundItems)

    elif button == mouse.RIGHT and not menuOpen:
        sounds.pick1.play()
        usePos = ( (mousePos[0]+scrollX)//8, (mousePos[1]+scrollY)//8 )
        if world[usePos].type != "air":
            selBlockStr = world[usePos].type
            selBlock = getattr(blocks, selBlockStr)
            world[usePos].durability -= 1
            if world[usePos].durability == 0:
                removeBlock(world, groundItems, usePos[0], usePos[1])
        world, taX, inventory, groundItems = tickAll(world, usePos[0], inventory, groundItems)

    elif button == mouse.MIDDLE and not menuOpen:
        usePos = ( (mousePos[0]+scrollX)//8, (mousePos[1]+scrollY)//8 )
        if world[usePos].type != "air":
            selBlockStr = world[usePos].type
            selBlock = getattr(blocks, selBlockStr)

    elif button == mouse.WHEEL_UP:
        selNo += 1
        if selNo > blocksAmt:
            selNo = 0
        selBlock = blocksClass[selNo]
        selBlockStr = blocksStr[selNo]
        while inventory[selBlockStr] == 0 and totalInventory > 0:
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
        while inventory[selBlockStr] == 0 and totalInventory > 0:
            selNo -= 1
            if selNo == -1:
                selNo = blocksAmt
            selBlock = blocksClass[selNo]
            selBlockStr = blocksStr[selNo]








#World gen --
seed = easygui.enterbox("Seed: ", "PixelGame - World Gen")
random.seed(seed)
heightMap = { 0:worldHeight//2 }
for x in range(1, worldWidth):
    heightMap[x] = random.randint(heightMap[x-1]-1, heightMap[x-1]+1)
    if heightMap[x] > (worldHeight//4)*3:
        heightMap[x] = (worldHeight//4)*3
    elif heightMap[x] < worldHeight//4:
        heightMap[x] = worldHeight//4

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
        tick(world, x, y, inventory, groundItems)
#Water --
for x in range(0, worldWidth):
    for y in range(0, worldHeight):
        if y >= worldHeight//2 and getWorldType(world, x, y) == "air" and y <= heightMap[x] and random.choice([True, True, True, False]):
            world[x, y] = blocks.water()
#Sandify --
for x in range(0, worldWidth):
    for y in range(0, worldHeight):
        if getWorldType(world,x+1,y) == "water" or getWorldType(world,x-1,y) == "water" or getWorldType(world,x,y-1) == "water" or getWorldType(world,x+2,y) == "water" or getWorldType(world,x-2,y) == "water" or getWorldType(world,x,y-2) == "water":
            if getWorldType(world,x,y) != "air" and getWorldType(world,x,y) != "water":
                world[x,y] = blocks.sand()
#Add ore --
for x in range(0, worldWidth):
    for y in range(0, worldHeight):
        if getWorldType(world, x, y) == "stone" and random.randint(0,20)==0:
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
#Top hat --
addedTopHat = False
while addedTopHat == False:
    x = random.randint(0,worldWidth-1)
    y = random.randint(0,worldHeight-1)
    if getWorldType(world, x, y) == "air" and isSolid(world, x, y+1):
        world[x, y] = blocks.top_hat()
        addedTopHat = True






print("Loaded!")
pgzrun.go() #Run the game
