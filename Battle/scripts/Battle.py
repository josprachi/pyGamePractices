import pygame, random, time, os
from Player import Player
from GameResources import imgRes
from Dice import Dice


BLACK = (0,0,0)
WHITE = (255,255,255)
YELLOW = (255, 255, 0)

num_chances=3#for now this will come through config file later
#MrBlue_Texture=pygame.Surface([1,1]) 
#MrRed_Texture=pygame.Surface([1,1]) 
DiceTextures=[]
#gameDisplay = pygame.Surface([800,600])
#def initGame():
pygame.init()
gameDisplay = pygame.display.set_mode((800,600))
pygame.display.set_caption('Hello World')


#def runGame():
    #pygame.init()

    #loadResources()

MrBlue_Texture = pygame.image.load(os.path.abspath(imgRes["mrBlueBody"]))
MrRed_Texture = pygame.image.load(os.path.abspath(imgRes["mrRedBody"]))

DiceTextures.append(pygame.image.load(os.path.abspath(imgRes["dice1Dot"])))
DiceTextures.append(pygame.image.load(os.path.abspath(imgRes["dice2Dot"])))
DiceTextures.append(pygame.image.load(os.path.abspath(imgRes["dice3Dot"])))
DiceTextures.append(pygame.image.load(os.path.abspath(imgRes["dice4Dot"])))
DiceTextures.append(pygame.image.load(os.path.abspath(imgRes["dice5Dot"])))
DiceTextures.append(pygame.image.load(os.path.abspath(imgRes["dice6Dot"])))

RedDiceResults=[]
BlueDiceResults=[]    

clock = pygame.time.Clock()
crashed = False
#print(os.path.abspath("../res"))


basicFont = pygame.font.SysFont(None, 48)



MrBlue = Player(MrBlue_Texture)
MrBlue.rect.x=100
MrBlue.rect.y=100



MrRed = Player(MrRed_Texture)
MrRed.rect.x=300
MrRed.rect.y=100

DiceRed = Dice(textures=DiceTextures)
DiceRed.rect.x=250
DiceRed.rect.y=400

DiceBlue= Dice(textures=DiceTextures)
DiceBlue.rect.x=450
DiceBlue.rect.y=400


all_sprites_list = pygame.sprite.Group()
all_Dice_list = pygame.sprite.Group()
all_sprites_list.add(MrBlue)
all_sprites_list.add(MrRed)
all_Dice_list.add(DiceRed)
all_Dice_list.add(DiceBlue)
gameDisplay.fill(BLACK)


while not crashed:

    for event in pygame.event.get():
        
        if event.type == pygame.KEYUP:
            print("Here")
            RedDiceResults = DiceRed.roll(1)
            BlueDiceResults = DiceBlue.roll(1)    
            for i in RedDiceResults:
                if RedDiceResults[i]>BlueDiceResults[i]:
                    print("Red Wins")
                else:
                    print("Blue Wins")

        if event.type == pygame.QUIT:
            crashed = True


        #print(event)

    #DiceRed.animate_roll()
    
    all_sprites_list.update()       
    all_Dice_list.update()
    gameDisplay.fill(BLACK)
    all_sprites_list.draw(gameDisplay)
    all_Dice_list.draw(gameDisplay)
    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()

""" 
if __name__ == "__main__":
    initGame()
    loadResources()
    runGame()    
     """