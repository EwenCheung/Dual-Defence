# coding: utf-8

import pygame
from sys import exit
from random import randint, choice
from Database import database


# game start from here
# have to initialise the pygame first
# pygame.init()
# pygame.font.init()
# pygame.display.set_caption('Pokemon vs Naruto')  # title name
# pygame.display.set_mode((1000, 600))


class Tools:
    def find_grid_coor(self, pos, grid_coor, num_ball, hero_type):
        # check whether out of map
        # 312 - 42 = 272 ( least x ) , 927 + 42 = 967 ( max x )
        # 172 - 45 = 127 ( least y ) , 532 + 45 = 577 ( max x )
        if pos[0] < 272 or pos[0] > 967 or pos[1] < 127 or pos[1] > 577:
            return None

        if hero_type == 'machine':
            if num_ball < 50:
                return None
        elif hero_type == 'archer':
            if num_ball < 150:
                return None
        elif hero_type == 'wizard':
            if num_ball < 100:
                return None

        # check at which column (finding coordinate x)
        for i, column in enumerate(grid_coor):
            # cause our grid_coor is center so use + and - to get the max result
            if grid_coor[i][0][0] - 42 <= pos[0] and grid_coor[i][0][0] + 42 >= pos[0]:
                # check at which row (finding coordinate y), will output the coor for x and y
                for coor in column:
                    if coor[1] - 45 <= pos[1] and coor[1] + 45 >= pos[1]:
                        if coor[2] == 1:
                            return None
                        elif coor[2] == 0:
                            coor[2] = 1
                            return (coor[0], coor[1])  # return coordinate where hero have to stay


class Gem_Ball:
    def __init__(self):
        self.gem_ball_surface = pygame.image.load('Bokemon vs Stick/Picture/utils/diamond_ball.png').convert_alpha()
        self.gem_ball_surface = pygame.transform.scale(self.gem_ball_surface, (50, 50))
        self.gem_ball_rect_storage = []

    def create_gem_ball(self):
        gem_ball_rectangle = self.gem_ball_surface.get_rect(center=(randint(312, 927), randint(-250, -100)))
        self.gem_ball_rect_storage.append(gem_ball_rectangle)

    def drop_gem_ball(self):
        for gem_ball_rect in self.gem_ball_rect_storage:
            # dropping from up and stop at bottom
            if gem_ball_rect.y < 535:
                gem_ball_rect.y += 0.6  # speed cannot below 0.6


# load hero frame
machine_frame = [
                    pygame.image.load('Bokemon vs Stick/Picture/machine/machine_1.png').convert_alpha() for _ in
                    range(30)] + [pygame.image.load('Bokemon vs Stick/Picture/machine/machine_2.png').convert_alpha()
                                  ]

wizard_normal = [pygame.image.load('Bokemon vs Stick/Picture/wizard/wizard_1.png').convert_alpha(),
                 pygame.image.load('Bokemon vs Stick/Picture/wizard/wizard_2.png').convert_alpha()]

archer_normal = [pygame.image.load('Bokemon vs Stick/Picture/archer/archer_1.png').convert_alpha(),
                 pygame.image.load('Bokemon vs Stick/Picture/archer/archer_2.png').convert_alpha()]

wizard_attack = [pygame.image.load('Bokemon vs Stick/Picture/wizard/wizard_3.png').convert_alpha(),
                 pygame.image.load('Bokemon vs Stick/Picture/wizard/wizard_4.png').convert_alpha(),
                 pygame.image.load('Bokemon vs Stick/Picture/wizard/wizard_5.png').convert_alpha()]

archer_attack = [pygame.image.load('Bokemon vs Stick/Picture/archer/archer_attack_1.png').convert_alpha(),
                 pygame.image.load('Bokemon vs Stick/Picture/archer/archer_attack_2.png').convert_alpha(),
                 pygame.image.load('Bokemon vs Stick/Picture/archer/archer_attack_3.png').convert_alpha(),
                 pygame.image.load('Bokemon vs Stick/Picture/archer/archer_attack_4.png').convert_alpha(),
                 pygame.image.load('Bokemon vs Stick/Picture/archer/archer_attack_5.png').convert_alpha(),
                 pygame.image.load('Bokemon vs Stick/Picture/archer/archer_attack_6.png').convert_alpha(), ]


