import pygame

walkRight = [pygame.image.load('sprites/R1.png'), pygame.image.load('sprites/R2.png'), pygame.image.load('sprites/R3.png'), pygame.image.load('sprites/R4.png'), pygame.image.load('sprites/R5.png'), pygame.image.load('sprites/R6.png'), pygame.image.load('sprites/R7.png'), pygame.image.load('sprites/R8.png'), pygame.image.load('sprites/R9.png')]

walkLeft = [pygame.image.load('sprites/L1.png'), pygame.image.load('sprites/L2.png'), pygame.image.load('sprites/L3.png'), pygame.image.load('sprites/L4.png'), pygame.image.load('sprites/L5.png'), pygame.image.load('sprites/L6.png'), pygame.image.load('sprites/L7.png'), pygame.image.load('sprites/L8.png'), pygame.image.load('sprites/L9.png')]

class player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.consecJumps = 0
        self.isJump = False
        self.jumpCount = 10
        self.left = False #check if moving left
        self.right = False #check if moving right
        self.walkCount = 0
        self.standing = True
        self.hitbox = (self.x + 20, self.y + 13, 26, 50) #defines hitbox as a class attribute
        self.health = 9
        self.ammo = 10


    def draw(self, win):
        if self.walkCount + 1 >= 54 : #sprite file only has 9 images and we're doing 3 frames per movement. so 27 or else it will have an index error
            self.walkCount = 0


        if not(self.standing):
            if self.left:
                win.blit(walkLeft[self.walkCount // 6], (self.x, self.y)) #uses above list 'walkleft', which is a list of images. prints the image at index walkcount//3
                self.walkCount += 1

            elif self.right:
                win.blit(walkRight[self.walkCount // 6], (self.x, self.y)) #same as above but for walking right
                self.walkCount += 1

        else:
            if self.right:          #makes it so whatever direction player was facing when moving will be the same direction they're facing when they stop
                win.blit(walkRight[0], (self.x, self.y))
            else:
                win.blit(walkLeft[0], (self.x, self.y))

        self.hitbox = (self.x + 20, self.y + 13, 26, 50) #updates hitbox coords

        if self.health > 0:
            pygame.draw.rect(win, (169,169,169), (self.hitbox[0]-13, self.hitbox[1] - 20, 50, 10))
            pygame.draw.rect(win, (255, 0, 0), (self.hitbox[0]-13, self.hitbox[1] - 20, 50 - ((50/9) * (9 - self.health)), 10))
        else:
            pygame.draw.rect(win, (169,169,169), (self.hitbox[0]-13, self.hitbox[1] - 20, 47 , 10))

        #pygame.draw.rect(win, (0, 0, 0), self.hitbox, 2) #draws hitbox

    def hit(self): #what happens when player is hit

        if self.health > 0:
            self.health = self.health - 2
        else:
            self.health = 0
