import pygame
import playerClass
import enemyClass
import bulletClass
import powerupClass
import random


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

global gameStatus
gameStatus = True #true = game is still ongoing. False = gameover

class timer(object):

    def __init__(self, duration):
        self.duration = duration
        self.counter = 0

    def loop(self):
        if self.counter > 0:
            self.counter += 1
        if self.counter > self.duration:
            self.counter = 0

    def update(self, newDuration):
        self.duration = newDuration


def redrawGameWindow():
    win.blit( bg, (0, 0)) #blits the image of 'bg'
    global gameStatus


    if gameStatus:
        man.draw(win) #calling the function above
        goblin.draw(win)
        for bullet in bullets:
            bullet.draw(win) #drawing the bullets

        ammoDisplay = myFont.render("Ammo: " + str(man.ammo), 1,(165, 42, 42))
        win.blit(ammoDisplay, (400, 35)) #draws and displays ammo

        scoreBoard = myFont.render("Score: "+ str(score), 1, (0, 0, 0)) #prints score
        win.blit(scoreBoard, (400, 10)) #draws scoreboard

        for ammopack in ammopacks:
            ammopack.draw(win)

        for healthpack in healthpacks:
            healthpack.draw(win)


    gameOverMsg = myFont.render("GAME OVER!", 1, (0, 0, 0))
    scoreBoard = myFont.render("Score: "+ str(score), 1, (0, 0, 0))
    if man.health <= 0: #displaying game over when player dies
        gameStatus = False
        win.blit(gameOverMsg, (190, 200))
        win.blit(scoreBoard, (210, 250))
        man.ammo = 0

    winMsg = myFont.render("You Win!", 1, (0, 0, 0))
    if goblin.visible == False: #displaying "you win" when player kills goblin
        gameStatus = False
        win.blit(winMsg, (203, 200))
        win.blit(scoreBoard, (200, 240))
        man.ammo = 0




    pygame.display.update() #updates the screen


#mainloop

man = playerClass.player(300, 410, 64, 64) #creating player instance 'man', which is a type of player

#healthpack = powerupClass.powerup(random.randint(10, 490), (252, 5, 71))
#ammopack = powerupClass.powerup(random.randint(10, 490), (252, 5, 71))

goblin = enemyClass.enemy(100, 415, 64, 64, 100, 0) #creating enemy instance 'goblin'

ammopacks = []
healthpacks = []

bullets = [] #list for containing bullets

myFont = pygame.font.SysFont("Arial", 20, True) #declares font

shootLoop = timer(5) #declaring shootloop (must be outside of main loop)
hitLoop = timer(8)

ammopackTimerDuration = random.randint(50, 100)
ammopackLoop = timer(ammopackTimerDuration)

healthpackTimerDuration = random.randint(50, 100)
healthpackLoop = timer(healthpackTimerDuration)

run = True
while run:

    global score
    score = enemyClass.score

    clock.tick(54) #sets fps to 27

    shootLoop.loop()
    hitLoop.loop()
    ammopackLoop.loop()
    healthpackLoop.loop()

    for event in pygame.event.get(): #quiting the game when you press 'x' on the window
        if event.type == pygame.QUIT:
            run = False

    goblin.targetX = man.x
    goblin.targetY = man.y

    #print(ammopackLoop.counter)
    '''ammopack mechanics'''
    if len(ammopacks) == 0:
        ammopackTimerDuration = random.randint(50, 100)
        ammopackLoop.update(ammopackTimerDuration) #updates the timer duration

        if ammopackLoop.counter == 0:
            ammopacks.append(powerupClass.powerup(random.randint(10, 490), (11, 72, 132))) #adding ammopacks to list of ammopacks
            #print(ammopacks)
            #print(ammopackLoop.duration)

    for ammopack in ammopacks:
        if (ammopack.y - (ammopack.width/2) < man.hitbox[1] + man.hitbox[3]
            and ammopack.y + (ammopack.width/2) > man.hitbox[1]):

            if (ammopack.x + (ammopack.width/2) > man.hitbox[0]
                and ammopack.x - (ammopack.width/2) < man.hitbox[2] + man.hitbox[0]):

                ammopacks.pop( ammopacks.index(ammopack))#removing ammopack after it collides with player
                ammopackLoop.counter = 1
                man.ammo += 2
                #print(ammopacks)
                if man.ammo + 2 >= 10:
                    man.ammo = 10
                else:
                    man.ammo += 2




    '''healthpack mechanics'''
    if len(healthpacks) == 0:
        healthpackTimerDuration = random.randint(50, 100)
        healthpackLoop.update(healthpackTimerDuration) #updates the timer duration

        if healthpackLoop.counter == 0:
            healthpacks.append(powerupClass.powerup(random.randint(10, 490), (196, 17, 109))) #adding healthpack to list of healthpacks
            #print(ammopacks)
            #print(healthpackLoop.duration)

    for healthpack in healthpacks:
        if (healthpack.y - (healthpack.width/2) < man.hitbox[1] + man.hitbox[3] and healthpack.y + (healthpack.width/2) > man.hitbox[1]):

            if (healthpack.x + (healthpack.width/2) > man.hitbox[0]and healthpack.x - (healthpack.width/2) < man.hitbox[2] + man.hitbox[0]):

                healthpacks.pop( healthpacks.index(healthpack))#removing healthpack after it collides with player
                healthpackLoop.counter = 1
                if man.health + 3 >= 10:
                    man.health = 10
                else:
                    man.health += 3

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
    if man.isJump == False and goblin.hitting == True and hitLoop.counter == 0 and goblin.visible:
        man.hit()
        hitLoop.counter = 1


    ''' Movement'''
    keys = pygame.key.get_pressed() #what happens when you press each key

    if keys[pygame.K_SPACE] and shootLoop.counter == 0: # only allows bullet to shoot when shootLoop = 0. Basic timer.
        if man.right:
            facing = 1     #variable 'facing' is used in projectile class to determine direction of bullet
        else:
            facing = -1

    #limits number of projectiles at a time to the set number
        if len(bullets) < 100 and man.ammo > 0:

            bullets.append(bulletClass.projectile( round(man.x + man.width//2), round(man.y + man.height//2), 6, (0, 0, 0), facing))
            man.ammo -= 1

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

