# coding: utf-8
import os
import pygame
from sys import exit
from random import randint, choice, uniform


def create_file_path(file):
    # Get the directory of the current script
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the file path relative to the current script
    file_path = os.path.join(current_dir, file)
    return file_path


class LogInMethod():
    def __init__(self):
        self.data_user = create_file_path('Data/user.txt')
        self.log_in_as = ''

    def sign_up(self, username, password):
        with open(self.data_user, mode='a') as f:
            f.write(f'{username}----{password}\n')

    def check_username_taken(self, input_username):
        with open(self.data_user, mode='rt', encoding='utf-8') as f:
            for line in f:
                username, password = line.strip().split('----')
                if input_username == username:
                    return False
            return True

    def check_user_pass(self, input_username, input_password):
        with open(self.data_user, mode='rt', encoding='utf-8') as f:
            for line in f:
                username, password = line.strip().split('----')
                if input_username == username and input_password == password:
                    return True
            print('No account found. Check your username and password. You have to register an account to sign in')
            return False

    def ask_log_in_method(self):
        log_in_method = input('Sign up an account enter "U" \n'
                              'Sign in an account enter "I"\n'
                              'Log in as guest enter "G"\n\n'
                              'Please enter your choice here :  ').strip().upper()
        return log_in_method

    def run(self):
        while True:
            log_in_method = self.ask_log_in_method()

            if log_in_method == 'G':  # log in as guest
                self.log_in_as = 'Guest'
                print(f'Logged in as : {self.log_in_as.title()}')
                return self.log_in_as

            elif log_in_method == 'U':  # sign up an account
                while True:
                    input_username = input('Enter username for sign up : ').strip()
                    res = self.check_username_taken(input_username)
                    if res:
                        input_password = input('Enter your password: ').strip()
                        print('Successfully registered')
                        print(f'Username:  {input_username}')
                        print(f'Password:  {input_password}')
                        print('Now, you can sign in your account\n')
                        break
                    else:
                        print('Username Taken, Please choose an another one')

                self.sign_up(input_username, input_password)

            elif log_in_method == 'I':
                while True:
                    input_username = input('Enter your username: ').strip()
                    input_password = input('Enter your password: ').strip()
                    res = self.check_user_pass(input_username, input_password)
                    if res:
                        self.log_in_as = input_username
                        print(f'Logged in as : {self.log_in_as.title()}')
                        return self.log_in_as.title()
                    else:
                        print('Incorrect username or password. Please try again.')

            else:
                print('Please enter the correct symbol\n')


logged_in_user = LogInMethod().run()

# have to initialise the pygame first because of loading image in class Ninja
pygame.init()
pygame.display.set_caption('Pokemon vs Naruto')  # title name
pygame.display.set_mode((1000, 600))


class Tools:
    def find_grid_coor(self, pos, grid_coor):
        # check whether out of map
        # 312 - 42 = 272 ( least x ) , 927 + 42 = 967 ( max x )
        # 172 - 45 = 127 ( least y ) , 532 + 45 = 577 ( max x )
        if pos[0] < 272 or pos[0] > 967 or pos[1] < 127 or pos[1] > 577:
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
                            return (coor[0], coor[1])  # return coordinate where pokemon have to stay

    def check_alive_pokemon(self, poke_groups, grid_coor):
        alive_pokemon = []
        for pokemon in poke_groups:
            if [pokemon.rect[0], pokemon.rect[1], 0] not in alive_pokemon:
                alive_pokemon.append([pokemon.rect[0], pokemon.rect[1], 1])
            for column in grid_coor:
                for coor in column:
                    if coor[2] != 0:
                        if coor not in alive_pokemon:
                            coor[2] = 0


