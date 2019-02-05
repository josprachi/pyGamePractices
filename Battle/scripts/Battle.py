import pygame
from Player import Player

pygame.init()
gameDisplay = pygame.display.set_mode((800,600))
pygame.display.set_caption('Hello World')
clock = pygame.time.Clock()
crashed = False
BLACK = (0,0,0)
WHITE = (255,255,255)
YELLOW = (255, 255, 0)
basicFont = pygame.font.SysFont(None, 48)
MrBlue = Player()
MrBlue.rect.x=200
MrBlue.rect.y=200

all_sprites_list = pygame.sprite.Group()

all_sprites_list.add(MrBlue)
gameDisplay.fill(BLACK)

while not crashed:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True

        print(event)

    
    all_sprites_list.update()    
    all_sprites_list.draw(gameDisplay)
    #pygame.display.flip()
    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()