class Hero(pygame.sprite.Sprite):
    # hero
    def __init__(self, hero_type, placing_coordinate):
        super().__init__()

        self.hero_type = hero_type
        self.placing_coordinate = placing_coordinate

        if self.hero_type == 'machine':
            self.normal_frames = [pygame.transform.scale(frame, (70, 82)) for frame in machine_frame]
            self.health = 300
        elif self.hero_type == 'archer':
            self.attack_frames = [pygame.transform.scale(frame, (75, 82)) for frame in archer_attack]
            self.normal_frames = [pygame.transform.scale(frame, (75, 82)) for frame in archer_normal]
            self.health = 180
            self.bullet_speed = 5
        elif self.hero_type == 'wizard':
            self.attack_frames = [pygame.transform.scale(frame, (75, 82)) for frame in wizard_attack]
            self.normal_frames = [pygame.transform.scale(frame, (75, 82)) for frame in wizard_normal]
            self.health = 200
            self.bullet_speed = 4
        else:
            print('No hero found')

        self.frames = self.normal_frames
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(center=(self.placing_coordinate))

        self.archer_bullet_surface = pygame.image.load('Bokemon vs Stick/Picture/archer/archer_bullet.png').convert_alpha()
        self.archer_bullet_surface = pygame.transform.scale(self.archer_bullet_surface, (50, 10))

        self.wizard_bullet_surface = pygame.image.load('Bokemon vs Stick/Picture/wizard/wizard_bullet.png').convert_alpha()
        self.wizard_bullet_surface = pygame.transform.scale(self.wizard_bullet_surface, (20, 20))

        self.machine_ball_surface = pygame.image.load('Bokemon vs Stick/Picture/utils/diamond_ball.png').convert_alpha()
        self.machine_ball_surface = pygame.transform.scale(self.machine_ball_surface, (25, 25))

        # this list will store all active bullet
        self.bullet_rect_storage = []

    def change_mode(self, mode):
        if self.hero_type == 'archer' or self.hero_type == 'wizard':
            if mode == 'attacking':
                self.frames = self.attack_frames
            if mode == 'normal':
                self.frames = self.normal_frames

    def update_animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            # Only create bullets when in attacking mode (or machine type which always shoots)
            if self.hero_type == 'machine' or self.frames == self.attack_frames:
                self.create_bullet()
            self.animation_index = 0

        self.image = self.frames[int(self.animation_index)]

    def create_bullet(self):
        # bullet created append into the list
        if self.hero_type == 'archer':
            new_bullet = self.archer_bullet_surface.get_rect(center=self.rect.center)
        elif self.hero_type == 'wizard':
            new_bullet = self.wizard_bullet_surface.get_rect(center=self.rect.center)
        elif self.hero_type == 'machine':
            new_bullet = self.machine_ball_surface.get_rect(
                center=((self.rect.bottomright[0] + randint(-15, 15)), ((self.rect.bottomright[1] + randint(-15, 15)))))
        self.bullet_rect_storage.append(new_bullet)

    def move_bullet(self):
        for bullet_rect in self.bullet_rect_storage[:]:  # Use slice copy to avoid modification during iteration
            bullet_rect.x += self.bullet_speed  # Move the bullet to the right
            if bullet_rect.x > 1030:
                # Remove bullets that have moved off-screen
                self.bullet_rect_storage.remove(bullet_rect)

    def update(self):
        self.update_animation_state()


# load enemy image
warrior_1_image = [
    pygame.image.load('Bokemon vs Stick/Picture/enemy_one/enemy_one_1.png').convert_alpha(),
    pygame.image.load('Bokemon vs Stick/Picture/enemy_one/enemy_one_2.png').convert_alpha(),
    pygame.image.load('Bokemon vs Stick/Picture/enemy_one/enemy_one_3.png').convert_alpha(),
    pygame.image.load('Bokemon vs Stick/Picture/enemy_one/enemy_one_4.png').convert_alpha()]

warrior_2_image = [
    pygame.image.load('Bokemon vs Stick/Picture/enemy_two/enemy_two_1.png').convert_alpha(),
    pygame.image.load('Bokemon vs Stick/Picture/enemy_two/enemy_two_2.png').convert_alpha(),
    pygame.image.load('Bokemon vs Stick/Picture/enemy_two/enemy_two_3.png').convert_alpha(),
    pygame.image.load('Bokemon vs Stick/Picture/enemy_two/enemy_two_4.png').convert_alpha()]

