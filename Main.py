'''
Ellis Hu
2026/10/17 - 2026/11/07
Time taken: 11 hours
Game is supposed to somewhat resemble a mix of touhou 
and IMPOSSIBLE SNAKE by marchalade

TO ADD: 
- Intro screen
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
intro_music_finished = False

pygame.mixer.init()
pygame.mixer.music.load('sfx/intro.mp3')
pygame.mixer.music.play()

if not intro_music_finished and not pygame.mixer.music.get_busy():
    pygame.mixer.music.load('sfx/loop.mp3')
    pygame.mixer.music.play(-1)
    intro_music_finished = True

clock = pygame.time.Clock()

font = pygame.font.Font(None, 28)


# Creating sprites
char_sprites = pygame.sprite.Group()     
bullets = pygame.sprite.Group()

player = aaa.Player(window)
player_hp_bar = aaa.Player_hp(window, player)

cat_img = pygame.image.load('imgs/cat.png').convert_alpha()
cat = aaa.Cat(250, 100, cat_img, window)
cat_atk = aaa.Cat_attack(window, player, 'paw')


# DIALOGUE DIALOGUE DIALOGUE !!
dialogue = aaa.Dialogue(window)
intro_speaking = [{'text' : ('and so we meet again, pesky serpent')}, 
                  {'text' : ("you've been a ssslithering pest in my ssside for too long")}, 
                  {'text' : ('this food chain isnt large enough for the two of us, dear Python')}, 
                  {'text' : ('i best you in scale(s), afterall')}, 
                  {'text' : ('prepare to end')},
                  {'text' : ('HERE')},
                  {'text' : ('AND')},
                  {'text' : ('MEOWWW!')},]
dialogue.start(intro_speaking)

char_sprites.add(player, cat)







def loop():
    gamestate = 0
        # Cat timers
    cat_action_timer = 0
    cat_act_delay = 750
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit(0) 

            if event.type == pygame.KEYDOWN:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE: 
                    # For dialogue progression in intro
                    if dialogue.active:
                        dialogue.next()
                    elif gamestate == 0 and len(bullets) == 0:
                        # if the game starts then space is used for attacking
                        bullets.add(aaa.Bullet(player, cat))
                        player.atk()


        if gamestate == 0 and not dialogue.active:
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
        pygame.draw.rect(window, (0, 0, 0), (0, 530, 600, 70))

        if gamestate == 0:
            cat_atk.update()
            char_sprites.draw(window)
            bullets.draw(window)
            player_hp_bar.update()

            
            if dialogue.active:
                dialogue.update()
                # blit the box
                window.blit(dialogue.textbox_frame[dialogue.curr_frame], (0, 0))
                # blit dialogue
                lines = dialogue.wrap_text(dialogue.text_display, 500)
                for i, line in enumerate(lines):
                    text = font.render(line, True, (255,255,255))
                    window.blit(text, (50, 400 + i * 30))

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