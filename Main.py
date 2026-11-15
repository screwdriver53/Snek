'''
Ellis Hu
2026/10/17 - 2026/11/15
Time taken: 15 hours
Game is supposed to somewhat resemble a mix of touhou, IMPOSSIBLE SNAKE by marchalade,
and The Binding of Issac

TO ADD: 
- Phase 2 and 3
    - New sprites for cat
    - New attacks for cat

- win/lose animations
- Maybe a sort of "brain" or learning algorithm, where it will be noted
    where the player likes to hang out at to increase attack frequency in that area
'''
import aaa
import pygame
from utils import resource_path

# DISPLAY
pygame.init()
window = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Dear Magic Cat")
background = pygame.image.load(resource_path("imgs/background.png")).convert_alpha()
background = pygame.transform.scale(background, (600,600))





# SOUNDS

pygame.mixer.init()
pygame.mixer.music.load(resource_path("sfx/intro.mp3"))
pygame.mixer.music.play()


clock = pygame.time.Clock()

font = pygame.font.Font(None, 28)


# Creating sprites
char_sprites = pygame.sprite.Group()     
bullets = pygame.sprite.Group()
yarn = pygame.sprite.Group()

player = aaa.Player(window)
player_hp_bar = aaa.Player_hp(window, player)

cat_img = pygame.image.load(resource_path("imgs/cat.png"))
cat = aaa.Cat(250, 100, cat_img, window)
cat_atk = aaa.Cat_attack(window, player, 'paw')


# DIALOGUE DIALOGUE DIALOGUE !!
dialogue = aaa.Dialogue(window)
intro_speaking = [{'text' : ('hello!! you play as the snake')}, 
                  {'text' : ('use WASD to move and SPACE to shoot')}, 
                  {'text' : ('your goal is to obliterate me, the cat')}, 
                  {'text' : ('however, i do attack back. so make sure to avoid the appearing red squares! a sound cue will be played when i attack')}, 
                  {'text' : ("that's all for the tutorial, so moving on!!")}, 
                  {'text' : ('and so we meet again, pesky serpent')}, 
                  {'text' : ("you've been a ssslithering pest in my ssside for too long")}, 
                  {'text' : ('this food chain isnt large enough for the two of us, dear Python')}, 
                  {'text' : ('i best you in scale(s), afterall')}, 
                  {'text' : ('prepare to end')},
                  {'text' : ('HERE')},
                  {'text' : ('AND')},
                  {'text' : ('MEOWWW!')},]

d1 = [{'text' : ('pesky ssserpent..')},
      {'text' : ('i believe i underestimated you')},
      {'text' : ('you may be more grand of an opponent than i originally believed')},
      {'text' : ('you may have lasted up until now')},
      {'text' : ('but your luck spree ends here')},
      {'text' : ('ill draw a line in the sand so you can see')},
      {'text' : ('ok so like')}]

d2 = [{'text' : ('snake?')},
      {'text' : ('more like...')},
      {'text' : ('DUMB')},
      {'text' : ('get it cuz ur dumb and a snake')},
      {'text' : ('ok anyways i rlly hate u man')},
      {'text' : ('like im hungry and youre just eating everything')},
      {'text' : ('youre also always in the way')},
      {'text' : ('im gonna skip you like a jump rope')}]

dialogue.start(intro_speaking, 'norm')

char_sprites.add(player, cat)



def loop():
    
    intro_finished = False
    gamestate = 0
    winlose = None
    phase = 1
        # Cat timers
    cat_action_timer = 0
    cat_act_delay = 1000
    
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

            if cat_action_timer >= cat_act_delay and cat_atk.finished:
                cat.action(cat_atk, phase, yarn, player)
                cat_action_timer = 0

            player.movement()
            player.update()
            cat.update()

            for bullet in bullets.copy():
                bullet.movement()
                
                for yarn_ball in yarn.copy():
                    if bullet.rect.colliderect(yarn_ball.rect):
                        yarn_ball.hp -= 1
                        bullet.kill()
                        if yarn_ball.hp <= 0:
                            yarn_ball.kill()
                        break

            if cat.hp <= 0 and phase == 3:
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
            yarn.update()
            yarn.draw(window)

            if cat.hp <= 0 and phase == 1:
                phase = 2
                cat_act_delay = 750
                cat_atk.cancel_atk()
                cat.reset(phase)
                char_sprites.add(cat)
                dialogue.textbox_change('witch1')
                dialogue.start(d1, 'witch1')
            elif cat.hp <= 0 and phase == 2:
                phase = 3
                cat_act_delay = 450
                cat_atk.cancel_atk()
                cat.reset(phase)
                char_sprites.add(cat)
                dialogue.textbox_change('witch2')
                dialogue.start(d2, 'witch2')
            elif cat.hp <= 0 and phase == 3:
                gamestate = 1

            if not intro_finished and not pygame.mixer.music.get_busy():
                pygame.mixer.music.load(resource_path('sfx/loop.mp3'))
                pygame.mixer.music.play(-1)
                intro_finished = True
            
            if dialogue.active:
                dialogue.update()
                # blit the box
                window.blit(dialogue.textbox_frame[dialogue.current_textbox][dialogue.curr_frame], (0, 0))
                # blit dialogue
                lines = dialogue.wrap_text(dialogue.text_display, 500)
                for i, line in enumerate(lines):
                    text = font.render(line, True, (255,255,255))
                    window.blit(text, (50, 400 + i * 30))

        elif gamestate == 1:
            if winlose == None:
                winlose = aaa.WinLose(window, 'win')
            winlose.update()
    
        elif gamestate == 2:
            if winlose == None:
                winlose = aaa.WinLose(window, 'lose')
            winlose.update()

        pygame.display.flip()
        clock.tick(60)

loop()