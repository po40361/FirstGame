import pygame

global score
score = 0

class enemy(object): #new class for enemies
    walkRight = [pygame.image.load('sprites/R1E.png'), pygame.image.load('sprites/R2E.png'), pygame.image.load('sprites/R3E.png'), pygame.image.load('sprites/R4E.png'), pygame.image.load('sprites/R5E.png'), pygame.image.load('sprites/R6E.png'), pygame.image.load('sprites/R7E.png'),pygame.image.load('sprites/R8E.png')]
    walkLeft = [pygame.image.load('sprites/L1E.png'), pygame.image.load('sprites/L2E.png'), pygame.image.load('sprites/L3E.png'), pygame.image.load('sprites/L4E.png'), pygame.image.load('sprites/L5E.png'), pygame.image.load('sprites/L6E.png'), pygame.image.load('sprites/L7E.png'), pygame.image.load('sprites/L8E.png')]

    standRight = [pygame.image.load('sprites/R6E.png')]
    standLeft = [pygame.image.load('sprites/L1E.png')]

    hitLeft = [pygame.image.load('sprites/L9E.png'), pygame.image.load('sprites/L10E.png'), pygame.image.load('sprites/L11E.png')]
    hitRight = [pygame.image.load('sprites/R9E.png'), pygame.image.load('sprites/R10E.png'), pygame.image.load('sprites/R11E.png')]





    def __init__(self, x, y, width, height, targetX, targetY):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        #self.end = end
        #self.path = [self.x, self.end] #where the enemy starts walking and where it stops
        self.walkCount = 0
        self.vel = 3
        self.hitbox = (self.x + 15, self.y, 26, 60) #the hitbox's attributes
        self.hitcount = 0  #same as walkcount but for the hitting sprite
        self.health = 9
        self.visible = True #is the enemy visible
        self.targetX = targetX #x coord of enemy's target
        self.targetY = targetY # y coord
        self.attack = False
        self.hitting = True




    def draw(self, win):
        self.move()


        if self.visible:
            if self.walkCount + 1 >= 24:
                self.walkCount = 0
            if self.hitcount + 1 >= 9:
                self.hitcount = 0

            if not self.hitting:
                if self.vel > 0:
                    #if self.attack == True:
                        #win.blit(self.hitRight[self.walkCount // 3], (self.x, self.y))

                    #else:
                    win.blit(self.walkRight[self.walkCount // 3], (self.x, self.y))
                    self.walkCount += 1 #changing the index for images

                    self.hitbox = (self.x + 15, self.y , 26, 58) #updates hitbox coords
                    #pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2) #draws hitbox

                elif self.vel < 0:
                    #if self.attack == True:
                        #win.blit(self.hitLeft[self.walkCount // 3], (self.x, self.y))

                    #else:
                    win.blit(self.walkLeft[self.walkCount // 3], (self.x, self.y))
                    self.walkCount += 1

                    self.hitbox = (self.x + 28, self.y , 26, 58) #updates hitbox coords
                    #pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2) #draws hitbox
            else:
                if self.vel > 0:
                    #win.blit(self.standRight[0], (self.x, self.y))
                    win.blit(self.hitRight[self.hitcount // 3], (self.x, self.y))
                    self.hitcount += 1
                else:
                    win.blit(self.hitLeft[self.hitcount // 3], (self.x, self.y))
                    self.hitcount += 1



            pygame.draw.rect(win, (169,169,169), (self.hitbox[0]-10, self.hitbox[1] - 20, 50 , 10))
            pygame.draw.rect(win, (255, 0, 0), (self.hitbox[0]-10, self.hitbox[1] - 20, 50 - ((50/9) * (9 - self.health)), 10))#red part of healthbar
            #pygame.draw.rect(win, (0, 255, 0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))#green part of healthbar


    def hit(self): #what happens when enemy is hit

        if self.health > 0:
            self.health = self.health - 1
        else:
            self.visible = False

        global score
        score += 1


    def move(self):

        #making mobs move on a set path
        '''
        if self.vel > 0:
            if self.x + self.vel < self.path[1]: #checking if enemy is approaching end of its path
                self.x += self.vel #moving enemy to the right

            else:
                self.vel = self.vel * -1 #changes direction
                self.walkCount = 0 #resets enemy walk animation

        else: #same as above but for opposite direction
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
        '''

        #self.attack = False

        '''if not \
                ((self.hitbox[0] - self.targetX) <= 1 or (self.hitbox[0] - self.targetX) >=-1) \
                and ((self.hitbox[1] - self.targetY) <= 10 or (self.hitbox[1] - self.targetY) >= -10):
                #checking if player is close enough for enemy to attack'''

        if (self.targetX - self.x) > 32: #checking if enemy is on the right or left of the player
                                         # and if they're far away enough to walk towards them
            self.hitting = False

            if self.vel > 0:
                self.x += self.vel #moving enemy to the right
            else:
                self.vel = self.vel * (-1)
                self.walkCount = 0 #resets enemy walk animation

        elif (self.x - self.targetX ) > 20:
            self.hitting = False

            if self.vel < 0:
                self.x += self.vel
            else:
                self.vel = self.vel * (-1)
                self.walkCount = 0

        elif ((self.targetX - self.x) < 32 or (self.x - self.targetX) < 20):
            #if player is within a certain nbr of pixels to the enemy's hitbox, enemy stops walking and attacks
            self.hitting = True
            self.walkCount = 0
