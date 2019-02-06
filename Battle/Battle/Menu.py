import pygame, random,os,time

class Button(pygame.sprite.Sprite):

    # Constructor. Pass in the color of the block,
    # and its x and y position
    BLACK=(0, 0, 0)
    def __init__(self, texture,points = 0, width = 1, height = 1,id=None):
       # Call the parent class (Sprite) constructor
       super(Button,self).__init__()
       # Create an image of the block, and fill it with a color.
       # This could also be an image loaded from the disk.
       self.image = texture
       pygame.draw.rect(self.image, self.BLACK, [0, 0, width, height])
       self.rect = self.image.get_rect()

       