warrior_3_image = [
    pygame.image.load('Bokemon vs Stick/Picture/enemy_three/enemy_three_1.png').convert_alpha(),
    pygame.image.load('Bokemon vs Stick/Picture/enemy_three/enemy_three_2.png').convert_alpha(),
    pygame.image.load('Bokemon vs Stick/Picture/enemy_three/enemy_three_3.png').convert_alpha(),
    pygame.image.load('Bokemon vs Stick/Picture/enemy_three/enemy_three_4.png').convert_alpha(),
    pygame.image.load('Bokemon vs Stick/Picture/enemy_three/enemy_three_5.png').convert_alpha()]

# load enemy attack image
warrior_1_attack = [
    pygame.image.load('Bokemon vs Stick/Picture/enemy_one/enemy_one_attack_1.png').convert_alpha(),
    pygame.image.load('Bokemon vs Stick/Picture/enemy_one/enemy_one_attack_2.png').convert_alpha(),
    pygame.image.load('Bokemon vs Stick/Picture/enemy_one/enemy_one_attack_3.png').convert_alpha(),
    pygame.image.load('Bokemon vs Stick/Picture/enemy_one/enemy_one_attack_4.png').convert_alpha()]

warrior_2_attack = [
    pygame.image.load('Bokemon vs Stick/Picture/enemy_two/enemy_two_attack_1.png').convert_alpha(),
    pygame.image.load('Bokemon vs Stick/Picture/enemy_two/enemy_two_attack_2.png').convert_alpha(),
    pygame.image.load('Bokemon vs Stick/Picture/enemy_two/enemy_two_attack_3.png').convert_alpha(),
    pygame.image.load('Bokemon vs Stick/Picture/enemy_two/enemy_two_attack_4.png').convert_alpha()]

warrior_3_attack = [
    pygame.image.load('Bokemon vs Stick/Picture/enemy_three/enemy_three_attack_1.png').convert_alpha(),
    pygame.image.load('Bokemon vs Stick/Picture/enemy_three/enemy_three_attack_2.png').convert_alpha(),
    pygame.image.load('Bokemon vs Stick/Picture/enemy_three/enemy_three_attack_3.png').convert_alpha(),
    pygame.image.load('Bokemon vs Stick/Picture/enemy_three/enemy_three_attack_4.png').convert_alpha(),
    pygame.image.load('Bokemon vs Stick/Picture/enemy_three/enemy_three_attack_5.png').convert_alpha()]


class Troop(pygame.sprite.Sprite):
    # load image

    def __init__(self, troop_type, all_grid_coor):
        super().__init__()

        self.troop_type = troop_type
        self.all_grid_coor = all_grid_coor

        if troop_type == 'warrior':
            self.frames = [pygame.transform.scale(frame, (75, 110)) for frame in warrior_1_image]
            self.frame = [pygame.transform.scale(frame, (75, 110)) for frame in warrior_1_attack]
            self.speed = 1
            self.health = 120
            self.attack = 20
            self.cooldown = 0
        elif troop_type == 'sparta':
            self.frames = [pygame.transform.scale(frame, (75, 82)) for frame in warrior_2_image]
            self.frame = [pygame.transform.scale(frame, (75, 82)) for frame in warrior_2_attack]
            self.speed = 1
            self.health = 110
            self.attack = 25
            self.cooldown = 0
        elif troop_type == 'giant':
            self.frames = [pygame.transform.scale(frame, (75, 82)) for frame in warrior_3_image]
            self.frame = [pygame.transform.scale(frame, (75, 82)) for frame in warrior_3_attack]
            self.speed = 1
            self.health = 110
            self.attack = 25
            self.cooldown = 0
        else:
            print('No ninja found')

        self.original_speed = self.speed

        # spawn at these position
        self.spawn_y = choice([172, 262, 352, 442, 532])
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(center=(randint(1100, 2000), self.spawn_y))

        self.animation_attack_index = 0
        self.image = self.frame[self.animation_attack_index]

    def update_animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def animation_attack_state(self):
        self.animation_attack_index += 0.1
        if self.animation_attack_index >= len(self.frame):
            self.animation_attack_index = 0
        self.image = self.frame[int(self.animation_attack_index)]

    def update(self, hero_groups):
        self.update_animation_state()

        if self.cooldown > 0:
            self.cooldown -= 1

        self.rect.x -= self.speed

        collisions = pygame.sprite.spritecollide(self, hero_groups, False)
        if collisions:
            self.speed = 0
            self.animation_attack_state()
            if self.cooldown == 0:
                for hero in collisions:
                    hero.health -= self.attack

                    self.cooldown = 60
                    if hero.health <= 0:
                        coor_with_1 = []
                        for column in self.all_grid_coor:
                            for coor in column:
                                if coor[2] == 1:
                                    coor_with_1.append(coor)
                                    if [hero.rect.centerx, hero.rect.centery, 1] in coor_with_1:
                                        coor[2] = 0
                        hero.kill()
                        self.speed = self.original_speed
        else:
            self.speed = self.original_speed

    def troop_being_attack(self, damage):
        self.health -= damage

    def check_troop_die(self):
        if self.health <= 0:
            self.kill()
            return True


