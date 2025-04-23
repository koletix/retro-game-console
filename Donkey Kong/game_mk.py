import os
import pygame
import json
import random

##################################################
#                   CONSTANTS
##################################################

LEVEL_PATH = "levels/"          # Levels relative directory
FPS = 60                        # Frames per second
ASPECT_RATIO = (4, 3)           # Screen Aspect Ratio

# Platform parameters 
PLATFORM_LINE_WIDTH = 7
PLATFORM_COLOR = (225, 51, 129)

# Ladder parameters
LADDER_LINE_WIDTH = 3
LADDER_COLOR = 'light blue'
LADDER_HEIGHT = 0.6

INITIAL_LIVES = 5
MAX_LEVEL_NUM = 1

##################################################
#     IMPORTING LEVEL PLATFORMS AND LADDERS
##################################################

def import_level(i):
    # Opening json file
    f = open(LEVEL_PATH + "level" + str(i) + ".json")

    data = json.load(f)
    ladders = None
    if "ladder" in data:
        ladders = data["ladder"]

    platforms = None
    if "platforms" in data:
        platforms = data["platforms"]

    # Closing file
    f.close()

    return ladders, platforms

def run_mk():
    USE_GAME_SOUND = False
    USE_GAME_CONTROLLER = True
    
    if USE_GAME_SOUND:
        pygame.mixer.init()
        music = pygame.mixer.music.load(os.path.join('assets/Sound/', 'bg.mp3'))
        pygame.mixer.music.play(-1)

    if USE_GAME_CONTROLLER:
        pygame.joystick.init()
        joystick_count = pygame.joystick.get_count()
        print(f"Number of joysticks connected: {joystick_count}")

        if joystick_count > 0:
            joystick = pygame.joystick.Joystick(0) # Use 0 for the first joystick
            joystick.init()
            print(f"Joystick name: {joystick.get_name()}")
        else:
            print("No joystick found. Switching to Keyboard")
            USE_GAME_CONTROLLER = False

    ##################################################
    #             FORMATTING THE SCREEN
    ##################################################
    # Screen Size Info
    info = pygame.display.Info() 
    screen_width, screen_height = info.current_w, info.current_h

    # Calculating Game Screen Size. Aspect Ratio 4 : 3
    height_percent = screen_height // 10
    window_width, window_height = (screen_height - height_percent) * ASPECT_RATIO[0] // ASPECT_RATIO[1] , screen_height - height_percent
    pygame.display.set_caption('Donkey Kong Jose!')
    screen = pygame.display.set_mode([window_width, window_height])

    ##################################################
    #             GAME GLOBAL VARIABLES
    ##################################################

    font_big = pygame.font.Font('freesansbold.ttf', 50)
    font_small = pygame.font.Font('freesansbold.ttf', 30)
    timer = pygame.time.Clock()

    section_width = window_width // 32
    section_height = window_height // 32
    slope = section_height // 8

    barrel_throw_period = 360
    barrel_count = barrel_throw_period / 2
    first_flame = False
    barrel_time = 360
    fireball_trigger = False

    score = 0
    high_score = 0
    lives = INITIAL_LIVES
    bonus = 6000
    bonus_dec = 50
    reset_game = False
    playing_level = 1

    bonus_counter = 0
    bonus_counter_max = 100

    ##################################################
    #             LOADING GAME IMAGES
    ##################################################
    peach1 = pygame.transform.scale(pygame.image.load('assets/images/peach/peach1.png'),
                                    (2 * section_width, 3 * section_height))
    peach2 = pygame.transform.scale(pygame.image.load('assets/images/peach/peach2.png'),
                                    (2 * section_width, 3 * section_height))
    oil_img = pygame.transform.scale(pygame.image.load('assets/images/OilDrum.png'),
                                    (2 * section_width, 3 * section_height))
    barrel1 = pygame.transform.scale(pygame.image.load('assets/images/barrels/barrel1.png'),
                                        (section_width * 1.5, section_height * 2))
    barrel2 = pygame.transform.scale(pygame.image.load('assets/images/barrels/barrel2.png'),
                                        (section_width * 2, section_height * 2.5))
    barrel_side = pygame.transform.scale(pygame.image.load('assets/images/barrels/barrel2.png'),
                                        (section_width * 2, section_height * 2.5))
    dk1 = pygame.transform.scale(pygame.image.load('assets/images/dk/dk1.png'),
                                (section_width * 5, section_height * 5))
    dk2 = pygame.transform.scale(pygame.image.load('assets/images/dk/dk2.png'),
                                (section_width * 5, section_height * 5))
    dk3 = pygame.transform.scale(pygame.image.load('assets/images/dk/dk3.png'),
                                (section_width * 5, section_height * 5))
    standing = pygame.transform.scale(pygame.image.load('assets/images/mario/standing.png'),
                                    (2 * section_width, 2.5 * section_height))
    standing = pygame.transform.flip(standing,True,False)
    jumping = pygame.transform.scale(pygame.image.load('assets/images/mario/jumping.png'),
                                    (2 * section_width, 2.5 * section_height))
    jumping = pygame.transform.flip(jumping,True,False)
    running = pygame.transform.scale(pygame.image.load('assets/images/mario/running.png'),
                                    (2 * section_width, 2.5 * section_height))
    climbing = pygame.transform.scale(pygame.image.load('assets/images/mario/climbing.png'),
                                    (2 * section_width, 2.5 * section_height))
    hammer_alone = pygame.transform.scale(pygame.image.load('assets/images/Hammer.png'),
                                    (2 * section_width, 2 * section_height))
    hammer_jump = pygame.transform.scale(pygame.image.load('assets/images/mario/hammer_jump.png'),
                                        (2.5 * section_width, 2.5 * section_height))
    hammer_overhead = pygame.transform.scale(pygame.image.load('assets/images/mario/hammer_overhead.png'),
                                            (2.5 * section_width, 3.5 * section_height))
    fireball = pygame.transform.scale(pygame.image.load('assets/images/Fireball.png'),
                                    (1.5 * section_width, 2 * section_height))

    def get_row_position(i):
        return window_height - 2 * section_height - 4 * (i - 1) * section_height

    ladders, platforms = import_level(1)  
    if ladders == None or platforms == None:
        raise Exception("Error:  Ladders and/or Platforms missing from level json file.")

    ##################################################
    #             MAIN CLASSES
    ##################################################

    class Platform:
        def __init__(self, row, col, slope_mult, length):
            self.x_pos = col * section_width
            self.y_pos = get_row_position(row) + slope_mult * slope
            self.length = length
            self.top = pygame.rect.Rect((self.x_pos, self.y_pos), (self.length * section_width, 2))

        def draw(self):
            for i in range(self.length):
                bot_coord = self.y_pos + section_height
                left_coord = self.x_pos + (section_width * i)
                mid_coord = left_coord + (section_width * 0.5)
                right_coord = left_coord + section_width
                top_coord = self.y_pos
                # draw 4 lines, top, bot, left diag, right diag
                pygame.draw.line(screen, PLATFORM_COLOR, (left_coord, top_coord),
                                (right_coord, top_coord), PLATFORM_LINE_WIDTH)
                pygame.draw.line(screen, PLATFORM_COLOR, (left_coord, bot_coord),
                                (right_coord, bot_coord), PLATFORM_LINE_WIDTH)
                pygame.draw.line(screen, PLATFORM_COLOR, (left_coord, bot_coord),
                                (mid_coord, top_coord), PLATFORM_LINE_WIDTH)
                pygame.draw.line(screen, PLATFORM_COLOR, (mid_coord, top_coord),
                                (right_coord, bot_coord), PLATFORM_LINE_WIDTH)
            # get the top platform 'surface'
            top_line = pygame.rect.Rect((self.x_pos, self.y_pos), (self.length * section_width, 2))
            # pygame.draw.rect(screen, 'blue', top_line)
            return top_line

    ##################################################

    class Ladder:
        def __init__(self, row, col, slope_mult, length):
            self.x_pos = col * section_width
            self.y_pos = get_row_position(row) + slope_mult * slope
            self.length = length
            self.body = pygame.rect.Rect((self.x_pos, self.y_pos - section_height),
                                    (section_width, (LADDER_HEIGHT * self.length * section_height + section_height)))

        def draw(self):

            for i in range(self.length):
                top_coord = self.y_pos + LADDER_HEIGHT * section_height * i
                bot_coord = top_coord + LADDER_HEIGHT * section_height
                mid_coord = (LADDER_HEIGHT / 2) * section_height + top_coord
                left_coord = self.x_pos
                right_coord = left_coord + section_width
                pygame.draw.line(screen, LADDER_COLOR, (left_coord, top_coord), (left_coord, bot_coord), LADDER_LINE_WIDTH)
                pygame.draw.line(screen, LADDER_COLOR, (right_coord, top_coord), (right_coord, bot_coord), LADDER_LINE_WIDTH)
                pygame.draw.line(screen, LADDER_COLOR, (left_coord, mid_coord), (right_coord, mid_coord), LADDER_LINE_WIDTH)
            body = pygame.rect.Rect((self.x_pos, self.y_pos - section_height),
                                    (section_width, (LADDER_HEIGHT * self.length * section_height + section_height)))
            return body

    ##################################################

    class Mario(pygame.sprite.Sprite):
        def __init__(self, x_pos, y_pos):
            pygame.sprite.Sprite.__init__(self)
            self.landed = True                      # True walking, False jumping
            self.pos = 0                            # 0-1 position climbing
            self.dir = 1                            # 0-1 walking direction
            self.climbing = False                   # climbing or not
            self.image = standing
            self.count = 0
            self.hammer = False
            self.max_hammer = 450
            self.hammer_len = self.max_hammer
            self.hammer_pos = 1
            self.y_change = 0
            self.x_change = 0
            self.x_speed = 3
            self.rect = self.image.get_rect()
            self.hitbox = self.rect
            self.landed = False
            self.hammer_box = self.rect
            self.rect.center = (x_pos, y_pos)
            self.over_barrel = False
            self.bottom = pygame.rect.Rect(self.rect.left, self.rect.bottom - 20, self.rect.width, 20)

        def draw(self):
            if not self.hammer:
                if not self.climbing and self.landed:
                    if self.pos == 0:
                        self.image = standing
                    else:
                        self.image = running
                if not self.landed and not self.climbing:
                    self.image = jumping
                if self.climbing:
                    if self.pos == 0:
                        self.image = climbing
                    else:
                        self.image = pygame.transform.flip(climbing, True, False)

            else:
                if self.hammer_pos == 0:
                    self.image = hammer_jump
                else:
                    self.image = hammer_overhead
            
            if self.dir == -1:
                self.image = pygame.transform.flip(self.image, True, False)

            self.calc_hitbox()
            if self.hammer_pos == 1 and self.hammer:
                screen.blit(self.image, (self.rect.left, self.rect.top - section_height))
            else:
                screen.blit(self.image, self.rect.topleft)


        def calc_hitbox(self):
            if not self.hammer:
                self.hitbox = pygame.rect.Rect((self.rect[0] + 15, self.rect[1] + 5),
                                                (self.rect[2] - 30, self.rect[3] - 10))
            elif self.hammer_pos == 0:
                if self.dir == 1:
                    self.hitbox = pygame.rect.Rect((self.rect[0], self.rect[1] + 5),
                                                    (self.rect[2] - 30, self.rect[3] - 10))
                    self.hammer_box = pygame.rect.Rect((self.hitbox[0] + self.hitbox[2], self.rect[1] + 5),
                                                        (self.hitbox[2], self.rect[3] - 10))
                else:
                    self.hitbox = pygame.rect.Rect((self.rect[0] + 40, self.rect[1] + 5),
                                                    (self.rect[2] - 30, self.rect[3] - 10))
                    self.hammer_box = pygame.rect.Rect((self.hitbox[0] - self.hitbox[2], self.rect[1] + 5),
                                                        (self.hitbox[2], self.rect[3] - 10))
            else:
                self.hitbox = pygame.rect.Rect((self.rect[0] + 15, self.rect[1] + 5),
                                                (self.rect[2] - 30, self.rect[3] - 10))
                self.hammer_box = pygame.rect.Rect((self.hitbox[0], self.hitbox[1] - section_height),
                                                    (self.hitbox[2], section_height))    
        def update(self):
                self.landed = False
                for i in range(len(plats)):
                    if self.bottom.colliderect(plats[i]):
                        self.landed = True
                        if not self.climbing:
                            self.rect.centery = plats[i].top - self.rect.height / 2 + 1
                if not self.landed and not self.climbing:
                    self.y_change += 0.25
                self.rect.move_ip(self.x_change * self.x_speed, self.y_change)
                self.bottom = pygame.rect.Rect(self.rect.left, self.rect.bottom - 20, self.rect.width, 20)
                if self.x_change != 0 or (self.climbing and self.y_change != 0):
                    if self.count < 3:
                        self.count += 1
                    else:
                        self.count = 0
                        if self.pos == 0:
                            self.pos += 1
                        else:
                            self.pos = 0
                else:
                    self.pos = 0
                if self.hammer:
                    self.hammer_pos = (self.hammer_len // 30) % 2
                    self.hammer_len -= 1
                    if self.hammer_len == 0:
                        self.hammer = False
                        self.hammer_len = self.max_hammer
            
    ##################################################
            
    class Hammer(pygame.sprite.Sprite):
        def __init__(self, x_pos, y_pos):
            pygame.sprite.Sprite.__init__(self)
            self.image = hammer_alone
            self.rect = self.image.get_rect()
            self.rect.top = y_pos
            self.rect.left = x_pos * section_width
            self.used = False

        def draw(self):
            if not self.used:
                screen.blit(self.image, (self.rect[0], self.rect[1]))
                if self.rect.colliderect(mario.hitbox):
                    self.kill()
                    mario.hammer = True
                    mario.hammer_len = mario.max_hammer
                    self.used = True

    ##################################################

    class Flame(pygame.sprite.Sprite):
        def __init__(self, x_pos, y_pos):
            pygame.sprite.Sprite.__init__(self)
            self.image = fireball
            self.rect = self.image.get_rect()
            self.rect.center = (x_pos, y_pos)
            self.pos = 1
            self.count = 0
            self.x_count = 0
            self.x_change = 2
            self.x_max = 4
            self.y_change = 0
            self.row = 1
            self.check_lad = False
            self.climbing = False

        def update(self):
            if self.y_change < 3 and not self.climbing:
                self.y_change += 0.25
            for i in range(len(plats)):
                if self.rect.colliderect(plats[i]):
                    self.climbing = False
                    self.y_change = -4
            # if flame collides with players hitbox - trigger reset of the game (also do this to barrels)
            if self.count < 15:
                self.count += 1
            else:
                self.count = 0
                self.pos *= -1
                if self.x_count < self.x_max:
                    self.x_count += 1
                else:  # row 1,3 and 5 - go further right than left overall, otherwise flip it
                    self.x_count = 0
                    if self.x_change > 0:
                        if self.row in [1, 3, 5]:
                            self.x_max = random.randint(3, 6)
                        else:
                            self.x_max = random.randint(6, 10)
                    else:
                        if self.row in [1, 3, 5]:
                            self.x_max = random.randint(6, 10)
                        else:
                            self.x_max = random.randint(3, 6)
                    self.x_change *= -1

            if self.x_change > 0:
                self.image = fireball
            else:
                self.image = pygame.transform.flip(fireball, True, False)

            self.rect.move_ip(self.x_change, self.y_change)
            if self.rect.top > screen_height or self.rect.top < 0:
                self.kill()

        def check_climb(self):
            already_collided = False
            for lad in lads:
                if self.rect.colliderect(lad) and not self.climbing and not self.check_lad:
                    self.check_lad = True
                    already_collided = True
                    if random.randint(0, 120) == 120:
                        self.climbing = True
                        self.y_change = - 4
            if not already_collided:
                self.check_lad = False
            if self.rect.bottom < get_row_position(6):
                self.row = 6
            elif self.rect.bottom < get_row_position(5):
                self.row = 5
            elif self.rect.bottom < get_row_position(4):
                self.row = 4
            elif self.rect.bottom < get_row_position(3):
                self.row = 3
            elif self.rect.bottom < get_row_position(2):
                self.row = 2
            else:
                self.row = 1

    ##################################################

    class Barrel(pygame.sprite.Sprite):
        def __init__(self, x_pos, y_pos):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.Surface((50, 50))
            self.rect = self.image.get_rect()
            self.rect.center = (x_pos, y_pos)
            self.y_change = 0
            self.x_change = 1
            self.pos = 0
            self.count = 0
            self.oil_collision = False
            self.falling = False
            self.check_lad = False
            self.bottom = self.rect

        def update(self, fire_trig):
            if self.y_change < 8 and not self.falling:
                barrel.y_change += 2
            for i in range(len(plats)):
                if self.bottom.colliderect(plats[i]):
                    self.y_change = 0
                    self.falling = False
            if self.rect.colliderect(oil_drum):
                if not self.oil_collision:
                    self.oil_collision = True
                    if random.randint(0, 4) == 4:
                        fire_trig = True
            if not self.falling:
                if get_row_position(6) >= self.rect.centery or get_row_position(4) >= self.rect.centery >= get_row_position(5) or get_row_position(2) > self.rect.centery >= get_row_position(3):
                    self.x_change = 3
                else:
                    self.x_change = -3
            else:
                self.x_change = 0
            self.rect.move_ip(self.x_change, self.y_change)
            if self.rect.top > screen_height:
                self.kill()
            if self.count < 15:
                self.count += 1
            else:
                self.count = 0
                if self.x_change > 0:
                    if self.pos < 3:
                        self.pos += 1
                    else:
                        self.pos = 0
                else:
                    if self.pos > 0:
                        self.pos -= 1
                    else:
                        self.pos = 3
            self.bottom = pygame.rect.Rect((self.rect[0], self.rect.bottom), (self.rect[2], 5))
            return fire_trig

        def check_fall(self):
            already_collided = False
            below = pygame.rect.Rect((self.rect[0], self.rect[1] + section_height), (self.rect[2], section_height))
            for lad in lads:
                if below.colliderect(lad) and not self.falling and not self.check_lad:
                    self.check_lad = True
                    already_collided = True
                    if random.randint(0, 60) == 60:
                        self.falling = True
                        self.y_change = 4
            if not already_collided:
                self.check_lad = False

        def draw(self):
            screen.blit(pygame.transform.rotate(barrel1, 90 * self.pos), self.rect.topleft)

    ##################################################
    #             MAIN FUNCTIONS
    ##################################################

    def create_platform_list(platform_level):
        platform_list =[]
        for platform in platform_level:
            p = Platform(platform["row"],platform["col"],platform["slope_mult"],platform["length"])
            platform_list.append(p)
        return platform_list

    ##################################################

    def create_ladder_list(ladder_level):
        ladder_list =[]
        for ladder in ladder_level:
            l = Ladder(ladder["row"],ladder["col"],ladder["slope_mult"],ladder["length"])
            ladder_list.append(l)
        return ladder_list

    ##################################################

    ladder_list = create_ladder_list(ladders)
    platform_list = create_platform_list(platforms)
    target = [10, get_row_position(7), 3]
    all_hammers = [[4, get_row_position(6) + 8*slope], [4, get_row_position(4)+ 5*slope]]

    ##################################################

    def draw_screen():
        # Drawing the platforms
        ladder_climbers = []
        for ladder in ladder_list:
            ladder.draw()
            if ladder.length >= 3:
                ladder_climbers.append(ladder.body)    
                    
        # Drawing the platforms
        platforms = []
        for platform in platform_list:
            platform.draw()
            platforms.append(platform.top)          

        return platforms, ladder_climbers

    ##################################################

    def draw_oil_drum():
        x_coord, y_coord = 4 * section_width, window_height - 4.6 * section_height
        oil = pygame.draw.rect(screen, 'blue', [x_coord, y_coord, 2 * section_width, 2.5 * section_height])
        screen.blit(oil_img, (x_coord, y_coord - section_height))
        return oil

    ##################################################

    def draw_barrels():
        screen.blit(pygame.transform.rotate(barrel2, 90), (section_width * 1.2, 5.4 * section_height))
        screen.blit(pygame.transform.rotate(barrel2, 90), (section_width * 2.5, 5.4 * section_height))
        screen.blit(pygame.transform.rotate(barrel2, 90), (section_width * 2.5, 7.7 * section_height))
        screen.blit(pygame.transform.rotate(barrel2, 90), (section_width * 1.2, 7.7 * section_height))

    ##################################################

    def draw_dk():
        phase_time = barrel_time // 4
        if barrel_throw_period - barrel_count > 3 * phase_time:
            dk_img = dk2
        elif barrel_throw_period - barrel_count > 2 * phase_time:
            dk_img = dk1
        elif barrel_throw_period - barrel_count > phase_time:
            dk_img = dk3
        else:
            dk_img = pygame.transform.flip(dk1, True, False)
            screen.blit(barrel1, (250, 250))
        screen.blit(dk_img, (3.5 * section_width, get_row_position(6) - 5.5 * section_height))

    ##################################################

    def reset(mario, flames, hammers, lives):
        pygame.time.delay(1000)
        for flam in flames:
            flam.kill()
        for h in hammers:
            h.kill()
        for h in all_hammers:
            hammers.add(Hammer(h[0],h[1]))
        lives -= 1
        bonus = 6000
        mario.kill()
        mario = Mario(280, window_height - 100)
        first_flame = False
        barrel_throw_period = 360
        barrel_count = barrel_throw_period / 2
        victory = False
        return mario, flames, hammers, lives, first_flame, victory, bonus, barrel_throw_period, barrel_count

    ##################################################

    def draw_misc():  
        # Menu Screen
        # put lives, levels, bonus text etc in here
        screen.blit(font_big.render(f'I•{score:06}', True, 'white'), (3*section_width, 2*section_height))
        screen.blit(font_big.render(f'TOP•{high_score}', True, 'white'), (14 * section_width, 2 * section_height))
        screen.blit(font_big.render(f'[  ][        ][  ]', True, 'white'), (20 * section_width, 4 * section_height))
        screen.blit(font_small.render(f'  M    BONUS     L ', True, 'white'), (20 * section_width + 5, 4 * section_height))
        screen.blit(font_small.render(f'  {lives}       {bonus}        {playing_level}  ', True, 'white'),
                    (20 * section_width + 5, 5 * section_height))
        # drawing peach
        if barrel_count < barrel_throw_period / 2:
            screen.blit(peach1, (10 * section_width, get_row_position(7) - 3 * section_height))
        else:
            screen.blit(peach2, (10 * section_width, get_row_position(7) - 3 * section_height))

        # drawing oil drum
        oil = draw_oil_drum()

        # drawing barrels
        draw_barrels()

        # drawing dk
        draw_dk()

        return oil

    ##################################################

    def can_move_vert():
        can_climb_up = False
        can_climb_down = False
        under = pygame.rect.Rect((mario.rect[0], mario.rect[1] + 2 * section_height), (mario.rect[2], mario.rect[3]))
        for lad in lads:
            if mario.hitbox.colliderect(lad) and not can_climb_up:
                can_climb_up = True
            if under.colliderect(lad):
                can_climb_down = True
        if (not can_climb_up and (not can_climb_down or mario.y_change < 0)) or \
                (mario.landed and can_climb_up and mario.y_change > 0 and not can_climb_down):
            mario.climbing = False
        return can_climb_up, can_climb_down

    ##################################################

    def barrel_collide(reset, score):
        under = pygame.rect.Rect((mario.rect[0], mario.rect[1] + 2 * section_height), (mario.rect[2], mario.rect[3]))
        for brl in barrels:
            if brl.rect.colliderect(mario.hitbox):
                reset = True
            elif not mario.landed and not mario.over_barrel and under.colliderect(brl):
                mario.over_barrel = True
                score += 100
        if mario.landed:
            mario.over_barrel = False

        return reset, score

    ##################################################

    def victory_cry():
        target_rect = pygame.rect.Rect((target[0]*section_width, target[1]), (section_width*target[2], 1))
        return mario.bottom.colliderect(target_rect)

    ##################################################

    hammers = pygame.sprite.Group()
    for h in all_hammers:
        hammers.add(Hammer(h[0],h[1]))
    mario = Mario(280, window_height - 100)
    flames = pygame.sprite.Group()
    barrels = pygame.sprite.Group()

    ##################################################
    #                   Main Loop 
    ##################################################
    run = True
    while run:
        screen.fill('black')
        timer.tick(FPS)

        if bonus_counter < bonus_counter_max:
            bonus_counter += 1
        else:
            bonus_counter = 0
            if bonus >= bonus_dec:
                bonus -= bonus_dec
            else:
                bonus = 0

        # draw the platforms and ladders
        plats, lads = draw_screen()

        # draw the miscelaneous objects
        oil_drum = draw_misc()

        up,down = can_move_vert()
        victory = victory_cry()

        if barrel_count < barrel_throw_period:
            barrel_count += 1
        else:
            barrel_count = random.randint(0, 40)
            barrel_time = barrel_throw_period - barrel_count
            barrel = Barrel(270, 270)
            barrels.add(barrel)
            if not first_flame:
                flame = Flame(5*section_width, window_height - 4*section_height)
                flames.add(flame)
                first_flame = True
        
        for barrel in barrels:
            barrel.draw()
            barrel.check_fall()
            fireball_trigger = barrel.update(fireball_trigger)
            if barrel.rect.colliderect(mario.hammer_box) and mario.hammer:
                barrel.kill()
                score += 500

        for flame in flames:
            flame.check_climb()
            if flame.rect.colliderect(mario.hitbox):
                reset_game = True  
                
        # Updating and drawing flames
        flames.draw(screen)
        flames.update()  

        # Updating and drawing Mario
        mario.update()
        mario.draw()

        # Drawing the barrels
        for h in hammers:
            h.draw()

        reset_game, score = barrel_collide(reset_game, score)
        if reset_game:
            if lives > 0:
                # U have more lives.  Play again!!!!
                mario, flames, hammers, lives, \
                first_flame, victory, bonus, \
                barrel_throw_period, barrel_count = reset(mario, flames, hammers, lives)
                reset_game = False
            else:
                # Live over.  U loose!!!!
                run = False
        
        # Getting the events.  KEYBOARD SO FAR

        for event in pygame.event.get():
            if USE_GAME_CONTROLLER:
                #####################################           
                #           CONTROLLER
                #####################################                                
                if event.type == pygame.JOYBUTTONDOWN:
                    button = event.button
                    if button == 1 and mario.landed:
                        mario.landed = False
                        mario.y_change = -6
                    if button == 2:
                        run = False
                if event.type == pygame.JOYBUTTONUP:
                    button = event.button
                    print(f"Button {button} released")
                if event.type == pygame.JOYHATMOTION:
                    hat = event.hat
                    value = event.value
                    print(f"Hat {hat} moved to {value}")
                    if hat == 0:
                        if value[0] == 1 and value[1] == 0 and not mario.climbing:
                            mario.x_change = 1
                            mario.dir = 1
                        if value[0] == -1 and value[1] == 0 and not mario.climbing:
                            mario.x_change = -1
                            mario.dir = -1
                        if value[0] == 0 and value[1] == 1:
                            if up:
                                mario.y_change = -2
                                mario.x_change = 0
                                mario.climbing = True
                        if value[0] == 0 and value[1] == -1:
                            if down:
                                mario.y_change = 2
                                mario.x_change = 0
                                mario.climbing = True        
                        if value[0] == 0 and value[1] == 0:
                            mario.x_change = 0   
                            if up:
                                mario.y_change = 0
                            if mario.climbing and mario.landed:
                                mario.climbing = False
            else:
                #####################################           
                #           KEYBOARD
                #####################################  
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT and not mario.climbing:
                        mario.x_change = 1
                        mario.dir = 1
                    if event.key == pygame.K_LEFT and not mario.climbing:
                        mario.x_change = -1
                        mario.dir = -1
                    if event.key == pygame.K_SPACE and mario.landed:
                        mario.landed = False
                        mario.y_change = -6
                    if event.key == pygame.K_UP:
                        if up:
                            mario.y_change = -2
                            mario.x_change = 0
                            mario.climbing = True
                    if event.key == pygame.K_DOWN:
                        if down:
                            mario.y_change = 2
                            mario.x_change = 0
                            mario.climbing = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT:
                        mario.x_change = 0
                    if event.key == pygame.K_LEFT:
                        mario.x_change = 0
                    if event.key == pygame.K_UP:
                        if up:
                            mario.y_change = 0
                        if mario.climbing and mario.landed:
                            mario.climbing = False
                    if event.key == pygame.K_DOWN:
                        if up:
                            mario.y_change = 0
                        if mario.climbing and mario.landed:
                            mario.climbing = False
        if victory:
            # U win!!!!!
            screen.blit(font_big.render('VICTORY!', True, 'white'), (window_width/2, window_height/2))
            reset_game = True
            score += bonus

            if score > high_score:
                high_score = score
            
            score = 0
            mario.climbing = False

            if playing_level < MAX_LEVEL_NUM:
                playing_level += 1
            else:
                playing_level = 1        

        pygame.display.flip()

if __name__ == "__main__":
    os.environ['SDL_VIDEO_CENTERED'] = '1' 
    pygame.init()
    run_mk()
    pygame.quit()