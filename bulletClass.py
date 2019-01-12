import pygame

class projectile(object): #new class for projectiles
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing #which direction the bullet is facing. -1 is left and +1 is going right cuz x-cordinates
        self.vel = 8 * facing

    def draw(self, win): #drawing bullet
        pygame.draw.circle( win, self.color, (self.x, self.y), self.radius)
