import pygame, random, time, os, configparser,sys
from Player import Player
from GameResources import imgRes,weponsList
from Dice import Dice

outputFile="../tests/output.txt"
configFile="../tests/config.txt"

class GameScene:
    windowWidth = 800
    windowHeight = 600
    BLACK = (0,0,0)
    WHITE = (255,255,255)
    YELLOW = (255, 255, 0)
    BlueXPos=50
    RedXPos=650
    LblYPos=50

    num_chances=3#for now this will come through config file later

    DiceTextures=[]

    def __init__(self ,config=None):

        self.num_chances=int(config.get("Assignment","num_Chances"))
        print("num chances",self.num_chances)
        self._running = True
        self._gameOver = False
        self._display_surf = None       
        self.RedDiceResults=[]
        self.BlueDiceResults=[]
        self.MrRedWepons=[]
        self.MrBlueWepons=[]   
        
 
    def on_init(self):
        
        self.initPygame()
        self.loadResources()
        self.initScene()
        self._running = True

    def initPygame(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode((self.windowWidth,self.windowHeight), pygame.HWSURFACE) 
        pygame.display.set_caption('Battle MrRed Vs MrBlue')
        self.clock = pygame.time.Clock()

    def loadResources(self):
        self.MrBlue_Texture = pygame.image.load(os.path.abspath(imgRes["mrBlueBody"]))
        self.MrRed_Texture = pygame.image.load(os.path.abspath(imgRes["mrRedBody"]))

        self.DiceTextures.append(pygame.image.load(os.path.abspath(imgRes["dice1Dot"])))
        self.DiceTextures.append(pygame.image.load(os.path.abspath(imgRes["dice2Dot"])))
        self.DiceTextures.append(pygame.image.load(os.path.abspath(imgRes["dice3Dot"])))
        self.DiceTextures.append(pygame.image.load(os.path.abspath(imgRes["dice4Dot"])))
        self.DiceTextures.append(pygame.image.load(os.path.abspath(imgRes["dice5Dot"])))
        self.DiceTextures.append(pygame.image.load(os.path.abspath(imgRes["dice6Dot"])))

    def initScene(self):

        self.MrRed = Player(self.MrRed_Texture,id="MrRed")
        self.MrBlue = Player(self.MrBlue_Texture,id="MrBlue")
         

        self.all_sprites_list = pygame.sprite.Group()
        self.all_Dice_list = pygame.sprite.Group() 
        self.weponFont = pygame.font.SysFont(None, 32) 

        for i in self.MrBlue.wepons:
            self.MrRedWepons.append(self.weponFont.render(str(i), 1, self.WHITE))
            self.MrBlueWepons.append(self.weponFont.render(str(i), 1, self.WHITE))   
             
        self.RollButton=self.weponFont.render("Click anywhere to roll Dice", 1, self.YELLOW)
        self.ResultText=self.weponFont.render(" ",1,self.YELLOW)

        self.DiceRed = Dice(self.DiceTextures)
        self.DiceBlue= Dice(self.DiceTextures)

        self.setSpritePosition(self.MrBlue,[self.windowWidth/2-(self.MrBlue.rect.width*1.25),self.windowHeight/4])
        self.setSpritePosition(self.MrRed,[self.windowWidth/2,self.windowHeight/4])
        self.setSpritePosition(self.DiceBlue,[self.windowWidth/2-(self.MrBlue.rect.width*1.25),self.windowHeight/2])
        self.setSpritePosition(self.DiceRed,[self.windowWidth/2,self.windowHeight/2])
       
        self.all_sprites_list.add(self.MrBlue)
        self.all_sprites_list.add(self.MrRed)
        self.all_Dice_list.add(self.DiceRed)
        self.all_Dice_list.add(self.DiceBlue)

    def setSpritePosition(self, _sprite, pos=[0,0]):
        _sprite.rect.x=pos[0]
        _sprite.rect.y=pos[1]


    def on_loop(self): 
        for event in pygame.event.get():
            #quit if the quit button was pressed
            if event.type == pygame.QUIT:
                self._running = False
                exit()

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if self._gameOver == False:
                    self.RollDices(self.num_chances)
                    self.DoAction(self.MrBlue,self.RedDiceResults)
                    self.DoAction(self.MrRed,self.BlueDiceResults)
                    if self.num_chances==0:
                        self._gameOver = True              

        self.all_sprites_list.update()
            
        self.all_Dice_list.update()
        pass
 
    def RollDices(self, num_chances=3):
        
        self.RedDiceResults=self.DiceRed.roll(num_chances)
        self.BlueDiceResults=self.DiceBlue.roll(num_chances)

    def DoAction(self, player,DiceResult):
        for i in DiceResult:
            player.removeWepon(weponsList[i-1])           
    
    #def WriteOutput(self,outputFile):

    def on_render(self):
        self._display_surf.fill((0,0,0))
        self.all_sprites_list.draw(self._display_surf)

        self.renderWepons(self.MrBlue,self.MrBlueWepons,self.BlueXPos)
        self.renderWepons(self.MrRed,self.MrRedWepons,self.RedXPos)
        self.all_Dice_list.draw(self._display_surf)  

        if self._gameOver:            
            self._display_surf.blit(self.ResultText,(self.windowWidth/3, self.windowHeight*7/8))
        else:
             self._display_surf.blit(self.RollButton,(self.windowWidth/3, self.windowHeight*7/8))


        pygame.display.update()
        self.clock.tick(60)
        pygame.display.flip()    
    
    def renderWepons(self,player,weponlist,xPos):
        counter=0
        for i in weponlist:
            if player.wepons[weponsList[counter]]!=0: 
                self._display_surf.blit(weponlist[counter],(xPos, self.LblYPos+(35*counter)))
            counter+=1


    def on_cleanup(self):
        pygame.quit()
 
      
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
 
        while( self._running ):
            pygame.event.pump()
            keys = pygame.key.get_pressed() 
            if (keys[pygame.K_ESCAPE]):
                self._running = False
 
            self.on_loop()
            self.on_render()
            self.clock.tick(60)
            #time.sleep (50.0 / 1000.0)
        self.on_cleanup()
    



if __name__ == "__main__" :
    
    config = configparser.ConfigParser()
    #print(os.path.abspath(configFile))
    config.read(os.path.abspath(configFile))
    print(config.get("Assignment","num_Chances"))
    mainGame = GameScene(config)
    mainGame.on_execute()
