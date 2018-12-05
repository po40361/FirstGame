import pygame
pygame.init()

EVENT = pygame.USEREVENT + 1

pygame.time.set_timer(pygame.USEREVENT, 500)

while True:

    for event in pygame.event.get():
        if event.type == pygame.USEREVENT:
            print("hi")





