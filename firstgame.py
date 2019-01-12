import pygame
import playerClass
import enemyClass
import bulletClass


pygame.init()

ScreenWidth = 500
ScreenHeight = 500

win = pygame.display.set_mode((ScreenWidth, ScreenHeight))
	#creates a surface

pygame.display.set_caption("First Game")

#different lists for sprites and animations


bg = pygame.image.load('bg.jpg')

char = pygame.image.load('sprites/standing.png')

clock = pygame.time.Clock() #allows for toggling fps


class timer(object):

    def __init__(self, duration):
        self.duration = duration
        self.counter = 0

    def loop(self):
        if self.counter > 0:
            self.counter += 1
        if self.counter > self.duration:
            self.counter = 0


def redrawGameWindow():
    win.blit( bg, (0, 0)) #blits the image of 'bg'
    man.draw(win) #calling the function above
    goblin.draw(win)
    for bullet in bullets:
        bullet.draw(win) #drawing the bullets

    randNumLabel = myFont.render("Score: "+ str(score), 1, (0, 0, 0)) #prints score
    win.blit(randNumLabel, (400, 10)) #draws scoreboard

    gameOverMsg = myFont.render("GAME OVER!", 1, (0, 0, 0))
    if man.health <= 0:
        win.blit(gameOverMsg, (190, 200))


    pygame.display.update() #updates the screen


#mainloop

man = playerClass.player(300, 410, 64, 64) #creating player instance 'man', which is a type of player


goblin = enemyClass.enemy(100, 415, 64, 64, 100, 0) #creating enemy instance 'goblin'

bullets = [] #list for containing bullets

#shootLoop = 0 #bullet cooldown timer variable.

#hitLoop = 0 #goblin hit cooldown

myFont = pygame.font.SysFont("Arial", 20, True) #declares font

shootLoop = timer(5) #declaring shootloop (must be outside of main loop)
hitLoop = timer(8)

run = True
while run:

    global score
    score = enemyClass.score

    clock.tick(54) #sets fps to 27

    shootLoop.loop()
    hitLoop.loop()

    for event in pygame.event.get(): #quiting the game when you press 'x' on the window
        if event.type == pygame.QUIT:
            run = False

    goblin.targetX = man.x
    goblin.targetY = man.y

    '''Bullet mechanics'''
    for bullet in bullets:

        #checking bullet collision with enemy
        if (bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] #hitbox[1] + hitbox[3] = bottom of hitbox. checks if bullet is above bottom of hitbox
            and bullet.y + bullet.radius > goblin.hitbox[1]): #checks if bullet is below the top of hitbox

            if (bullet.x + bullet.radius > goblin.hitbox[0] #hitbox[0] = left hitbox border
                and bullet.x - bullet.radius < goblin.hitbox[2] + goblin.hitbox[0]): #hitbox[2] + hitbox[0] = right border of hitbox

                    goblin.hit()
                    bullets.pop( bullets.index( bullet )) #removing the bullet after it has hit the goblin




        if bullet.x < ScreenWidth and bullet.x > 0: #ensure bullet is confined within bounds
            bullet.x += bullet.vel  #moving bullet

        else:
            bullets.pop( bullets.index( bullet ) ) #making the bullet disappear when it hits the edge of the screen

    '''player taking damage'''
    if man.isJump == False and goblin.hitting == True and hitLoop.counter == 0:
        man.hit()
        hitLoop.counter = 1


    ''' Movement'''
    keys = pygame.key.get_pressed() #what happens when you press each key

    if keys[pygame.K_SPACE] and shootLoop.counter == 0: # only allows bullet to shoot when shootLoop = 0. Basic timer.
        if man.left:
            facing = -1     #variable 'facing' is used in projectile class to determine direction of bullet
        else:
            facing = 1

    #limits number of projectiles at a time to the set number
        if len(bullets) < 100:

            bullets.append(bulletClass.projectile( round(man.x + man.width//2), round(man.y + man.height//2), 6, (0, 0, 0), facing))

        shootLoop.counter = 1


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
            #man.consecJumps +=1

    else:
        if man.jumpCount >= -10: #jumpCount is counting the pixels that the player is jumping

            neg = 1 #neg is to toggle if player is still jumping up or has started to fall down
            if man.jumpCount < 0:
                neg = -1 #neg = -1 will make player movement negative (the falling part of the jump)

            man.y -= (man.jumpCount ** 2) * 0.2 * neg
            #using a quadratic funct4on to make each position change smaller than the last. This will ensure that proper jump physics is shown

            man.jumpCount -= 2
            #decreasing the jumpCount by 1 each time player moves (so player moves 20 times if jumpCount = 10. since 10 -> -10 = 20 times)

        else:
            man.isJump = False
            #man.consecJumps = 0
            man.jumpCount = 10


    redrawGameWindow()


pygame.quit()

