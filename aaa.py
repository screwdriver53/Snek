import pygame
import random

    # Overall parent class, majority of sprites will be based on this i think idk
class basic(pygame.sprite.Sprite):
    def __init__(self, image, x, y, active):
        super().__init__()
        self.image = image
        self.x = x
        self.y = y
        self.active = active
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    # Player class

# PLAYER RELATED CLASSES
class Player(basic):
    def __init__(self, screen):
        self.slow = 0
        self.hp = 3
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()
        self.sprites = {'walk':[pygame.image.load("imgs/mc/move1.png").convert_alpha(),
                                pygame.image.load("imgs/mc/move2.png").convert_alpha(),
                                pygame.image.load("imgs/mc/move3.png").convert_alpha(),
                                pygame.image.load("imgs/mc/move4.png").convert_alpha(),
                                pygame.image.load("imgs/mc/move5.png").convert_alpha(),
                                pygame.image.load("imgs/mc/move6.png").convert_alpha(),
                                pygame.image.load("imgs/mc/move7.png").convert_alpha(),
                                ], 
                        'attack':[pygame.image.load("imgs/mc/atk_1.png").convert_alpha(),
                                  pygame.image.load("imgs/mc/atk_2.png").convert_alpha(),
                                  pygame.image.load("imgs/mc/atk_3.png").convert_alpha(),
                                  pygame.image.load("imgs/mc/atk_4.png").convert_alpha(),
                                ]}
        self.state = 'walk'
        self.current_sprite = 0
        self.image = self.sprites[self.state][self.current_sprite]
        
        super().__init__(self.sprites['walk'][0], 100, 100, True)
        
        self.hitbox_radius = 35
        self.hitbox = pygame.Rect(0, 0, self.hitbox_radius * 2, self.hitbox_radius * 2)
        self.hitbox.center = self.rect.center

    def hp(self):
        return self.hp

    def movement(self):
        key = pygame.key.get_pressed()

        speed = 4
        if pygame.time.get_ticks() < self.slow:
            speed = 2

        dx = 0
        dy = 0

        if key[pygame.K_w]:
            dy = -speed
        if key[pygame.K_s]:
            dy = speed
        if key[pygame.K_a]:
            dx = -speed
        if key[pygame.K_d]:
            dx = speed

        self.rect.x += dx
        self.rect.y += dy

        self.keep_inbounds()
        self.hitbox.center = self.rect.center

    def keep_inbounds(self):
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > self.width:
            self.rect.right = self.width
        if self.rect.top < 0:
            self.rect.top = 0

        if self.rect.bottom > self.screen.get_height() - 70:
            self.rect.bottom = self.screen.get_height() - 70

    def atk(self):
        if self.state != 'attack':
            self.state = 'attack'
            self.current_sprite = 0

    def update(self):
        frames = self.sprites[self.state]
        self.current_sprite += 0.25

        if int(self.current_sprite) >= len(frames):
            if self.state == 'attack':
                self.state = 'walk'
                self.current_sprite = 0
                frames = self.sprites['walk']
            else:
                self.current_sprite = 0

        self.image = frames[int(self.current_sprite)]

class Player_hp():
    def __init__(self, screen, player):
        self.screen = screen
        self.player = player
        self.sprites = [pygame.image.load("imgs/mc/hp_bar/Snake_hp1.png").convert_alpha(),
                        pygame.image.load("imgs/mc/hp_bar/Snake_hp2.png").convert_alpha(),
                        pygame.image.load("imgs/mc/hp_bar/Snake_hp3.png").convert_alpha(),
                        pygame.image.load("imgs/mc/hp_bar/Snake_hp4.png").convert_alpha(),
                        ]
    def update(self):
        image = self.sprites[3 - self.player.hp]
        self.screen.blit(image, (10, 520))

    # Player bullet class
class Bullet(basic):
    def __init__(self, player, cat):
        self.image = pygame.image.load("imgs/bullet.png").convert_alpha()

        x = player.rect.centerx - self.image.get_width()//2
        y = player.rect.top

        super().__init__(self.image, x, y, True)
        self.cat = cat
    def movement(self):
        self.rect.y -= 10
            # if it hits the cat
        if self.rect.colliderect(self.cat.rect):
            self.cat.hp -= 1
            self.kill()
            self.bullet_CD = False

            if self.cat.hp <= 0:
                self.cat.kill()
            return

            # kill bullet if hit screen
        if self.rect.bottom < 0:
            self.kill()
            self.bullet_CD = False
            return

        


    # Cat class

