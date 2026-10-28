'''
Ellis Hu
2026/10/17 - 2026/10/28
Time taken: 8 hours
Game is supposed to somewhat resemble a mix of touhou 
and IMPOSSIBLE SNAKE by marchalade

TO ADD: 
- Player bullet delays
- Intro screen
- Cat phases? (9?)
'''
import aaa
import pygame

# DISPLAY
pygame.init()
window = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Oh, Cats!")
background = pygame.image.load("imgs/background.png").convert_alpha()
background = pygame.transform.scale(background, (600,600))

# SOUNDS
pygame.mixer.init()
pygame.mixer.music.load('sfx/intro.mp3')
pygame.mixer.music.play()
intro_fin = False

if intro_fin == False and pygame.mixer.music.get_busy == False:
    pygame.mixer.music.load('sfx/loop.mp3')
    pygame.mixer.music.play(-1)
    intro_fin = True

clock = pygame.time.Clock()

# Creating sprites
char_sprites = pygame.sprite.Group()     
bullets = pygame.sprite.Group()

player = aaa.Player(window)
cat_img = pygame.image.load('imgs/cat.png').convert_alpha()
cat = aaa.Cat(250, 100, cat_img, window)

bullet = aaa.Bullet(player, cat)
cat_atk = aaa.Cat_attack(window, player, 'paw')

char_sprites.add(player, cat)

font = pygame.font.Font(None, 64)

def loop():
    gamestate = 0
    cat_action_timer = 0
    cat_act_delay = 1000
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit(0) 

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullets.add(aaa.Bullet(player, cat))
                    player.atk()

        if gamestate == 0:
            cat_action_timer += clock.get_time()

            if cat_action_timer >= cat_act_delay:
                cat.action(cat_atk)
                cat_action_timer = 0

            player.movement()
            player.update()
            cat.update()

            for bullet in bullets.copy():
                bullet.movement()

            if cat.hp <= 0:
                gamestate = 1
            elif player.hp <= 0:
                gamestate = 2

        window.blit(background, (0,0))

        if gamestate == 0:
            cat_atk.update()
            char_sprites.draw(window)
            bullets.draw(window)

        elif gamestate == 1:
            window.fill((0,0,0))
            text = font.render('you win!', True, (255,255,255))
            window.blit(text, (300,300))
    
        elif gamestate == 2:
            window.fill((0,0,0))
            text = font.render('you lost :(', True, (255,255,255))
            window.blit(text, (300,300))

        pygame.display.flip()
        clock.tick(60)

loop()