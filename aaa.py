import pygame
import random

    # Overall parent class, majority of sprites will be based on this
class basic(pygame.sprite.Sprite):
    def __init__(self, image, x, y, active):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.x = x
        self.y = y
        self.active = active
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    # Player class
class Player(basic):
    def __init__(self, screen):
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
        self.hp = 5
        self.image = self.sprites[self.state][self.current_sprite]
        
        super().__init__(self.sprites['walk'][0], 100, 100, True)


    def movement(self):
        key = pygame.key.get_pressed()
        dx = dy = 0
        
        if key[pygame.K_w]:
            dy -= 5
        elif key[pygame.K_s]:
            dy +=5
        elif key[pygame.K_a]:
            dx -= 5
        elif key[pygame.K_d]:
            dx += 5
        
        self.rect.x += dx
        self.rect.y += dy
        self.keep_inbounds()

    def keep_inbounds(self):
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > self.width:
            self.rect.right = self.width
        if self.rect.top < 0:
            self.rect.top = 0

        if self.rect.bottom > self.screen.get_height():
            self.rect.bottom = self.screen.get_height()

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
            if self.cat.hp <= 0:
                self.cat.kill()
            return

            # kill bullet if hit screen
        if self.rect.bottom < 0:
            self.kill()
            return
        


    # Cat class
class Cat(basic):
    def __init__(self, x, y, image, screen):
        super().__init__(image, x, y, True)
        
        self.hp = 9
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()

        self.sprites = {'walk':[pygame.image.load('imgs/cat/walk1.png'),
                                pygame.image.load('imgs/cat/walk2.png'),
                                pygame.image.load('imgs/cat/walk3.png'),
                                pygame.image.load('imgs/cat/walk4.png'),
                                pygame.image.load('imgs/cat/walk5.png'),
                                pygame.image.load('imgs/cat/walk6.png'),
                                  ],
                        'attack':[pygame.image.load('imgs/cat/atk1.png'),
                                  pygame.image.load('imgs/cat/atk2.png'),
                                  pygame.image.load('imgs/cat/atk3.png'),
                                  pygame.image.load('imgs/cat/atk4.png'),
                                  pygame.image.load('imgs/cat/atk5.png'),
                                  pygame.image.load('imgs/cat/atk6.png'),
                                  ]
                        }
        self.state = 'walk'
        self.current_sprite = 0
        self.move = x

    def action(self, cat_atk):
        action = random.randint(1,2)
        if action == 1:
            self.movement()
        else:
            self.attack(cat_atk)

    def movement(self):
        self.state = 'walk'

        if self.rect.x == self.move:
            self.move = random.randint(0, self.width - self.rect.width)

        if self.rect.x < self.move:
            self.rect.x = min(self.rect.x + 5, self.move)
        elif self.rect.x > self.move:
            self.rect.x = max(self.rect.x - 5, self.move)

        self.keep_inbounds()

    def keep_inbounds(self):
        if self.rect.left < 0:
            self.rect.left = 0

        if self.rect.right > self.width:
            self.rect.right = self.width

    def attack(self, cat_atk):
        self.state = 'attack'

        if cat_atk.finished: 
            self.atk = random.randint(1,2)
        
            if self.atk == 1:
                cat_atk.atk_paw()
            else:
                cat_atk.atk_scratch()

    def update(self):
        frames = self.sprites[self.state]

        if frames:
            self.current_sprite += 0.25
            if int(self.current_sprite) >= len(frames):
                self.current_sprite = 0

            self.image = frames[int(self.current_sprite)]
        self.keep_inbounds()

    # Cat attack class
class Cat_attack:
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
        '''scratch'''
            # Changes state for animation
        self.state = 'scratch'

        # Set atk
        self.width = 100
        self.height = 120
        self.warn = 1200
        self.atk = 600
        self.do_atk()

    
    def atk_paw(self):
        '''paw'''
            # Changes state for animation
        self.state = 'paw'

        # Set atk 
        self.width = 100
        self.height = 200
        self.warn = 1500
        self.atk = 600
        self.do_atk()
    
    def do_atk(self):
            # Keeping in bounds
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()
        x = random.randint(0, screen_width - self.width)
        y = random.randint(0, screen_height - self.height)

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

        if time_passed < self.warn:
            pygame.draw.rect(self.screen, (255,0,0), self.hitbox, 3)

        elif time_passed < self.warn + self.atk:
            frames = self.sprites[self.state]
            self.current_sprite += 0.25

            if int(self.current_sprite) >= len(frames):
                self.current_sprite = 0
        
            self.image = frames[int(self.current_sprite)]
            self.screen.blit(self.image, self.hitbox.topleft)

            if self.hit_player == False and self.hitbox.colliderect(self.player.rect):
                self.player.hp -= 1
                self.hit_player = True
        else:
            self.finished = True
            return