# CAT RELATED CLASSES
class Cat(basic):
    def __init__(self, x, y, image, screen):
        super().__init__(image, x, y, True)
        
        self.hp = 9
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()

        self.sprites = {
            1 : {'walk':[pygame.image.load('imgs/p1/walk1.png').convert_alpha(),
                            pygame.image.load('imgs/p1/walk2.png').convert_alpha(),
                            pygame.image.load('imgs/p1/walk3.png').convert_alpha(),
                            pygame.image.load('imgs/p1/walk4.png').convert_alpha(),
                            pygame.image.load('imgs/p1/walk5.png').convert_alpha(),
                            pygame.image.load('imgs/p1/walk6.png').convert_alpha(),
                            ],
                    'attack':[pygame.image.load('imgs/p1/atk1.png').convert_alpha(),
                            pygame.image.load('imgs/p1/atk2.png').convert_alpha(),
                            pygame.image.load('imgs/p1/atk3.png').convert_alpha(),
                            pygame.image.load('imgs/p1/atk4.png').convert_alpha(),
                            pygame.image.load('imgs/p1/atk5.png').convert_alpha(),
                            pygame.image.load('imgs/p1/atk6.png').convert_alpha(),
                            ]
                    },
            2 : {'walk':[pygame.image.load('imgs/p2/walk1.png').convert_alpha(),
                            pygame.image.load('imgs/p2/walk2.png').convert_alpha(),
                            pygame.image.load('imgs/p2/walk3.png').convert_alpha(),
                            pygame.image.load('imgs/p2/walk4.png').convert_alpha(),
                            pygame.image.load('imgs/p2/walk5.png').convert_alpha(),
                            pygame.image.load('imgs/p2/walk6.png').convert_alpha(),
                            ],
                    'attack':[pygame.image.load('imgs/p2/atk1.png').convert_alpha(),
                            pygame.image.load('imgs/p2/atk2.png').convert_alpha(),
                            pygame.image.load('imgs/p2/atk3.png').convert_alpha(),
                            pygame.image.load('imgs/p2/atk4.png').convert_alpha(),
                            pygame.image.load('imgs/p2/atk5.png').convert_alpha(),
                            pygame.image.load('imgs/p2/atk6.png').convert_alpha(),
                            ]
                    },
            3 : {'walk':[pygame.image.load('imgs/p3/walk1.png').convert_alpha(),
                            pygame.image.load('imgs/p3/walk2.png').convert_alpha(),
                            pygame.image.load('imgs/p3/walk3.png').convert_alpha(),
                            pygame.image.load('imgs/p3/walk4.png').convert_alpha(),
                            pygame.image.load('imgs/p3/walk5.png').convert_alpha(),
                            pygame.image.load('imgs/p3/walk6.png').convert_alpha(),
                            ],
                    'attack':[pygame.image.load('imgs/p3/atk1.png').convert_alpha(),
                            pygame.image.load('imgs/p3/atk2.png').convert_alpha(),
                            pygame.image.load('imgs/p3/atk3.png').convert_alpha(),
                            pygame.image.load('imgs/p3/atk4.png').convert_alpha(),
                            pygame.image.load('imgs/p3/atk5.png').convert_alpha(),
                            pygame.image.load('imgs/p3/atk6.png').convert_alpha(),
                            ]
                    }
        }
        self.state = 'walk'
        self.current_sprite = 0
        self.move = x
        
        self.phase = 1

    def action(self, cat_atk, phase, yarn, player):
        action = random.randint(1, 2)

        if action == 1:
            self.movement()
        else:
            self.attack(cat_atk, phase, yarn, player)

    def movement(self):
        self.state = 'walk'

        if self.rect.x == self.move:
            self.move = random.randint(0, self.width - self.rect.width)

        if self.rect.x < self.move:
            self.rect.x = min(self.rect.x + random.randint(5, 50), self.move)
        elif self.rect.x > self.move:
            self.rect.x = max(self.rect.x - random.randint(5, 50), self.move)

        self.keep_inbounds()

    def keep_inbounds(self):
        if self.rect.left < 0:
            self.rect.left = 0

        if self.rect.right > self.width:
            self.rect.right = self.width

    def attack(self, cat_atk, phase, yarn, player):
        self.state = 'attack'

        if cat_atk.finished and phase == 1: 
            self.atk = random.randint(1,2)
        
            if self.atk == 1:
                cat_atk.atk_paw()
            else:
                cat_atk.atk_scratch()
        
        elif phase == 2:
            self.atk = random.randint(1,3)

            if self.atk == 1:
                cat_atk.atk_paw()
            elif self.atk == 2:
                cat_atk.atk_scratch()
            else:
                cat_atk.spell_yarn(yarn, player)

        elif phase == 3:
            self.atk = random.randint(1,3)

            if self.atk == 1:
                cat_atk.atk_paw()
            elif self.atk == 2:
                cat_atk.atk_scratch()
            else:
                cat_atk.spell_yarn(yarn, player)


    def reset(self, phase):
        self.hp = 9
        self.rect.center = (300, 100)

        # when the phase change lmao
        self.phase = phase
        self.current_sprite = 0
        self.state = 'walk'
        self.image = self.sprites[self.phase][self.state][0]


    def update(self):
        frames = self.sprites[self.phase][self.state]

        if frames:
            self.current_sprite += 0.25
            if int(self.current_sprite) >= len(frames):
                self.current_sprite = 0

            self.image = frames[int(self.current_sprite)]
        self.keep_inbounds()

    # Cat attack class
