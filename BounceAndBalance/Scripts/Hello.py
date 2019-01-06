import pygame
pygame.init()
gameDisplay = pygame.display.set_mode((800,600))
pygame.display.set_caption('Hello World')
clock = pygame.time.Clock()
crashed = False
BLACK = (0,0,0)
WHITE = (255,255,255)
basicFont = pygame.font.SysFont(None, 48)
text = basicFont.render('HELLO WORLD', True, BLACK)
textRect = text.get_rect()
textRect.centerx = gameDisplay.get_rect().centerx
textRect.centery = gameDisplay.get_rect().centery
gameDisplay.fill(WHITE)
gameDisplay.blit(text,textRect)

while not crashed:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True

        print(event)

    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()