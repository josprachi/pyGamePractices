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
    RED=(255,0,0)
    BLUE=(0,0,255)
    BlueXPos=50
    RedXPos=650
    LblYPos=50

    num_chances=3#for now this will come through config file later

    DiceTextures=[]

    def __init__(self ,config=None):

        self.num_chances=int(config.get("Assignment","num_Chances"))
        #print("num chances",self.num_chances)
        self._running = True
        self._gameOver = False
        self._display_surf = None 
        self._rolling_dice=False
        self._startLoop=False      
        self.RedDiceResults=[]
        self.BlueDiceResults=[]
        self.MrRedWepons=[]
        self.MrBlueWepons=[]  
        self.redPoints=0
        self.bluePoints=0 
        
    #initialize the game 
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
        self.timer=0
    

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

        for i in weponsList:#self.MrBlue.wepons:
            self.MrRedWepons.append(self.weponFont.render(str(i)+" "+str(self.MrBlue.wepons[i]), 1, self.WHITE))
            self.MrBlueWepons.append(self.weponFont.render(str(i)+" "+str(self.MrRed.wepons[i]), 1, self.WHITE))   
             
        self.RollButton=self.weponFont.render("Click anywhere to roll Dice", 1, self.YELLOW)
        self.ResultText=self.weponFont.render(" ",1,self.YELLOW)

        self.RedPointText=self.weponFont.render(str(self.MrRed.calculatePoints()),1,self.RED)
        self.BluePointText=self.weponFont.render(str(self.MrBlue.calculatePoints()),1,self.BLUE)

        self.DiceRed = Dice(self.DiceTextures)
        self.DiceBlue= Dice(self.DiceTextures)

        self.DiceBlue.randomize()
        self.DiceRed.randomize()

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

        self.all_sprites_list.update()            
        self.all_Dice_list.update()

        if self.num_chances==0:
            self._gameOver = True
            self._startLoop = False
            self.calculateResults()

        if self._gameOver == False  and self._startLoop == True: 
            if self._rolling_dice==False:

                self.timer+=self.clock.get_time()                
                if self.timer>=1200:
                    self.animateDices()
            else:
                self.timer+=self.clock.get_time()                
                if self.timer>=500:
                    self.stopDiceAnimations()

        for event in pygame.event.get():
            #quit if the quit button was pressed
            if event.type == pygame.QUIT:
                self._running = False
                exit()

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self._startLoop=True
                self.timer=0
                self.RollDices(num_chances=self.num_chances)           
                    
        pass
             

    def stopDiceAnimations(self):
            
            self._rolling_dice=False
            self.DiceRed.stopAnimationAtValue(self.RedDiceResults[self.num_chances-1])
            self.DiceBlue.stopAnimationAtValue(self.BlueDiceResults[self.num_chances-1])

            #time.sleep(1.5)
            self.DoAction(self.MrBlue,self.RedDiceResults[self.num_chances-1])
            self.DoAction(self.MrRed,self.BlueDiceResults[self.num_chances-1])
            
            self.num_chances-=1
            self.timer=0
            

    def animateDices(self):
        
        self.DiceRed.startAnimation()
        self.DiceBlue.startAnimation()
        self._rolling_dice=True
        self.timer=0
    
    def RollDices(self, num_chances=3):
       
        self.RedDiceResults=self.DiceRed.roll(num_chances)
        self.BlueDiceResults=self.DiceBlue.roll(num_chances)

    def DoAction(self, player,weponid):
        #for i in DiceResult:
        player.removeWepon(weponsList[weponid-1])           
    
    def on_render(self):
        self._display_surf.fill((0,0,0))
        self.all_sprites_list.draw(self._display_surf)

        self.renderWepons(self.MrBlue,self.MrBlueWepons,self.BlueXPos)
        self.renderWepons(self.MrRed,self.MrRedWepons,self.RedXPos)


        self.RedPointText=self.weponFont.render(str(self.MrRed.calculatePoints()),1,self.RED)
        self.BluePointText=self.weponFont.render(str(self.MrBlue.calculatePoints()),1,self.BLUE)
        self._display_surf.blit(self.RedPointText,(self.windowWidth/3, self.windowHeight/8))
        self._display_surf.blit(self.BluePointText,(self.windowWidth*2/3, self.windowHeight/8))

        self.all_Dice_list.draw(self._display_surf)  

        if self._gameOver:            
            self._display_surf.blit(self.ResultText,(self.windowWidth/3, self.windowHeight*7/8))
        else:
             self._display_surf.blit(self.RollButton,(self.windowWidth/3, self.windowHeight*7/8))


        pygame.display.update()
        self.clock.tick(60)
        pygame.display.flip()    
    
    def calculateResults(self):
        self.redPoints=self.MrRed.calculatePoints()
        self.bluePoints=self.MrBlue.calculatePoints()
        if self.redPoints!=self.bluePoints:
            if self.redPoints>self.bluePoints:
                self.ResultText=self.weponFont.render(" Red Wins ",1,self.YELLOW)
            else:
                self.ResultText=self.weponFont.render(" Blue Wins ",1,self.YELLOW)  
        else:
            self.ResultText=self.weponFont.render(" Its a Tie ",1,self.YELLOW)          


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
    
    config.read(os.path.abspath(configFile))
   
    mainGame = GameScene(config)
    mainGame.on_execute()