class Cat_attack():
    def __init__(self, screen, player, state):
        self.warning_sfx = pygame.mixer.Sound('sfx/cat_atk_warn.mp3')
        self.screen = screen
        self.player = player
        self.state = state

        self.hitbox = None

        self.finished = True
        self.hit_player = False
    
        self.sprites = {'scratch':[pygame.image.load("imgs/scratch/scratch0.png").convert_alpha(),
                                   pygame.image.load("imgs/scratch/scratch1.png").convert_alpha(),
                                   pygame.image.load("imgs/scratch/scratch2.png").convert_alpha(),
                                   pygame.image.load("imgs/scratch/scratch3.png").convert_alpha(),
                                   pygame.image.load("imgs/scratch/scratch4.png").convert_alpha(),
                                   pygame.image.load("imgs/scratch/scratch5.png").convert_alpha()],
                        'paw':[pygame.image.load("imgs/paw/paw1.png").convert_alpha(),
                               pygame.image.load("imgs/paw/paw2.png").convert_alpha(),
                               pygame.image.load("imgs/paw/paw3.png").convert_alpha(),
                               pygame.image.load("imgs/paw/paw4.png").convert_alpha(),
                               pygame.image.load("imgs/paw/paw5.png").convert_alpha(),
                               pygame.image.load("imgs/paw/paw6.png").convert_alpha(),
                               pygame.image.load("imgs/paw/paw7.png").convert_alpha(),
                               pygame.image.load("imgs/paw/paw8.png").convert_alpha(),]
                        }

        self.current_sprite = 0
        self.image = self.sprites[self.state][self.current_sprite]

    def atk_scratch(self):
        '''Phase 1 - scratch'''
            # Changes state for animation
        self.state = 'scratch'

        # Set atk
        self.width = 180
        self.height = 220
        self.warn = 1200
        self.atk = 600
        self.do_atk()

    
    def atk_paw(self):
        '''Phase 1 - paw'''
            # Changes state for animation
        self.state = 'paw'

        # Set atk 
        self.width = 200
        self.height = 280
        self.warn = 1500
        self.atk = 600
        self.do_atk()

    def spell_yarn(self, yarn, player):
        self.state = 'yarn'
        self.width = 60
        self.height = 60
        self.warn = 1000
        self.atk = 0

        self.yarn = yarn
        self.player = player

        self.do_atk()
    
    def do_atk(self):
            # Keeping in bounds
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()
        x = random.randint(0, screen_width - self.width)
        y = random.randint(0, screen_height - 70 - self.height)

        # 
        self.hitbox = pygame.Rect(x, y, self.width, self.height)

            # Track atk time and if it did sumthing
        self.start_time = pygame.time.get_ticks()
        self.finished = False
        self.hit_player = False
        self.current_sprite = 0 

        self.warning_sfx.play()

    def update(self):
        if self.finished:
            return
        
        time_passed = pygame.time.get_ticks() - self.start_time

        #warning
        if time_passed < self.warn:
            pygame.draw.rect(self.screen, (255,0,0), self.hitbox, 3)

        #yarn
        elif self.state == 'yarn':
            self.yarn.add(Yarn(self.hitbox.x, self.hitbox.y, self.player))
            self.finished = True
            return

        # attacking
        elif time_passed < self.warn + self.atk:
            frames = self.sprites[self.state]
            self.current_sprite += 0.25

            if int(self.current_sprite) >= len(frames):
                self.current_sprite = 0
        
            self.image = frames[int(self.current_sprite)]
            self.image = pygame.transform.scale(self.image, (self.width, self.height))
            self.screen.blit(self.image, self.hitbox.topleft)

            if self.hit_player == False and self.hitbox.colliderect(self.player.hitbox):
                self.player.hp -= 1
                self.hit_player = True
        else:
            self.finished = True
            return

