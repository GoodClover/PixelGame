import pygame

print("\n"*100)
print("toSet by Oliver Simmons")
dire = input("Block: ")

full = pygame.image.load(dire+"\\full.png")
sections = {}

#  1
# 8█2
#  4

#0 -> 15

def newOne(i,x,y):
    newSurf = pygame.Surface((8,8), pygame.SRCALPHA, 32)
    #newSurf.set_colorkey((0,0,0))
    newSurf.blit(full, (0,0), (x*8,y*8,8,8))
    sections[i] = newSurf
    print(str(i)+" done!")

newOne(0, 4, 4)
newOne(1, 4, 2)
newOne(2, 0, 4)
newOne(3, 0, 2)
newOne(4, 4, 0)
newOne(5, 4, 1)
newOne(6, 0, 0)
newOne(7, 0, 1)
newOne(8, 2, 4)
newOne(9, 2, 2)
newOne(10, 1, 4)
newOne(11, 1, 2)
newOne(12, 2, 0)
newOne(13, 2, 1)
newOne(14, 1, 0)
newOne(15, 1, 1)


for i in range(0,16):
    pygame.image.save(sections[i], dire+"\\"+str(i)+".png")
