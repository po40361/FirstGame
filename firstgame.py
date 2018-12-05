import pygame
pygame.init()

ScreenWidth = 500
ScreenHeight = 480

win = pygame.display.set_mode((ScreenWidth, ScreenHeight))
	#creates a surface

pygame.display.set_caption("First Game")

#different lists for sprites and animations
walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'), pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'), pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]

walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'), pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'), pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]

bg = pygame.image.load('bg.jpg')

char = pygame.image.load('standing.png')

clock = pygame.time.Clock() #allows for toggling fps

class player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.isJump = False
        self.jumpCount = 10
        self.left = False #check if moving left
        self.right = False #check if moving right
        self.walkCount = 0
        self.standing = True
        self.hitbox = (self.x + 20, self.y + 13, 26, 50) #defines hitbox as a class attribute

    def draw(self, win):
        if self.walkCount + 1 >= 27: #sprite file only has 9 images and we're doing 3 frames per movement. so 27 or else it will have an index error
            self.walkCount = 0


        if not(self.standing):
            if man.left:
                win.blit(walkLeft[self.walkCount // 3], (self.x, self.y)) #uses above list 'walkleft', which is a list of images. prints the image at index walkcount//3
                self.walkCount += 1

            elif man.right:
                win.blit(walkRight[self.walkCount // 3], (self.x, self.y)) #same as above but for walking right
                self.walkCount += 1

        else:
            if self.right:          #makes it so whatever direction player was facing when moving will be the same direction they're facing when they stop
                win.blit(walkRight[0], (self.x, self.y))
            else:
                win.blit(walkLeft[0], (self.x, self.y))

        self.hitbox = (self.x + 20, self.y + 13, 26, 50) #updates hitbox coords
        pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2) #draws hitbox


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

class enemy(object): #new class for enemies
    walkRight = [pygame.image.load('R1E.png'), pygame.image.load('R2E.png'), pygame.image.load('R3E.png'), pygame.image.load('R4E.png'), pygame.image.load('R5E.png'), pygame.image.load('R6E.png'), pygame.image.load('R7E.png'), pygame.image.load('R8E.png'), pygame.image.load('R9E.png'), pygame.image.load('R10E.png'), pygame.image.load('R11E.png')]
    walkLeft = [pygame.image.load('L1E.png'), pygame.image.load('L2E.png'), pygame.image.load('L3E.png'), pygame.image.load('L4E.png'), pygame.image.load('L5E.png'), pygame.image.load('L6E.png'), pygame.image.load('L7E.png'), pygame.image.load('L8E.png'), pygame.image.load('L9E.png'), pygame.image.load('L10E.png'), pygame.image.load('L11E.png')]

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end] #where the enemy starts walking and where it stops
        self.walkCount = 0
        self.vel = 3
        self.hitbox = (self.x + 15, self.y, 26, 60)


    def draw(self, win):
        self.move()
        if self.walkCount + 1 >= 33:
            self.walkCount = 0


        if self.vel > 0:
            win.blit(self.walkRight[self.walkCount // 3], (self.x, self.y))
            self.walkCount += 1 #changing the index for images

            self.hitbox = (self.x + 15, self.y , 26, 58) #updates hitbox coords
            pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2) #draws hitbox

        else:
            win.blit(self.walkLeft[self.walkCount // 3], (self.x, self.y))
            self.walkCount += 1

            self.hitbox = (self.x + 28, self.y , 26, 58) #updates hitbox coords
            pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2) #draws hitbox

    def hit(self): #what happens when enemy is hit
        print('Hit!')
        pass

    def move(self):
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




def redrawGameWindow():
    win.blit( bg, (0, 0)) #blits the image of 'bg'
    man.draw(win) #calling the function above
    goblin.draw(win)
    for bullet in bullets:
        bullet.draw(win) #drawing the bullets

    pygame.display.update() #updates the screen


#mainloop

man = player(300, 410, 64, 64) #creating player instance 'man', which is a type of player

goblin = enemy(100, 415, 64, 64, 450) #creating enemy instance 'goblin'

bullets = [] #list for containing bullets

shootLoop = 0 #bullet cooldown timer variable.



run = True
while run:
    clock.tick(27) #sets fps to 27

    if shootLoop > 0: #bullet cooldown loop. Basic timer. shootLoop is global variable declared outside of main loop and is first updated after bullet is shot.
        shootLoop += 1
    if shootLoop > 5: #sets duration of timer
        shootLoop = 0


    for event in pygame.event.get(): #quiting the game when you press 'x' on the window
        if event.type == pygame.QUIT:
            run = False


    '''Bullet mechanics'''
    for bullet in bullets:

        #checking bullet collision with enemy
        if (bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] #hitbox[1] + hitbox[3] = bottom of hitbox. checks if bullet is above bottom of hitbox
            and bullet.y + bullet.radius > goblin.hitbox[1]): #checks if bullet is below the top of hitbox

            if (bullet.x + bullet.radius > goblin.hitbox[0] #hitbox[0] = left hitbox border
                and bullet.x - bullet.radius < goblin.hitbox[2] + goblin.hitbox[0]): #hitbox[2] + hitbox[0] = right border of hitbox

                    goblin.hit()
                    bullets.pop( bullets.index( bullet )) #removing the bullet after it has hit the goblin


        if bullet.x < 500 and bullet.x > 0: #ensure bullet is confined within bounds
            bullet.x += bullet.vel  #moving bullet

        else:
            bullets.pop( bullets.index( bullet ) ) #making the bullet disappear when it hits the edge of the screen


    ''' Movement'''
    keys = pygame.key.get_pressed() #what happens when you press each key

    if keys[pygame.K_SPACE] and shootLoop == 0: # only allows bullet to shoot when shootLoop = 0. Basic timer.
        if man.left:
            facing = -1     #variable 'facing' is used in projectile class to determine direction of bullet
        else:
            facing = 1

    #limits number of projectiles at a time to the set number
        if len(bullets) < 100:

            bullets.append(projectile( round(man.x + man.width//2), round(man.y + man.height//2), 6, (0, 0, 0), facing))

        shootLoop = 1


    if keys[pygame.K_a]: #move left
        if man.x > 0:
            if (man.x - man.vel) < 0:        # declaring screen boundaries for player
                man.x -= man.x
            else:
                man.x -= man.vel
        man.left = True
        man.right = False
        man.standing = False

    elif keys[pygame.K_d]:#move right
        if man.x < (ScreenWidth - man.width):
            if (man.x + man.vel) > (ScreenWidth - man.width):
                man.x += ((ScreenWidth - man.width) - man.x)
            else:
                man.x += man.vel
        man.left = False
        man.right = True
        man.standing = False

    else:
        man.standing = True
        man.walkCount = 0

    if man.isJump == False:
        ''' Jumping'''
        if keys[pygame.K_w]: #jump
            man.isJump = True

    else:
        if man.jumpCount >= -10: #jumpCount is counting the pixels that the player is jumping

            neg = 1 #neg is to toggle if player is still jumping up or has started to fall down
            if man.jumpCount < 0:
                neg = -1 #neg = -1 will make player movement negative (the falling part of the jump)

            man.y -= (man.jumpCount ** 2) * 0.5 * neg
            #using a quadratic funct4on to make each position change smaller than the last. This will ensure that proper jump physics is shown

            man.jumpCount -= 2
            #decreasing the jumpCount by 1 each time player moves (so player moves 20 times if jumpCount = 10. since 10 -> -10 = 20 times)

        else:
            man.isJump = False
            man.jumpCount = 10


    redrawGameWindow()


pygame.quit()