class Yarn(basic):
    def __init__(self, x, y, player):
        image = pygame.image.load("imgs/yarn0.png").convert_alpha()
        image = pygame.transform.scale(image, (50, 50))

        super().__init__(image, x, y, True)
        
        self.player = player
        self.hp = 1

        self.spawn = pygame.time.get_ticks()
        self.life = 5000

        self.touched = False

    def update(self):
        curr_time = pygame.time.get_ticks()

        if curr_time - self.spawn >= self.life:
            self.kill()
            return
        if not self.touched and self.rect.colliderect(self.player.rect):
            self.player.slow = curr_time + 2000
            self.touched = True
            self.kill()
            return
        
    

# MISC CLASSES
class Dialogue():
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 28)
        
        self.dialogue = []
        self.index = 0
        self.text_display = ''
        self.char_timer = 0
        self.char_delay = 50

        self.active = False
        self.finished = False

        self.textbox_frame = {'norm': [pygame.image.load("imgs/textbox/p1_cat_talk0.png").convert_alpha(),
                                       pygame.image.load("imgs/textbox/p1_cat_talk1.png").convert_alpha()],
                            'witch1': [pygame.image.load("imgs/textbox/p2_cat_talk2.png").convert_alpha(),
                                        pygame.image.load("imgs/textbox/p2_cat_talk3.png").convert_alpha()],
                            'witch2': [pygame.image.load("imgs/textbox/p3_cat_talk4.png").convert_alpha(),
                                        pygame.image.load("imgs/textbox/p3_cat_talk5.png").convert_alpha()],}
        self.curr_frame = 0
        self.current_textbox = 'norm'

    def start(self, dialogue, textbox = 'norm'):
        self.dialogue = dialogue
        self.current_textbox = textbox
        self.curr_frame = 0
        self.index = 0
        self.text_display = ''
        self.char_timer = 0
        self.char_delay = 50
        self.active = True
        self.finished = False

    def update(self): 
        if not self.active:
            return

        current_line = self.dialogue[self.index]['text']
        if len(self.text_display) < len(current_line):
            self.curr_frame = 0
            self.char_timer += 1

            if self.char_timer >= self.char_delay // (1000//60):
                self.text_display += current_line[len(self.text_display)]
                self.char_timer = 0
        else:
            self.curr_frame = 1

    def next(self):
        if not self.active:
            return
        current_line = self.dialogue[self.index]['text']

        if len(self.text_display) < len(current_line):
            self.text_display = current_line
        else:
            self.index += 1

            if self.index >= len(self.dialogue):
                self.active = False
                self.finished = True
            else:
                self.text_display = ''
                self.char_timer = 0
                self.curr_frame = 0

    def textbox_change(self, textbox):
        self.current_textbox = textbox
        self.curr_frame = 0

    def wrap_text(self, text, max_width):
        words = text.split(' ')
        lines = []
        current_line = ''

        for word in words:
            test_line = current_line + word + ' '

            if self.font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word + ' '

        lines.append(current_line.strip())
        return lines
