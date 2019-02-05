from GameResources import weponType as wepons
import pygame


class Player(pygame.sprite.Sprite):
    WHITE = (255, 255, 255)
    YELLOW = (255, 255, 0)
    width = 50
    height = 50
    def __init__(self, points=0,spriteSet=None):

        super(Player,self).__init__()
        
        self.image = pygame.Surface([self.width, self.height])
        
        self.image.fill(self.WHITE)
        self.image.set_colorkey(self.WHITE)
        pygame.draw.rect(self.image, self.YELLOW, [0, 0, self.width, self.height])
        self.rect = self.image.get_rect()

        self.wepons=wepons
        self.points=points

    def calculatePoints(self):
        self.points=0      
        for i in self.wepons:
            self.points+=self.wepons[i]
        print(self,"Current Available Points=>", self.points)

    def removeWepon(self, weponName):
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
    print(p2.getAvailableWepons())
    p2.removeWepon("Dagger")
    p2.calculatePoints()
    print(p2.getAvailableWepons())
    p2.removeWepon("Sward")
    p2.calculatePoints()
    print(p2.getAvailableWepons())
    p2.calculatePoints()