class Poke_Ball:
    def __init__(self):
        self.poke_ball_surface = pygame.image.load('Picture/utils/Poke_Ball.png').convert_alpha()
        self.poke_ball_surface = pygame.transform.scale(self.poke_ball_surface, (50, 50))
        self.poke_ball_rect_storage = []

    def create_poke_ball(self):
        poke_ball_rectangle = self.poke_ball_surface.get_rect(center=(randint(312, 927), randint(-250, -100)))
        self.poke_ball_rect_storage.append(poke_ball_rectangle)

    def drop_poke_ball(self):
        for poke_ball_rect in self.poke_ball_rect_storage:
            # dropping from up and stop at bottom
            if poke_ball_rect.y < 535:
                poke_ball_rect.y += uniform(0.4, 0.6)


class Pokemon(pygame.sprite.Sprite):
    # pokemon
    MACHINE_FRAMES = [
                         pygame.image.load('Picture/machine/machine_1.png').convert_alpha() for _ in range(15)] + [
                         pygame.image.load('Picture/machine/machine_2.png').convert_alpha()
                     ]

    SQUIRTLE_ATTACK = [pygame.image.load('Picture/squirtle/squirtle_1.png').convert_alpha(),
                       pygame.image.load('Picture/squirtle/squirtle_2.png').convert_alpha(),
                       pygame.image.load('Picture/squirtle/squirtle_3.png').convert_alpha(),
                       pygame.image.load('Picture/squirtle/squirtle_4.png').convert_alpha()]

    PIKACHU_ATTACK = [pygame.image.load('Picture/pikachu/pikachu_1.png').convert_alpha(),
                      pygame.image.load('Picture/pikachu/pikachu_2.png').convert_alpha(),
                      pygame.image.load('Picture/pikachu/pikachu_3.png').convert_alpha(),
                      pygame.image.load('Picture/pikachu/pikachu_4.png').convert_alpha()]

    PIKACHU_NORMAL = [pygame.image.load('Picture/pikachu/pikachu_1.png').convert_alpha(),
                      pygame.image.load('Picture/pikachu/pikachu_3.png').convert_alpha(),
                      pygame.image.load('Picture/pikachu/pikachu_4.png').convert_alpha()]

    SQUIRTLE_NORMAL = [pygame.image.load('Picture/squirtle/squirtle_1.png').convert_alpha(),
                       pygame.image.load('Picture/squirtle/squirtle_1.png').convert_alpha(),
                       pygame.image.load('Picture/squirtle/squirtle_2.png').convert_alpha(),
                       pygame.image.load('Picture/squirtle/squirtle_2.png').convert_alpha()]

    def __init__(self, pokemon_type, pokemoning_coordinate):
        super().__init__()

        self.pokemon_type = pokemon_type
        self.pokemoning_coordinate = pokemoning_coordinate

        if self.pokemon_type == 'machine':
            self.normal_frames = [pygame.transform.scale(frame, (70, 82)) for frame in self.MACHINE_FRAMES]
            self.health = 100
        elif self.pokemon_type == 'pikachu':
            self.attack_frames = [pygame.transform.scale(frame, (75, 82)) for frame in self.PIKACHU_ATTACK]
            self.normal_frames = [pygame.transform.scale(frame, (75, 82)) for frame in self.PIKACHU_NORMAL]
            self.health = 200
            self.bullet_speed = 5
        elif self.pokemon_type == 'squirtle':
            self.attack_frames = [pygame.transform.scale(frame, (75, 82)) for frame in self.SQUIRTLE_ATTACK]
            self.normal_frames = [pygame.transform.scale(frame, (75, 82)) for frame in self.SQUIRTLE_NORMAL]
            self.health = 150
            self.bullet_speed = 4
        else:
            print('No pokemon found')

        self.frames = self.normal_frames
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(center=(self.pokemoning_coordinate))

        self.pikachu_bullet_surface = pygame.image.load('Picture/pikachu/pikachu_attack.png').convert_alpha()
        self.pikachu_bullet_surface = pygame.transform.scale(self.pikachu_bullet_surface, (50, 50))
        self.pikachu_bullet_rectangle = self.pikachu_bullet_surface.get_rect(center=self.rect.center)

        self.squirtle_bullet_surface = pygame.image.load('Picture/squirtle/squirtle_attack.png').convert_alpha()
        self.squirtle_bullet_surface = pygame.transform.scale(self.squirtle_bullet_surface, (50, 50))
        self.squirtle_bullet_rectangle = self.squirtle_bullet_surface.get_rect(center=self.rect.center)

        self.machine_ball_surface = pygame.image.load('Picture/utils/Poke_Ball.png').convert_alpha()
        self.machine_ball_surface = pygame.transform.scale(self.machine_ball_surface, (25, 25))
        self.machine_ball_rectangle = self.machine_ball_surface.get_rect(center=self.rect.center)

        # this list will store all active bullet
        self.bullet_rect_storage = []

    def check_attacking(self, answer):
        if self.pokemon_type == 'pikachu' or self.pokemon_type == 'squirtle':
            if answer == 'attacking':
                self.frames = self.attack_frames
            if answer == 'normal':
                self.frames = self.normal_frames

    def update_animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
            self.create_bullet()

        self.image = self.frames[int(self.animation_index)]

    def create_bullet(self):
        # bullet created append into the list
        if self.pokemon_type == 'pikachu':
            new_bullet = self.pikachu_bullet_surface.get_rect(center=self.rect.center)
        elif self.pokemon_type == 'squirtle':
            new_bullet = self.squirtle_bullet_surface.get_rect(center=self.rect.center)
        elif self.pokemon_type == 'machine':
            new_bullet = self.machine_ball_surface.get_rect(
                center=((self.rect.bottomright[0] + randint(-15, 15)), ((self.rect.bottomright[1] + randint(-15, 15)))))

        self.bullet_rect_storage.append(new_bullet)

    def move_bullet(self):
        for bullet_rect in self.bullet_rect_storage:
            bullet_rect.x += self.bullet_speed  # Move the bullet to the right of Pikachu
            if bullet_rect.x > 1010:
                # Remove bullets that have moved off-screen
                self.bullet_rect_storage.remove(bullet_rect)

    def update(self):
        self.update_animation_state()


