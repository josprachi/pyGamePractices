import pygame, random,os
#from GameResources import imgRes

class Dice(pygame.sprite.Sprite):
    NUM_FACES = 6
    index=0
    BLACK=(0, 0, 0)
    def __init__(self, textures=None, width = 1, height = 1, index = 0):
        super(Dice,self).__init__()
        self.index=index
        self.images=textures
        self.image=self.images[self.index]
        pygame.draw.rect(self.image, self.BLACK, [0, 0, width, height])
        self.rect = self.image.get_rect()

    def roll(self, iterations=1):
        rollValues=[]
        for i in range(iterations):
            rollValues.append(random.randint(1,self.NUM_FACES))
        return rollValues

    def animate_roll(self):
        self.index+=1
        if(self.index>=5):
            self.index=0
        self.image=self.images[self.index]

    def showValue(self,valueIndex):
        self.index=valueIndex
        self.image=self.images[valueIndex]

        
    #if __name__ == "__main__":
    #D1=Dice(pygame.image.load(os.path.abspath(imgRes["dice6Dot"])))    
    #print(D1.roll(6))