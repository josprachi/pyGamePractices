import pygame, random, time, os, configparser,sys
from Player import Player
from GameResources import imgRes,weponsList
from Dice import Dice
from Menu import Button
outputFile="./output/output.txt"
configFile="../config.txt"

class GameScene:
    windowWidth = 0
    windowHeight = 0
    BLACK = (0,0,0)
    WHITE = (255,255,255)
    YELLOW = (255, 255, 0)
    RED=(255,0,0)
    BLUE=(0,0,255)
    BlueXPos=50
    RedXPos=650
    LblYPos=50
    inputString=""
    num_chances=1#for now this will come through config file later

    DiceTextures=[]

    def __init__(self ,config=None,mode=None):
        self.config=config 
        self.num_chances=int(config.get("Assignment","num_Chances"))

        if mode=="auto":
            self.mode=mode             
        else:
            self.mode=str(config.get("Assignment","mode")) 
           
        self.windowHeight=int(config.get("Assignment","windowHeight"))
        self.windowWidth=int(config.get("Assignment","windowWidth"))


        self._running = True
        self._gameOver = False
        self._display_surf = None 
        self._rolling_dice = False
        self._startLoop = False
        self._outputSaved= False
        if self.mode!="auto":             
            self._showInput = True
        else:           
            self._showInput= False         
        self.RedDiceResults = []
        self.BlueDiceResults = []
        self.MrRedWepons = []
        self.MrBlueWepons = []  
        self.redPoints = 0
        self.bluePoints = 0        
        
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

        self.saveBtnTexture=pygame.image.load(os.path.abspath(imgRes["savebtn"]))

    def initScene(self):
        #Players
        self.MrRed = Player(self.MrRed_Texture,id="MrRed")
        self.MrBlue = Player(self.MrBlue_Texture,id="MrBlue")

        #Buttons
        self.SaveBtn=Button(self.saveBtnTexture)
        

        self.all_sprites_list = pygame.sprite.Group()

        self.all_Dice_list = pygame.sprite.Group() 

        #fonts and texts
        self.weponFont = pygame.font.SysFont(None, 32)
        self.smallFont = pygame.font.SysFont(None, 20)

        for i in weponsList:#self.MrBlue.wepons:
            self.MrRedWepons.append(self.weponFont.render(str(i)+" "+str(self.MrBlue.wepons[i]), 1, self.WHITE))
            self.MrBlueWepons.append(self.weponFont.render(str(i)+" "+str(self.MrRed.wepons[i]), 1, self.WHITE))   
             
        self.RollButton=self.weponFont.render("Click anywhere to roll Dice", 1, self.YELLOW)
        self.ResultText=self.weponFont.render(" ",1,self.YELLOW)

        self.Instruction=self.smallFont.render("once result is displayed, click on the save button to save the output and to exit the game anytime press \"Esc\"   ",1,self.YELLOW)

        self.RedPointText=self.weponFont.render(str(self.MrRed.calculatePoints()),1,self.RED)
        self.BluePointText=self.weponFont.render(str(self.MrBlue.calculatePoints()),1,self.BLUE)

        self.NumChancesText=self.weponFont.render(str(self.num_chances), 1, self.YELLOW)

        self.DiceRed = Dice(self.DiceTextures)
        self.DiceBlue= Dice(self.DiceTextures)

        self.DiceBlue.randomize()
        self.DiceRed.randomize()

        self.setSpritePosition(self.MrBlue,[self.windowWidth/2-(self.MrBlue.rect.width*1.25),self.windowHeight/4])
        self.setSpritePosition(self.MrRed,[self.windowWidth/2,self.windowHeight/4])
        self.setSpritePosition(self.DiceBlue,[self.windowWidth/2-(self.MrBlue.rect.width*1.25),self.windowHeight/2])
        self.setSpritePosition(self.DiceRed,[self.windowWidth/2,self.windowHeight/2])

        self.setSpritePosition(self.SaveBtn,[self.windowWidth/4-(self.SaveBtn.rect.width*1.25),self.windowHeight*3/4])
       
        self.all_sprites_list.add(self.MrBlue)
        self.all_sprites_list.add(self.MrRed)
        self.all_sprites_list.add(self.SaveBtn)
        self.all_Dice_list.add(self.DiceRed)
        self.all_Dice_list.add(self.DiceBlue)

    def setSpritePosition(self, _sprite, pos=[0,0]):
        _sprite.rect.x=pos[0]
        _sprite.rect.y=pos[1]


    def on_loop(self):

        self.all_sprites_list.update()            
        self.all_Dice_list.update()

        self.redPoints=self.MrRed.calculatePoints()
        self.bluePoints=self.MrBlue.calculatePoints()

        if self.num_chances==0 or self.detectAnybodyLostAllWepons():
            self._gameOver = True
            self._startLoop = False
            self.calculateResults()

        if self._gameOver == False and self._showInput == True: 
            self.num_chances = self.askQuestion(self._display_surf, "How many times do you want to roll the dice?",self.YELLOW,self.BLUE)
            if(self.num_chances==0):
                self.num_chances=int(self.config.get("Assignment","num_Chances"))
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
                if self._gameOver:
                    x,y=event.pos                    
                    if self.SaveBtn.rect.collidepoint(x,y):
                        self.writeResultToFile()
                else:
                    self._startLoop=True
                    self.outputToWrite="No of Chances= "+str(self.num_chances)
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

            self.redPoints=self.MrRed.calculatePoints()
            self.bluePoints=self.MrBlue.calculatePoints()
            #self.outputToWrite+= "\n chance=> "+ str(self.num_chances)+"  Dice Blue: "+str(self.BlueDiceResults[self.num_chances-1])+"  Dice Red: "+str(self.RedDiceResults[self.num_chances-1])+" Mr Blue Scored: "+ str(self.bluePoints)+" and Mr Red Scored: "+str(self.redPoints)
            self.generateOutput()
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

        self.RedPointText=self.weponFont.render(str(self.redPoints),1,self.RED)
        self.BluePointText=self.weponFont.render(str(self.bluePoints),1,self.BLUE)

        self._display_surf.blit(self.RedPointText,(self.windowWidth*2/3, self.windowHeight/8))
        self._display_surf.blit(self.BluePointText,(self.windowWidth/3, self.windowHeight/8))

        self.NumChancesText=self.weponFont.render("Remainig rolls: "+str(self.num_chances),1,self.YELLOW)
        if self._rolling_dice == True:
            self.RollButton=self.weponFont.render("Please wait untill game is over ",1,self.YELLOW)
            
        self._display_surf.blit(self.NumChancesText,(self.windowWidth/4, self.windowHeight*4/5))

        self._display_surf.blit(self.Instruction,(10, self.windowHeight*13/14))

        self.all_Dice_list.draw(self._display_surf)  

        if self._gameOver:            
            self._display_surf.blit(self.ResultText,(self.windowWidth/4, self.windowHeight*7/8))
        else:
             self._display_surf.blit(self.RollButton,(self.windowWidth/3, self.windowHeight*7/8))


        pygame.display.update()
        self.clock.tick(60)
        pygame.display.flip() 


    def detectAnybodyLostAllWepons(self):        
        if self.bluePoints<2 or self.redPoints<2:
            return True
        else:
            return False    

    def calculateResults(self):
        
        if self.redPoints!=self.bluePoints:
            if self.redPoints>self.bluePoints:
                self.ResultText=self.weponFont.render("Mr Red Wins ",1,self.YELLOW)
                return 1
            else:
                self.ResultText=self.weponFont.render("Mr Blue Wins ",1,self.YELLOW)
                return 0  
        else:
            self.ResultText=self.weponFont.render(" Its a Tie ",1,self.YELLOW)
            return None          


    def renderInput(self):
        print("this is to take input from user")

    def generateOutput(self):
        i= self.calculateResults()
        if self._gameOver:
            self.outputToWrite+="\n overall"
        else:        
            self.outputToWrite+= "\n chance=> "+ str(self.num_chances)
            self.outputToWrite+="  Dice Blue: "+str(self.BlueDiceResults[self.num_chances-1])+"  Dice Red: "+str(self.RedDiceResults[self.num_chances-1])
            self.outputToWrite+=" Mr Blue Scored: "+ str(self.bluePoints)+" and Mr Red Scored: "+str(self.redPoints)
        
        if i == 1:
            self.outputToWrite+=" winner is Mr Red"
        elif i==0:
            self.outputToWrite+=" winner is Mr Blue "
        else:
            self.outputToWrite+=" its a tie " 
       

       
    def writeResultToFile(self):
        if self._outputSaved == False:
            self.generateOutput()
            self._outputSaved=True

        #print("This prints result of the game into output file")
        file_path=os.path.abspath(outputFile)
        if os.path.exists(file_path):
            f = open(file_path, "w")
            f.write(self.outputToWrite)
        else:
            f = open(file_path, "w")
            f.write(self.outputToWrite)    

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
        self.on_cleanup()

    def popup(self,screen, message, width, height,x , y, bgcolor, textColor):
        #Display a popup box in the middle of the screen
        #This popup will only disappear when the user presses the Return key
 
        fontobject = pygame.font.Font(None,18)
        pygame.draw.rect(screen, bgcolor,(x - width/2 +2,y - height/2 +2,300,36), 0)
        pygame.draw.rect(screen, self.WHITE,(x - width/2,y - height/2,304,40), 1)
        if len(message) != 0:
            screen.blit(fontobject.render(message, 1, textColor),(x - width/2 + 10, y - height/2 + 14))
            pygame.display.flip()  

    def askQuestion(self,screen, question,bgColor, textColor, width=300, height=40, x=-1, y=-1):
        #width, height, x, y, bgColor and textColor are optional arguments
        #When x and y are omitted, use the centre of the screen
        if x==-1:
            x = screen.get_width() / 2
        if y==-1:
            y = screen.get_height() / 2
 
        pygame.font.init()
        current_string = ""
        self.popup(self._display_surf, question + ": " + "".join(current_string), width, height, x, y, bgColor, textColor)
        
        while self._showInput:
            inkey = self.getKey()
            if inkey == pygame.K_BACKSPACE:
                current_string = current_string[0:-1]
            elif inkey == pygame.K_RETURN:
                self._showInput=False                           
            elif inkey <= 255:
                if (inkey>=48 and inkey<=57):
                    current_string += chr(inkey)
            self.popup(screen, question + ": " + "".join(current_string), width, height, x, y, bgColor, textColor)                      
 
        return int(current_string)

    def getKey(self):
        while 1:
            event = pygame.event.poll()
            if event.type == pygame.KEYDOWN:
                return event.key
            else:
                pass
                     





if __name__ == "__main__" :
    
    config = configparser.ConfigParser()    
    config.read(os.path.abspath(configFile))   
    mainGame = GameScene(config)
    mainGame.on_execute()
