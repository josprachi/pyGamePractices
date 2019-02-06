from GameResources import weponType as wepons
import pygame


class Player(pygame.sprite.Sprite):
    WHITE = (255, 255, 255)
    YELLOW = (255, 255, 0)
    BLACK=(0, 0, 0)
    
    def __init__(self, texture,points = 0, width = 1, height = 1,id=None):

        super(Player,self).__init__()
        
        #self.image = pygame.Surface([width,height])
        
        self.image=texture
        #self.image.set_colorkey(self.WHITE)
        pygame.draw.rect(self.image, self.BLACK, [0, 0, width, height])
        self.rect = self.image.get_rect()
        
        self.wepons=wepons.copy()
        self.points=points
        self.id=id

    def calculatePoints(self):
        self.points=0      
        for i in self.wepons:
            self.points+=self.wepons[i]
        return self.points    
        #print(self,"Current Available Points=>", self.points)

    def removeWepon(self, weponName):
        #print(weponName,"this is wepon to be removed")
        self.wepons[weponName]=0#just to make sure the wepon is removed from displayd list and does not have any value

    def getAvailableWepons(self):
        avilWep=[]
        for i in self.wepons:
            if self.wepons[i]!=0:                
                avilWep.append(i)
        return avilWep        
             
if __name__ == "__main__":
    p1=Player()
    p2=Player()
    p1.calculatePoints()
    p2.calculatePoints()
    #print(p2.getAvailableWepons())
    p2.removeWepon("Dagger")
    p2.calculatePoints()
    #print(p2.getAvailableWepons())
    p2.removeWepon("Sward")
    p2.calculatePoints()
    #print(p2.getAvailableWepons())
    p2.calculatePoints()
