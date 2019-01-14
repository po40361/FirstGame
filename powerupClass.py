import pygame

class powerup(object): #new class for powerups
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.addedHealth = 0
        self.addedAmmo = 0
        self.width = 20
        self.ceiling = 10
        self.ground = 435

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))











