import pygame
import random

pygame.init()

window = pygame.display.set_mode((800, 600))
window.fill((0, 0, 0))
pygame.display.set_caption("Snek")

# PLAYER
player = pygame.surface.Surface((100,100))
player.fill((255, 255, 255))
# player display
player = pygame.image.load("player.png").convert_alpha()
player = pygame.transform.scale(player, (100, 100))

# Player vars
player_x = 0
player_y = 0
player_vel_x = 0
player_vel_y = 0

# OBJECT
#will come soon awestdrytfgvybhujnimko,,plijmuhnygbtfedwavbk hcenwuiogfeyqufubhhhgywhwqh work on this

# idea: different animals with diff speeds and movement pattersn
# basically snake but now it real frfr







# Object Vars
object_x = 0
object_y = 0
object_vel_x = 0
object_vel_y = 0


def collision():
    '''Checks for collision between player and object'''
    if (player_x <= (object_x + object.width) and 
        (player_x +player.width) >= object_x and 
        player_y <= (object_y + object.height) and 
        (player_y + player.height) >= object_y):
        return True
    else:
        return False


while True:
    # Quit statement
    for event in pygame.event.get():
        # INPUTs
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                player_vel_y = -5
            if event.key == pygame.K_s:
                player_vel_y = 5
            if event.key == pygame.K_a:
                player_vel_x = -5
            if event.key == pygame.K_d:
                player_vel_x = 5
            else:
                player_vel_x = 0
                player_vel_y = 0

    if object_x >= window.height:
        # edit this so it changes movement direction when it hits the wall esdrtfyguhijoiakeprgoshtrjitsrugrefyewdtwt






        if event.type == pygame.QUIT:
            quit(0)

    window.fill((0, 0, 0))

    # Update player movement
    player_x += player_vel_x
    player_y += player_vel_y
    # Update object movement
    object_x += object_vel_x
    object_y += object_vel_y

    # 1. Draw thingy 2. where is it being drawn on screen
    window.blit(player, (player_x, player_y))
    window.blit(object, (object_x, object_y))

    #Keep this at the end or it lowk wont work
    pygame.display.flip()