class Ninja(pygame.sprite.Sprite):
    # load images
    NARUTO_FRAMES = [pygame.image.load('Picture/naruto/naruto_walk_1.png').convert_alpha(),
                     pygame.image.load('Picture/naruto/naruto_walk_2.png').convert_alpha(),
                     pygame.image.load('Picture/naruto/naruto_walk_3.png').convert_alpha()]

    SASUKE_FRAMES = [pygame.image.load('Picture/sasuke/sasuke_walk_1.png').convert_alpha(),
                     pygame.image.load('Picture/sasuke/sasuke_walk_2.png').convert_alpha(),
                     pygame.image.load('Picture/sasuke/sasuke_walk_3.png').convert_alpha()]

    KAKASHI_FRAMES = [pygame.image.load('Picture/kakashi/kakashi_run_1.png').convert_alpha(),
                      pygame.image.load('Picture/kakashi/kakashi_run_2.png').convert_alpha(),
                      pygame.image.load('Picture/kakashi/kakashi_run_3.png').convert_alpha()]

    # attack image
    Naruto_attack_frame = [pygame.image.load('Picture/naruto/naruto_attack_1.png').convert_alpha(),
                           pygame.image.load('Picture/naruto/naruto_attack_2.png').convert_alpha()]

    Sasuke_attack_frame = [pygame.image.load('Picture/sasuke/sasuke_attack_1.png').convert_alpha(),
                           pygame.image.load('Picture/sasuke/sasuke_attack_2.png').convert_alpha()]

    Kakashi_attack_frame = [pygame.image.load('Picture/kakashi/kakashi_attack_1.png').convert_alpha(),
                            pygame.image.load('Picture/kakashi/kakashi_attack_2.png').convert_alpha()]

    def __init__(self, ninja_type):
        super().__init__()
        # speed cannot be lower than 0.6 , if not ninja will not spawn
        self.ninja_type = ninja_type
        self.speed = 1

        if ninja_type == 'naruto':
            self.frames = [pygame.transform.scale(frame, (84, 45)) for frame in self.NARUTO_FRAMES]
            self.frame = [pygame.transform.scale(frame, (84, 45)) for frame in self.Naruto_attack_frame]
            self.health = 120
            self.attack = 20
            self.cooldown = 0
        elif ninja_type == 'sasuke':
            self.frames = [pygame.transform.scale(frame, (75, 55)) for frame in self.SASUKE_FRAMES]
            self.frame = [pygame.transform.scale(frame, (75, 55)) for frame in self.Sasuke_attack_frame]
            self.health = 100
            self.attack = 15
            self.cooldown = 0
        elif ninja_type == 'kakashi':
            self.frames = [pygame.transform.scale(frame, (110, 85)) for frame in self.KAKASHI_FRAMES]
            self.frame = [pygame.transform.scale(frame, (110, 85)) for frame in self.Kakashi_attack_frame]
            self.speed = 2
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

    def update(self, pokemon_groups):
        self.update_animation_state()

        if self.cooldown > 0:
            self.cooldown -= 1

        self.rect.x -= self.speed

        collisions = pygame.sprite.spritecollide(self, pokemon_groups, False)
        if collisions:
            self.speed = 0
            self.animation_attack_state()
            if self.cooldown == 0:
                for pokemon in collisions:
                    pokemon.health -= self.attack

                    self.cooldown = 60
                    if pokemon.health <= 0:
                        pokemon.kill()
                        self.speed = self.original_speed
        else:
            self.speed = self.original_speed

    def ninja_being_attack(self, damage):
        self.health -= damage

    def check_ninja_die(self):
        if self.health <= 0:
            self.kill()
            return True


