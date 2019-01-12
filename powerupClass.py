import pygame

class powerup(object): #new class for powerups
    def __init__(self, x, color):
        self.x = x
        self.y = 435
        self.color = color
        self.addedHealth = 0
        self.addedAmmo = 0
        self.width = 20

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))








