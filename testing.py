# coding: utf-8

import pygame
from sys import exit
from random import randint, choice

class LogInMethod():
    def __init__(self):
        self.log_in_as = ''

    def sign_up(self, username, password):
        with open('Data/user.txt', mode='a') as f:
            f.write(f'{username}----{password}\n')

    def check_username_taken(self, input_username):
        with open('Data/user.txt', mode='rt', encoding='utf-8') as f:
            for line in f:
                username, password = line.strip().split('----')
                if input_username == username:
                    return False
            return True

    def check_user_pass(self, input_username, input_password):
        with open('Data/user.txt', mode='rt', encoding='utf-8') as f:
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

class Plant(pygame.sprite.Sprite):
    # center coordinate for each box
    # x = [325, 410, 495, 586, 670]
    # y = [172, 262, 352, 442, 532]
    grid_coor = [(325, 172), (325, 262), (325, 352), (325, 442), (325, 532),
                 (410, 172), (410, 262), (410, 352), (410, 442), (410, 532),
                 (495, 172), (495, 262), (495, 352), (495, 442), (495, 532),
                 (586, 172), (586, 262), (586, 352), (586, 442), (586, 532),
                 (670, 172), (670, 262), (670, 352), (670, 442), (670, 532)]

    # plant
    MACHINE_FRAMES = [pygame.image.load('Picture/machine/machine_1.jpeg').convert_alpha(),
                      pygame.image.load('Picture/machine/machine_2.jpeg').convert_alpha()]

    SQUIRTLE_FRAMES = [pygame.image.load('Picture/squirtle/squirtle_1.png').convert_alpha(),
                       pygame.image.load('Picture/squirtle/squirtle_2.png').convert_alpha(),
                       pygame.image.load('Picture/squirtle/squirtle_3.png').convert_alpha(),
                       pygame.image.load('Picture/squirtle/squirtle_4.png').convert_alpha()]

    PIKACHU_FRAMES = [pygame.image.load('Picture/pikachu/pikachu_1.png').convert_alpha(),
                      pygame.image.load('Picture/pikachu/pikachu_2.png').convert_alpha(),
                      pygame.image.load('Picture/pikachu/pikachu_3.png').convert_alpha(),
                      pygame.image.load('Picture/pikachu/pikachu_4.png').convert_alpha()]

    def __init__(self, plant_type):
        super().__init__()

        self.plant_type = plant_type

        if plant_type == 'machine':
            self.frames = [pygame.transform.scale(frame, (75, 82)) for frame in self.MACHINE_FRAMES]
            self.health = 100
            self.damage = 0
        elif plant_type == 'pikachu':
            self.frames = [pygame.transform.scale(frame, (75, 82)) for frame in self.PIKACHU_FRAMES]
            self.health = 200
            self.damage = 25
        elif plant_type == 'squirtle':
            self.frames = [pygame.transform.scale(frame, (75, 82)) for frame in self.SQUIRTLE_FRAMES]
            self.health = 150
            self.damage = 20
        else:
            print('No plant found')

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(center=(choice(self.grid_coor)))

    def update_animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.update_animation_state()

    def being_attack(self, damage):
        self.health -= damage
        if self.health == 0:
            self.kill()

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

    def __init__(self, ninja_type):
        super().__init__()
        # speed cannot be lower than 0.6 , if not ninja will not spawn
        self.ninja_type = ninja_type
        self.speed = 1

        if ninja_type == 'naruto':
            self.frames = [pygame.transform.scale(frame, (84, 45)) for frame in self.NARUTO_FRAMES]
        elif ninja_type == 'sasuke':
            self.frames = [pygame.transform.scale(frame, (75, 55)) for frame in self.SASUKE_FRAMES]
        elif ninja_type == 'kakashi':
            self.frames = [pygame.transform.scale(frame, (90, 60)) for frame in self.KAKASHI_FRAMES]
            self.speed = 2
        else:
            print('No ninja found')

        # spawn at these position
        self.position_list_y = [172, 260, 355, 445, 532]

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(center=(randint(1100, 1300), choice(self.position_list_y)))

    def update_animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.update_animation_state()
        self.rect.x -= self.speed