class Game():
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((1000, 600))  # screen size
        self.machine_card_initial_position = (120, 8)
        self.pikachu_card_initial_position = (191, 8)
        self.squirtle_card_initial_position = (262, 8)
        self.before_press_start = True
        self.after_press_start = False

        # Groups
        self.ninja_groups = pygame.sprite.Group()
        self.pokemon_groups = pygame.sprite.Group()

        # reset game state for play again
        self.reset_game_state()

        # set up Ninja timer
        self.ninja_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.ninja_timer, 6000)

        self.spawned_ball = Poke_Ball()
        # set up poke_ball_drop_timer
        self.poke_ball_timer = pygame.USEREVENT + 2
        pygame.time.set_timer(self.poke_ball_timer, 10000)

        # choice of ninja
        self.ninja_choice = ['naruto', 'sasuke', 'kakashi', 'sasuke']

    def reset_game_state(self):
        self.num_ball = 10000
        self.chosen_pokemon = None
        self.coordinate = None
        self.remaining_time = None
        self.timer_duration = 90000  # milisec
        self.row_with_ninja = []
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
        self.ninja_groups.empty()
        self.pokemon_groups.empty()
        self.set_up()  # set up surface and rectangle etc

    def set_up(self):  # set up surface and rectangle etc
        welcome_fp = create_file_path('Picture/utils/welcome.jpg')
        self.welcome_surface = pygame.image.load(welcome_fp).convert()
        self.welcome_surface = pygame.transform.scale(self.welcome_surface, (1000, 600))

        white_fp = create_file_path('Picture/utils/white_screen.jpeg')
        self.white_surface = pygame.image.load(white_fp).convert()
        self.white_surface = pygame.transform.scale(self.white_surface, (410, 100))
        self.white_rectangle = self.white_surface.get_rect(topleft=(510, 70))

        username_font = pygame.font.Font(None, 30)
        self.username_surface = username_font.render(logged_in_user, None, 'Green')
        self.username_rectangle = self.username_surface.get_rect(center=(257, 90))

        background_fp = create_file_path('Picture/utils/game_background.png')
        self.background_surface = pygame.image.load(background_fp).convert()
        self.background_surface = pygame.transform.scale(self.background_surface, (1000, 600))

        machine_card_fp = create_file_path('Picture/machine/machine_card.png')
        self.machine_card_surface = pygame.image.load(machine_card_fp).convert()
        self.machine_card_surface = pygame.transform.scale(self.machine_card_surface, (68, 83))
        self.machine_card_rectangle = self.machine_card_surface.get_rect(topleft=self.machine_card_initial_position)

        pikachu_card_fp = create_file_path('Picture/pikachu/pikachu_card.png')
        self.pikachu_card_surface = pygame.image.load(pikachu_card_fp).convert()
        self.pikachu_card_surface = pygame.transform.scale(self.pikachu_card_surface, (68, 83))
        self.pikachu_card_rectangle = self.pikachu_card_surface.get_rect(topleft=self.pikachu_card_initial_position)

        squirtle_card_fp = create_file_path('Picture/squirtle/squirtle_card.png')
        self.squirtle_card_surface = pygame.image.load(squirtle_card_fp).convert()
        self.squirtle_card_surface = pygame.transform.scale(self.squirtle_card_surface, (68, 83))
        self.squirtle_card_rectangle = self.squirtle_card_surface.get_rect(topleft=self.squirtle_card_initial_position)

        self.num_ball_font = pygame.font.Font(None, 30)
        self.num_ball_surface = self.num_ball_font.render(str(self.num_ball), None, 'Black')
        self.num_ball_rectangle = self.num_ball_surface.get_rect(center=(65, 85))

        wood_plank = create_file_path('Picture/utils/wood.png')
        self.wood_plank_surface = pygame.image.load(wood_plank).convert()
        self.wood_plank_surface = pygame.transform.scale(self.wood_plank_surface, (140, 50))
        self.wood_plank_rectangle = self.wood_plank_surface.get_rect(topleft=(850, 10))
        self.timer = pygame.font.Font(None, 36).render(None, True, (255, 255, 255))
        self.timer_rectangle = self.timer.get_rect(center=(890, 35))

    def event_handling(self):
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == self.ninja_timer and self.after_press_start:
                spawned_ninja = Ninja((choice(self.ninja_choice)))
                self.ninja_groups.add(spawned_ninja)

            if event.type == self.poke_ball_timer and self.after_press_start:
                self.spawned_ball.create_poke_ball()

            if event.type == pygame.MOUSEBUTTONDOWN and self.white_rectangle.collidepoint(event.pos):
                self.after_press_start = True
                self.before_press_start = False
                self.begin_time = pygame.time.get_ticks()  # this record the initial countdown and i put here coz to only program the time when user move to next page

            # choose pokemon
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.machine_card_rectangle.collidepoint(event.pos):
                    self.chosen_pokemon = 'machine'
                elif self.pikachu_card_rectangle.collidepoint(event.pos):
                    self.chosen_pokemon = 'pikachu'
                elif self.squirtle_card_rectangle.collidepoint(event.pos):
                    self.chosen_pokemon = 'squirtle'

                for poke_ball_rect in self.spawned_ball.poke_ball_rect_storage:
                    if poke_ball_rect.collidepoint(event.pos):  # if the ball pos collide witht the pos i click
                        self.spawned_ball.poke_ball_rect_storage.remove(poke_ball_rect)  # remove
                        self.num_ball += 50
                        break

                for machine_pokemon in self.pokemon_groups:
                    if machine_pokemon.pokemon_type == 'machine':
                        for bullet_rect in machine_pokemon.bullet_rect_storage:
                            if bullet_rect.collidepoint(event.pos):
                                machine_pokemon.bullet_rect_storage.remove(bullet_rect)
                                self.num_ball += 20
                                break

            # drag pokemon
            if self.chosen_pokemon and event.type == pygame.MOUSEMOTION:
                # card follow the mouse pos
                if self.chosen_pokemon == 'machine':
                    self.machine_card_rectangle.move_ip(event.rel)
                elif self.chosen_pokemon == 'pikachu':
                    self.pikachu_card_rectangle.move_ip(event.rel)
                elif self.chosen_pokemon == 'squirtle':
                    self.squirtle_card_rectangle.move_ip(event.rel)

            # pokemon released and back to the initial position
            if event.type == pygame.MOUSEBUTTONUP and self.chosen_pokemon is not None:
                # check pokemon release at which coordinate
                self.coordinate = self.tools.find_grid_coor(event.pos, self.grid_coor)
                if self.coordinate is not None:
                    if self.chosen_pokemon == 'machine':
                        self.num_ball -= 50
                        if not self.machine_card_rectangle.colliderect(self.machine_card_initial_position + (1, 1)):
                            self.machine_card_rectangle.topleft = self.machine_card_initial_position  # Snap back to initial position

                    elif self.chosen_pokemon == 'pikachu':
                        self.num_ball -= 150
                        if not self.pikachu_card_rectangle.colliderect(self.pikachu_card_initial_position + (1, 1)):
                            self.pikachu_card_rectangle.topleft = self.pikachu_card_initial_position  # Snap back to initial position

                    elif self.chosen_pokemon == 'squirtle':
                        self.num_ball -= 100
                        if not self.squirtle_card_rectangle.colliderect(self.squirtle_card_initial_position + (1, 1)):
                            self.squirtle_card_rectangle.topleft = self.squirtle_card_initial_position  # Snap back to initial position

                    spawned_pokemon = Pokemon(self.chosen_pokemon, self.coordinate)
                    self.pokemon_groups.add(spawned_pokemon)

                # card snap back without deducting num_balls
                if self.coordinate is None:
                    if self.chosen_pokemon == 'machine':
                        if not self.machine_card_rectangle.colliderect(self.machine_card_initial_position + (1, 1)):
                            self.machine_card_rectangle.topleft = self.machine_card_initial_position

                    elif self.chosen_pokemon == 'pikachu':
                        if not self.pikachu_card_rectangle.colliderect(self.pikachu_card_initial_position + (1, 1)):
                            self.pikachu_card_rectangle.topleft = self.pikachu_card_initial_position

                    elif self.chosen_pokemon == 'squirtle':
                        if not self.squirtle_card_rectangle.colliderect(self.squirtle_card_initial_position + (1, 1)):
                            self.squirtle_card_rectangle.topleft = self.squirtle_card_initial_position

                self.chosen_pokemon = None
                self.coordinate = None

            if self.remaining_time == 0 and event.type == pygame.MOUSEBUTTONDOWN:
                if self.home_page_rect.collidepoint(event.pos):
                    self.reset_game_state()
                    self.before_press_start = True
                    self.after_press_start = False
                elif self.play_again_rect.collidepoint(event.pos):
                    self.reset_game_state()
                    self.after_press_start = True
                    self.before_press_start = False
                    self.begin_time = pygame.time.get_ticks()

    def game_start(self):
        if self.before_press_start:
            self.screen.blit(self.white_surface, self.white_rectangle)
            self.screen.blit(self.welcome_surface, (0, 0))
            self.screen.blit(self.username_surface, self.username_rectangle)

        if self.after_press_start:
            self.num_ball_surface = self.num_ball_font.render(str(self.num_ball), None, 'Black')

            exact_time = pygame.time.get_ticks()
            time_pass = exact_time - self.begin_time
            self.remaining_time = max(0, self.timer_duration - time_pass)
            minutes = self.remaining_time // 60000
            seconds = (self.remaining_time % 60000) // 1000
            self.timer = pygame.font.Font(None, 36).render(f"{minutes:02}:{seconds:02}", True, (255, 255, 255))

            self.screen.blit(self.background_surface, (0, 0))
            self.screen.blit(self.machine_card_surface, self.machine_card_rectangle)
            self.screen.blit(self.pikachu_card_surface, self.pikachu_card_rectangle)
            self.screen.blit(self.squirtle_card_surface, self.squirtle_card_rectangle)
            self.screen.blit(self.num_ball_surface, self.num_ball_rectangle)

            self.screen.blit(self.wood_plank_surface, self.wood_plank_rectangle)
            self.screen.blit(self.timer, self.timer_rectangle)

            self.pokemon_groups.draw(self.screen)
            self.pokemon_groups.update()

            self.ninja_groups.draw(self.screen)
            self.ninja_groups.update(self.pokemon_groups)

            for pokemon in self.pokemon_groups:
                for ninja in self.ninja_groups:
                    # if ninja in that row, add into self.row_with_ninja
                    if ninja.rect.centerx < 1000 and ninja.rect.centery == pokemon.rect.centery:
                        if ninja.rect.centery not in self.row_with_ninja:
                            # append the y_coor into it
                            # using y_coor is because later check whether same y_coor with plant which mean by same row
                            self.row_with_ninja.append(ninja.rect.centery)
                            pokemon.check_attacking('attacking')

                        die = ninja.check_ninja_die()
                        if die or ninja.rect.centerx < (pokemon.rect.centerx - 20):
                            self.row_with_ninja.remove(ninja.rect.centery)
                            for bullet_rect in pokemon.bullet_rect_storage:
                                if bullet_rect.x > 1030:
                                    pokemon.bullet_rect_storage.remove(bullet_rect)
                            pokemon.check_attacking('normal')

                    # bullet collide then cause damage
                    for bullet_rect in pokemon.bullet_rect_storage:
                        if bullet_rect.colliderect(ninja.rect):
                            pokemon.bullet_rect_storage.remove(bullet_rect)
                            if pokemon.pokemon_type == 'pikachu':
                                ninja.ninja_being_attack(20)
                            elif pokemon.pokemon_type == 'squirtle':
                                ninja.ninja_being_attack(20)
                            break

            # move bullet and blit bullet for pokemon in row_with_ninja
            for pokemon in self.pokemon_groups:
                if pokemon.rect.centery in self.row_with_ninja:
                    if pokemon.pokemon_type == 'pikachu':
                        pokemon.move_bullet()
                        for bullet_rect in pokemon.bullet_rect_storage:
                            self.screen.blit(pokemon.pikachu_bullet_surface, bullet_rect)
                    elif pokemon.pokemon_type == 'squirtle':
                        pokemon.move_bullet()
                        for bullet_rect in pokemon.bullet_rect_storage:
                            self.screen.blit(pokemon.squirtle_bullet_surface, bullet_rect)

                if pokemon.pokemon_type == 'machine':
                    for bullet_rect in pokemon.bullet_rect_storage:
                        self.screen.blit(pokemon.machine_ball_surface, bullet_rect)  # Draw the poke ball

            self.tools.check_alive_pokemon(self.pokemon_groups, self.grid_coor)

            for poke_ball_rect in self.spawned_ball.poke_ball_rect_storage:
                self.spawned_ball.drop_poke_ball()
                self.screen.blit(self.spawned_ball.poke_ball_surface, poke_ball_rect)

        if self.remaining_time == 0:
            self.after_press_start = False
            self.screen.fill((0, 0, 0))
            win_message = pygame.font.Font(None, 85).render("You've Won", True, (255, 255, 255))
            win_message_rect = win_message.get_rect(center=(500, 220))
            self.screen.blit(win_message, win_message_rect)

            self.wood_plank_surface = pygame.transform.scale(self.wood_plank_surface, (200, 70))

            self.wood_plank_rectangle = self.wood_plank_surface.get_rect(center=(350, 360))
            self.screen.blit(self.wood_plank_surface, self.wood_plank_rectangle)
            home_page = pygame.font.Font(None, 40).render('Home Page', True, (255, 255, 255))
            self.home_page_rect = home_page.get_rect(center=(350, 360))
            self.screen.blit(home_page, self.home_page_rect)

            self.wood_plank_rectangle = self.wood_plank_surface.get_rect(center=(650, 360))
            self.screen.blit(self.wood_plank_surface, self.wood_plank_rectangle)
            play_again = pygame.font.Font(None, 40).render("Play Again", True, (255, 255, 255))
            self.play_again_rect = play_again.get_rect(center=(650, 360))
            self.screen.blit(play_again, self.play_again_rect)

    def run(self):
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
    Game().run()
