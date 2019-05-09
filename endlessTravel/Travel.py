import pygame
import time
from pygame.locals import *

winWidth=600
winHeight=480
color_CYAN=(0,255,255)
color_BLACK=(0,0,0)
bkgs=[]
bkg_texture_str="gameBkg.png"
shipAnimFrames_str=["ripple0.png","ripple1.png","ripple2.png","ripple3.png","ripple4.png"]
all_sprites_list = pygame.sprite.Group()
clock = pygame.time.Clock()

class GameScene:
    def __init__(self ,config=None,mode=None):
        print("init")
    def on_init(self):
        print("on init")
    def initPygame(self):
        print("initPygame")
    def loadResources(self):
        print("loadResources")
    def initScene(self):
        print("inirScene")
    def update(self):
        print("update")
    def render(self):
        print("render")
    def reset():
        print("reset")

class Background(pygame.sprite.Sprite):
    x = 0
    y = 0
    maxY=0
    def __init__(self, texture, bushes, x = 0, y = 0, width = 1, height = 1):
        super(Background,self).__init__()		
        self.image = texture
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.bushes = bushes
        self.rect = self.image.get_rect()
    def scroll(self,speed):
        self.y += speed
        if self.y > winHeight:
            self.y =- winHeight
    
    def update(self):
        self.scroll(5)

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))
        i = 0
        while i<len(self.bushes):
            if i%2==0:
                self.image.blit(self.bushes[i],(winWidth*0.01*i,50*i))
            else:
                self.image.blit(self.bushes[i],(winWidth*0.83+(i*10),50*i))
            i+=1

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, texture, x = 0, y = 0):
        super(Obstacle,self).__init__()
        self.image = texture
        self.x = x
        self.y = y

    def scroll(self,speed):
        self.y += speed
        if self.y > winHeight:
            self.y =- winHeight
    
    def update(self):
        self.scroll(0)    

    def draw(self, surface):
        surface.blit(self.image,(self.x, self.y))	

class Ship(pygame.sprite.Sprite):
    index = 0
    def __init__(self, texture, animFrames, x = 0, y = 0, width = 1, height = 1):
        super(Ship, self).__init__()
        self.image = texture
        self.animFrames = animFrames
        self.currentFrame = self.animFrames[0]
        #self.image.set_colorkey(self.WHITE)
        self.x = x
        self.y = y
        self.rect = self.image.get_rect()
        self.width = self.rect.width
        self.height = self.rect.height

    def update(self):
        if self.isAnimating:
            self.animate()

    def draw(self, surface):
        surface.blit(self.currentFrame, (self.x - self.width, self.y - self.height * 0.2))
        #pygame.display.flip()
        surface.blit(self.image,(self.x, self.y))

    def startAnimation(self):
        self.isAnimating = True

    def animate(self):
        self.index += 1
        if(self.index >= len(self.animFrames)):
            self.index = 0
        self.currentFrame = self.animFrames[self.index]
        time.sleep(0.01)

    def stopAnimation(self):
        self.isAnimating=False
        print("stop animation")		


if __name__ == "__main__":
    pygame.init()
    caption = "Endless Travel"
    pygame.display.set_caption(caption)
    ship = pygame.image.load("ship.png")
    pygame.display.set_icon(ship)
    Game_Window = pygame.display.set_mode((winWidth,winHeight))
    Game_Window.fill(color_CYAN)
    bush = pygame.transform.scale((pygame.image.load("bush.png")),(50,50))
    bushes = []
    shipAnimFrames = []
    padtex= pygame.image.load("Pad_04_1.png")
    padrect=padtex.get_rect()
    pad= pygame.transform.scale(padtex,(int(padrect.width*0.15),int(padrect.height*0.25)))

    i = 0
    while i < 5:
        bushes.append(bush.copy())
        i += 1
    
    i = 0
    while i < len(shipAnimFrames_str):
        shipAnimFrames.append((pygame.image.load(shipAnimFrames_str[i])))
        i += 1

    bkg_texture=pygame.transform.scale((pygame.image.load(bkg_texture_str)), (winWidth,winHeight))	
    BkgSprite1 = Background(bkg_texture, bushes, 0, winHeight * (-1))
    BkgSprite2 = Background(bkg_texture, bushes, 0, 0)
    BkgSprite3 = Background(bkg_texture, bushes, 0, winHeight)
    ShipSprite = Ship(ship,shipAnimFrames, winWidth*0.45, winHeight*0.75)
    ShipSprite.startAnimation()
    
    obstacleSprite = Obstacle(pad, winWidth*0.35, winHeight*0.5) 

    all_sprites_list.add(BkgSprite1)
    all_sprites_list.add(BkgSprite2)
    all_sprites_list.add(BkgSprite3)
    all_sprites_list.add(ShipSprite)
    all_sprites_list.add(obstacleSprite)
    while True:
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                exit()
        all_sprites_list.update()
        Game_Window.fill(color_CYAN)
        #all_sprites_list.draw(Game_Window)
        BkgSprite1.draw(Game_Window)
        BkgSprite2.draw(Game_Window)
        BkgSprite3.draw(Game_Window)
        ShipSprite.draw(Game_Window)
        obstacleSprite.draw(Game_Window)
        
        #Game_Window.blit(ship,(winWidth*0.45,winHeight*0.25))
        clock.tick(60)
        pygame.display.flip()        