class GamePokemonVsStick:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((1000, 600))  # screen size
        self.machine_card_initial_position = (120, 8)
        self.archer_card_initial_position = (191, 8)
        self.wizard_card_initial_position = (262, 8)
        self.reset_func()

    def reset_func(self):
        self.before_press_start = True  # main menu
        self.after_press_start = False  # game start
        self.begin_time = None

        # Groups
        self.troop_groups = pygame.sprite.Group()
        self.hero_groups = pygame.sprite.Group()

        # reset game state for play again
        self.reset_game_state()

        # set up gem_ball_drop_timer
        self.gem_ball_timer = pygame.USEREVENT + 2
        pygame.time.set_timer(self.gem_ball_timer, 16000)

        # choice of ninja
        self.troop_choice = ['warrior', 'sparta', 'giant']

    def reset_game_state(self):

        # set up Ninja timer
        self.troop_timer = pygame.USEREVENT + 1
        self.spawn_time = 8000
        pygame.time.set_timer(self.troop_timer, self.spawn_time)

        self.num_ball = 500
        self.chosen_hero = None
        self.coordinate = None
        self.remaining_time = None
        self.help_menu_page = None
        self.lose = False
        self.wave = 1
        # center coordinate for each box
        # x = [312, 400, 486, 577, 663, 750, 838, 927]
        # y = [172, 262, 352, 442, 532]
        # grid_coor [0] is x_coor , [1] is y_coor , [2] is the grid been taken
        self.grid_coor = [
            [[312, 172, 0], [312, 262, 0], [312, 352, 0], [312, 442, 0], [312, 532, 0]],
            [[400, 172, 0], [400, 262, 0], [400, 352, 0], [400, 442, 0], [400, 532, 0]],
            [[486, 172, 0], [486, 262, 0], [486, 352, 0], [486, 442, 0], [486, 532, 0]],
            [[577, 172, 0], [577, 262, 0], [577, 352, 0], [577, 442, 0], [577, 532, 0]],
            [[663, 172, 0], [663, 262, 0], [663, 352, 0], [663, 442, 0], [663, 532, 0]],
            [[750, 172, 0], [750, 262, 0], [750, 352, 0], [750, 442, 0], [750, 532, 0]],
            [[838, 172, 0], [838, 262, 0], [838, 352, 0], [838, 442, 0], [838, 532, 0]],
            [[927, 172, 0], [927, 262, 0], [927, 352, 0], [927, 442, 0], [927, 532, 0]]
        ]
        self.tools = Tools()
        self.spawned_ball = Gem_Ball()
        self.troop_groups.empty()
        self.hero_groups.empty()

        self.go_home_py = False
        self.set_up()  # set up surface and rectangle etc

    def set_up(self):  # set up surface and rectangle etc
        # main menu surface and rect
        self.welcome_surface = pygame.image.load('Bokemon vs Stick/Picture/utils/welcome.jpg').convert()
        self.welcome_surface = pygame.transform.scale(self.welcome_surface, (1000, 600))

        self.start_adventure_surface = pygame.image.load('Bokemon vs Stick/Picture/utils/white_screen.jpeg').convert()
        self.start_adventure_surface = pygame.transform.scale(self.start_adventure_surface, (410, 100))
        self.start_adventure_rect = self.start_adventure_surface.get_rect(topleft=(510, 70))

        username_font = pygame.font.Font(None, 30)
        self.username_surface = username_font.render(database.username, True, 'Green')
        self.username_rectangle = self.username_surface.get_rect(center=(257, 90))

        press_h_font = pygame.font.Font(None, 35)
        self.h_surface = press_h_font.render(("Press 'h' for help menu. You can find guides there"), True, 'White')
        self.h_rectangle = self.h_surface.get_rect(center=(500, 570))

        self.help_menu_font = pygame.font.Font(None, 20)
        # Read the help_menu_file file
        with open("Bokemon vs Stick/Data/help_menu.txt", "r") as file:
            self.help_menu_content = file.read()
        self.help_menu_page = False

        # game start surface and rect
        self.background_surface = pygame.image.load('Bokemon vs Stick/Picture/utils/game_background.png').convert()
        self.background_surface = pygame.transform.scale(self.background_surface, (1000, 600))

        self.machine_card_surface = pygame.image.load('Bokemon vs Stick/Picture/machine/machine_card.png').convert()
        self.machine_card_surface = pygame.transform.scale(self.machine_card_surface, (68, 83))
        self.machine_card_rectangle = self.machine_card_surface.get_rect(topleft=self.machine_card_initial_position)

        self.archer_card_surface = pygame.image.load('Bokemon vs Stick/Picture/archer/archer_card.png').convert()
        self.archer_card_surface = pygame.transform.scale(self.archer_card_surface, (68, 83))
        self.archer_card_rectangle = self.archer_card_surface.get_rect(topleft=self.archer_card_initial_position)

        self.wizard_card_surface = pygame.image.load('Bokemon vs Stick/Picture/wizard/wizard_card.png').convert()
        self.wizard_card_surface = pygame.transform.scale(self.wizard_card_surface, (68, 83))
        self.wizard_card_rectangle = self.wizard_card_surface.get_rect(topleft=self.wizard_card_initial_position)

        self.num_ball_font = pygame.font.Font(None, 30)
        self.num_ball_surface = self.num_ball_font.render(str(self.num_ball), True, 'Black')
        self.num_ball_rectangle = self.num_ball_surface.get_rect(center=(65, 85))

        self.wave_font = pygame.font.Font(None, 50)
        self.wave_surface = self.wave_font.render(f'Wave {self.wave}', True, 'White')
        self.wave_rectangle = self.wave_surface.get_rect(center=(80, 580))

        self.wave_background_surf = pygame.image.load('Bokemon vs Stick/Picture/utils/wave_background.jpeg').convert()
        self.wave_background_surf = pygame.transform.scale(self.wave_background_surf, (140, 50))
        self.wave_background_rect = self.wave_background_surf.get_rect(center=(80, 580))

        self.wood_plank_surface = pygame.image.load('Bokemon vs Stick/Picture/utils/wood.png').convert()
        self.wood_plank_surface = pygame.transform.scale(self.wood_plank_surface, (140, 50))
        self.wood_plank_rectangle = self.wood_plank_surface.get_rect(topleft=(850, 10))
        self.time = None
        self.timer = pygame.font.Font(None, 36).render(None, True, (255, 255, 255))
        self.timer_rectangle = self.timer.get_rect(center=(890, 35))

        self.back_background_size = (250, 55)
        self.back_background_surf = pygame.surface.Surface(self.back_background_size)
        self.back_background_surf.fill((14, 25, 45))
        self.back_background_rect = self.back_background_surf.get_rect(center=(254, 40))

        self.back_button_surf = pygame.image.load('Stick of War/Picture/Store/back_to_level.png').convert_alpha()
        self.back_button_surf = pygame.transform.scale(self.back_button_surf, (75, 75))
        self.back_button_rect = self.back_button_surf.get_rect(center=(155, 40))

        self.back_word_surf = pygame.font.Font(None, 42)
        self.back_word_surf = self.back_word_surf.render('Back to Home', True, "Green")
        self.back_word_rect = self.back_word_surf.get_rect(center=(270, 40))

    def event_handling(self):
        # Event handling
        for event in pygame.event.get():
            # press 'x' to quit the game
            if event.type == pygame.QUIT:
                database.update_user()
                database.push_data()
                pygame.quit()
                exit()

            if self.before_press_start and event.type == pygame.KEYDOWN:
                if not self.help_menu_page and event.key == pygame.K_h:  # if press 'h' for Help
                    self.help_menu_page = True
                    self.before_press_start = False

            elif self.help_menu_page and event.type == pygame.KEYDOWN:
                if not self.before_press_start and event.key == pygame.K_h:  # if press 'h' for Help
                    self.before_press_start = True
                    self.help_menu_page = False

            # press 'start adventure' in the home page, then game will start
            if event.type == pygame.MOUSEBUTTONDOWN and self.start_adventure_rect.collidepoint(
                    event.pos) and self.before_press_start:
                self.after_press_start = True
                self.before_press_start = False
                self.begin_time = pygame.time.get_ticks()  # this record the initial countdown and i put here coz to only program the time when user move to next page

            # spawned ninja
            if event.type == self.troop_timer and self.after_press_start:
                spawned_troop = Troop((choice(self.troop_choice)), self.grid_coor)
                self.troop_groups.add(spawned_troop)

            # spawned gem_ball from sky
            if event.type == self.gem_ball_timer and self.after_press_start:
                self.spawned_ball.create_gem_ball()

            if event.type == pygame.MOUSEBUTTONDOWN:
                # press hero card from the top , and chosen hero will be that
                if self.machine_card_rectangle.collidepoint(event.pos):
                    self.chosen_hero = 'machine'
                elif self.archer_card_rectangle.collidepoint(event.pos):
                    self.chosen_hero = 'archer'
                elif self.wizard_card_rectangle.collidepoint(event.pos):
                    self.chosen_hero = 'wizard'

                # if pressed gem_ball from sky , earned 50 num_ball
                for gem_ball_rect in self.spawned_ball.gem_ball_rect_storage:
                    if gem_ball_rect.collidepoint(event.pos):
                        self.spawned_ball.gem_ball_rect_storage.remove(gem_ball_rect)
                        self.num_ball += 50
                        break

                # if pressed gem_ball from machine , earned 25 num_ball
                for machine_hero in self.hero_groups:
                    if machine_hero.hero_type == 'machine':
                        for bullet_rect in machine_hero.bullet_rect_storage:
                            if bullet_rect.collidepoint(event.pos):
                                machine_hero.bullet_rect_storage.remove(bullet_rect)
                                self.num_ball += 25
                                break

            # drag the hero card chosen just now
            if self.chosen_hero and event.type == pygame.MOUSEMOTION:
                # card follow the mouse pos
                if self.chosen_hero == 'machine':
                    self.machine_card_rectangle.move_ip(event.rel)
                elif self.chosen_hero == 'archer':
                    self.archer_card_rectangle.move_ip(event.rel)
                elif self.chosen_hero == 'wizard':
                    self.wizard_card_rectangle.move_ip(event.rel)

            # button_up after dragging hero , hero planted and back to the initial position
            if event.type == pygame.MOUSEBUTTONUP and self.chosen_hero is not None:
                # check hero release at which coordinate and enough num_ball or not
                # return None if the position release hero card is unavailable (out of map / already have hero)
                # return the x and y coordinate of the box for planting if available
                self.coordinate = self.tools.find_grid_coor(event.pos, self.grid_coor, self.num_ball,
                                                            self.chosen_hero)

                if self.coordinate is not None:  # not None which mean by is available for planting
                    if self.chosen_hero == 'machine':
                        self.num_ball -= 50
                        if not self.machine_card_rectangle.topleft == self.machine_card_initial_position:
                            self.machine_card_rectangle.topleft = self.machine_card_initial_position  # Snap back to initial position

                    elif self.chosen_hero == 'archer':
                        self.num_ball -= 150
                        if not self.archer_card_rectangle.topleft == self.archer_card_initial_position:
                            self.archer_card_rectangle.topleft = self.archer_card_initial_position  # Snap back to initial position

                    elif self.chosen_hero == 'wizard':
                        self.num_ball -= 100
                        if not self.wizard_card_rectangle.topleft == self.wizard_card_initial_position:
                            self.wizard_card_rectangle.topleft = self.wizard_card_initial_position  # Snap back to initial position

                    # chosen heri spawned at the box with the coordinate returned above
                    spawned_hero = Hero(self.chosen_hero, self.coordinate)
                    self.hero_groups.add(spawned_hero)

                # if return None which mean by not available for planting
                # card snap back without deducting num_balls
                if self.coordinate is None:
                    if self.chosen_hero == 'machine':
                        if not self.machine_card_rectangle.topleft == self.machine_card_initial_position:
                            self.machine_card_rectangle.topleft = self.machine_card_initial_position

                    elif self.chosen_hero == 'archer':
                        if not self.archer_card_rectangle.topleft == self.archer_card_initial_position:
                            self.archer_card_rectangle.topleft = self.archer_card_initial_position

                    elif self.chosen_hero == 'wizard':
                        if not self.wizard_card_rectangle.topleft == self.wizard_card_initial_position:
                            self.wizard_card_rectangle.topleft = self.wizard_card_initial_position

                # clear
                self.chosen_hero = None
                self.coordinate = None

            # player can choose to turn back to main menu(before press start) or play again(after press start)
            if self.lose and event.type == pygame.MOUSEBUTTONDOWN:
                if self.home_page_rect.collidepoint(event.pos):
                    self.reset_game_state()
                    self.before_press_start = True
                    self.after_press_start = False
                elif self.play_again_rect.collidepoint(event.pos):
                    self.reset_game_state()
                    self.after_press_start = True
                    self.before_press_start = False
                    self.begin_time = pygame.time.get_ticks()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                if self.before_press_start and self.back_background_rect.collidepoint(mouse_pos):
                    self.bg_music.stop()
                    self.go_home_py = True

    def game_start(self):
        if self.before_press_start:  # main menu page
            self.screen.blit(self.start_adventure_surface, self.start_adventure_rect)
            self.screen.blit(self.welcome_surface, (0, 0))
            self.screen.blit(self.username_surface, self.username_rectangle)
            self.screen.blit(self.h_surface, self.h_rectangle)
            self.screen.blit(self.back_background_surf, self.back_background_rect)
            self.screen.blit(self.back_button_surf, self.back_button_rect)
            self.screen.blit(self.back_word_surf, self.back_word_rect)

        if self.help_menu_page:
            self.screen.fill((255, 255, 255))
            text_lines = self.help_menu_content.split('\n')
            y_position = 10

            for line in text_lines:
                text = self.help_menu_font.render(line, True, (0, 0, 0))
                self.screen.blit(text, (10, y_position))
                y_position += 20  # Adjust the line spacing as needed

        if self.after_press_start:  # game start
            self.num_ball_surface = self.num_ball_font.render(str(self.num_ball), None, 'Black')

            # timer
            exact_time = pygame.time.get_ticks()
            time_pass = (exact_time - self.begin_time) // 1000
            minutes = time_pass // 60
            seconds = time_pass % 60
            self.time = f"{minutes:02}:{seconds:02}"
            self.timer = pygame.font.Font(None, 36).render(self.time, True, (255, 255, 255))

            # wave
            if minutes >= self.wave:
                self.spawn_time = self.spawn_time // 3
                pygame.time.set_timer(self.troop_timer, self.spawn_time)
                self.wave = minutes + 1

                self.wave_surface = pygame.font.Font(None, 50).render(f'Wave {self.wave}', True, 'White')

            # blit all background
            self.screen.blit(self.background_surface, (0, 0))
            self.screen.blit(self.machine_card_surface, self.machine_card_rectangle)
            self.screen.blit(self.archer_card_surface, self.archer_card_rectangle)
            self.screen.blit(self.wizard_card_surface, self.wizard_card_rectangle)
            self.screen.blit(self.num_ball_surface, self.num_ball_rectangle)
            self.screen.blit(self.wood_plank_surface, self.wood_plank_rectangle)
            self.screen.blit(self.timer, self.timer_rectangle)

            # update the frame of ninja and hero then draw them out
            self.hero_groups.draw(self.screen)
            self.hero_groups.update()
            self.troop_groups.draw(self.screen)
            self.troop_groups.update(self.hero_groups)

            # blit gem ball
            for gem_ball_rect in self.spawned_ball.gem_ball_rect_storage:
                self.spawned_ball.drop_gem_ball()
                self.screen.blit(self.spawned_ball.gem_ball_surface, gem_ball_rect)

            self.screen.blit(self.wave_background_surf, self.wave_background_rect)
            self.screen.blit(self.wave_surface, self.wave_rectangle)

            # First, track which rows still have active troops
            active_rows = set()
            for troop in self.troop_groups:
                if troop.rect.centerx < 1025:  # Only count troops on screen
                    active_rows.add(troop.rect.centery)
            
            # Check each hero individually and set their attack mode based on their row
            for hero in self.hero_groups:
                hero_row = hero.rect.centery
                
                # Check if this hero's row has any troops
                if hero_row in active_rows:
                    # Troops in this row - this hero should be attacking
                    if hero.hero_type != 'machine':
                        hero.change_mode('attacking')
                else:
                    # No troops in this row - this hero should be normal
                    if hero.hero_type != 'machine':
                        hero.change_mode('normal')
                
                # Handle bullet collisions (keep bullets flying until they hit or go off-screen)
                for troop in self.troop_groups:
                    for bullet_rect in hero.bullet_rect_storage[:]:  # Use slice copy to avoid modification during iteration
                        if hero.hero_type != 'machine' and bullet_rect.colliderect(troop.rect):
                            hero.bullet_rect_storage.remove(bullet_rect)
                            if hero.hero_type == 'archer':
                                troop.troop_being_attack(25)
                            elif hero.hero_type == 'wizard':
                                troop.troop_being_attack(18)
                            # Check if troop dies and remove it
                            troop.check_troop_die()
                            break

            # move and blit bullets for all heroes (bullets should continue flying)
            for hero in self.hero_groups:
                if hero.hero_type == 'archer':
                    hero.move_bullet()
                    for bullet_rect in hero.bullet_rect_storage:
                        self.screen.blit(hero.archer_bullet_surface, bullet_rect)
                elif hero.hero_type == 'wizard':
                    hero.move_bullet()
                    for bullet_rect in hero.bullet_rect_storage:
                        self.screen.blit(hero.wizard_bullet_surface, bullet_rect)
                elif hero.hero_type == 'machine':
                    # Machine bullets are collectible gem balls, don't move them like projectiles
                    for bullet_rect in hero.bullet_rect_storage:
                        self.screen.blit(hero.machine_ball_surface, bullet_rect)

            # if ninja cross over to the house then lose
            for troop in self.troop_groups:
                if troop.rect.centerx < 250:
                    self.lose = True
                    self.after_press_start = False

        if self.lose:
            self.screen.fill((0, 0, 0))

            loss_message = pygame.font.Font(None, 135).render("K.O.", True, (255, 255, 255))
            loss_message_rect = loss_message.get_rect(center=(500, 145))
            self.screen.blit(loss_message, loss_message_rect)

            used_time = pygame.font.Font(None, 70).render(f'You survived for {self.time}', True, (255, 255, 255))
            used_time_rect = used_time.get_rect(center=(500, 250))
            self.screen.blit(used_time, used_time_rect)

            wave_message = pygame.font.Font(None, 70).render(f'You reached Wave {self.wave}', True, (255, 255, 255))
            wave_message_rect = wave_message.get_rect(center=(500, 335))
            self.screen.blit(wave_message, wave_message_rect)

            self.wood_plank_surface = pygame.transform.scale(self.wood_plank_surface, (200, 70))

            self.wood_plank_rectangle = self.wood_plank_surface.get_rect(center=(350, 430))
            self.screen.blit(self.wood_plank_surface, self.wood_plank_rectangle)
            home_page = pygame.font.Font(None, 40).render('Home Page', True, (255, 255, 255))
            self.home_page_rect = home_page.get_rect(center=(350, 430))
            self.screen.blit(home_page, self.home_page_rect)

            self.wood_plank_rectangle = self.wood_plank_surface.get_rect(center=(650, 430))
            self.screen.blit(self.wood_plank_surface, self.wood_plank_rectangle)
            play_again = pygame.font.Font(None, 40).render("Play Again", True, (255, 255, 255))
            self.play_again_rect = play_again.get_rect(center=(650, 430))
            self.screen.blit(play_again, self.play_again_rect)

    def run(self):
        self.bg_music = pygame.mixer.Sound('Bokemon vs Stick/audio/bg_music.mp3')
        self.bg_music.set_volume(0.1)
        self.bg_music.play(loops=-1)
        while True:
            # CLear screen
            self.screen.fill((255, 255, 255))

            # event_handling_control_function
            self.event_handling()

            # start function which will blit screen and etc
            self.game_start()

            pygame.display.update()
            pygame.display.flip()  # redraw the screen

            self.clock.tick(60)  # 60 fps


if __name__ == "__main__":
    GamePokemonVsStick().run()