class Game():
    def __init__(self):
        pygame.display.set_caption('Pokemon vs Naruto')  # title name
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((1000, 600))  # screen size
        self.machine_card_initial_position = (120, 8)
        self.pikachu_card_initial_position = (191, 8)
        self.squirtle_card_initial_position = (262, 8)
        self.num_ball = 10000
        self.set_up()  # set up surface and rectangle etc
        self.before_press_start = True
        self.after_press_start = False
        self.chosen_pokemon = None

        # Groups
        self.ninja_groups = pygame.sprite.Group()
        self.plant_groups = pygame.sprite.Group()

        # set up Ninja timer
        self.ninja_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.ninja_timer, 1500)

        # choice of ninja
        self.ninja_choice = ['naruto', 'sasuke', 'kakashi', 'naruto', 'sasuke']

    def set_up(self):  # set up surface and rectangle etc
        self.welcome_surface = pygame.image.load('Picture/welcome.png').convert()
        self.welcome_surface = pygame.transform.scale(self.welcome_surface, (1000, 600))

        self.white_surface = pygame.image.load('Picture/white_screen.jpeg').convert()
        self.white_surface = pygame.transform.scale(self.white_surface, (400, 100))
        self.white_rectangle = self.white_surface.get_rect(topleft=(500, 90))

        username_font = pygame.font.Font(None, 30)
        self.username_surface = username_font.render(logged_in_user, None, 'White')
        self.username_rectangle = self.username_surface.get_rect(center=(210, 100))

        self.background_surface = pygame.image.load('Picture/game_background_pokemon.png').convert()
        self.background_surface = pygame.transform.scale(self.background_surface, (1000, 600))

        self.machine_card_surface = pygame.image.load('Picture/machine_card.png').convert()
        self.machine_card_surface = pygame.transform.scale(self.machine_card_surface, (68, 83))
        self.machine_card_rectangle = self.machine_card_surface.get_rect(topleft=self.machine_card_initial_position)

        self.pikachu_card_surface = pygame.image.load('Picture/pikachu_card.png').convert()
        self.pikachu_card_surface = pygame.transform.scale(self.pikachu_card_surface, (68, 83))
        self.pikachu_card_rectangle = self.pikachu_card_surface.get_rect(topleft=self.pikachu_card_initial_position)

        self.squirtle_card_surface = pygame.image.load('Picture/squirtle_card.png').convert()
        self.squirtle_card_surface = pygame.transform.scale(self.squirtle_card_surface, (68, 83))
        self.squirtle_card_rectangle = self.squirtle_card_surface.get_rect(topleft=self.squirtle_card_initial_position)

        self.num_ball_font = pygame.font.Font(None, 30)
        self.num_ball_surface = self.num_ball_font.render(str(self.num_ball), None, 'Black')
        self.num_ball_rectangle = self.num_ball_surface.get_rect(center=(65, 85))

    def event_handling(self):
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == self.ninja_timer and self.after_press_start:
                self.ninja_groups.add(Ninja((choice(self.ninja_choice))))

            if event.type == pygame.MOUSEBUTTONDOWN and self.white_rectangle.collidepoint(event.pos):
                self.after_press_start = True
                self.before_press_start = False

            # choose pokemon
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.machine_card_rectangle.collidepoint(event.pos):
                    self.chosen_pokemon = 'machine'
                elif self.pikachu_card_rectangle.collidepoint(event.pos):
                    self.chosen_pokemon = 'pikachu'
                elif self.squirtle_card_rectangle.collidepoint(event.pos):
                    self.chosen_pokemon = 'squirtle'

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
            if event.type == pygame.MOUSEBUTTONUP:
                if self.chosen_pokemon is not None:
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

                    self.plant_groups.add(Plant(self.chosen_pokemon))
                    self.chosen_pokemon = None

    def game_start(self):
        if self.before_press_start:
            self.screen.blit(self.white_surface, self.white_rectangle)
            self.screen.blit(self.welcome_surface, (0, 0))
            self.screen.blit(self.username_surface, self.username_rectangle)

        if self.after_press_start:
            self.num_ball_surface = self.num_ball_font.render(str(self.num_ball), None, 'Black')
            self.screen.blit(self.background_surface, (0, 0))
            self.screen.blit(self.machine_card_surface, self.machine_card_rectangle)
            self.screen.blit(self.pikachu_card_surface, self.pikachu_card_rectangle)
            self.screen.blit(self.squirtle_card_surface, self.squirtle_card_rectangle)
            self.screen.blit(self.num_ball_surface, self.num_ball_rectangle)

            self.ninja_groups.draw(self.screen)
            self.ninja_groups.update()

            self.plant_groups.draw(self.screen)
            self.plant_groups.update()

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

            self.clock.tick(60)

if __name__ == "__main__":
    Game().run()
