# coding: utf-8
import os
import pygame
from sys import exit
from random import randint, choice

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
        self.speed = 1

        if ninja_type == 'naruto':
            self.frames = [pygame.transform.scale(frame, (84, 40)) for frame in self.NARUTO_FRAMES]
        elif ninja_type == 'sasuke':
            self.frames = [pygame.transform.scale(frame, (84, 40)) for frame in self.SASUKE_FRAMES]
        elif ninja_type == 'kakashi':
            self.frames = [pygame.transform.scale(frame, (84, 40)) for frame in self.KAKASHI_FRAMES]
            self.speed = 2
        else:
            print('No ninja found')

        # spawn at these position
        self.position_list_y = [175, 260, 355, 444, 528]

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
        self.active_pokemon = None
        # Groups
        self.ninja_groups = pygame.sprite.Group()
        # set up Ninja timer
        self.ninja_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.ninja_timer, 1500)
        # choice of ninja
        self.ninja_choice = ['naruto', 'sasuke', 'kakashi', 'naruto', 'sasuke']

    def set_up(self):  # set up surface and rectangle etc
        welcome_fp = create_file_path('Picture/welcome.png')
        self.welcome_surface = pygame.image.load(welcome_fp).convert()
        self.welcome_surface = pygame.transform.scale(self.welcome_surface, (1000, 600))

        white_fp = create_file_path('Picture/white_screen.jpeg')
        self.white_surface = pygame.image.load(white_fp).convert()
        self.white_surface = pygame.transform.scale(self.white_surface, (400, 100))
        self.white_rectangle = self.white_surface.get_rect(topleft=(500, 90))

        username_font = pygame.font.Font(None, 30)
        self.username_surface = username_font.render(logged_in_user, None, 'White')
        self.username_rectangle = self.username_surface.get_rect(center=(210, 100))

        background_fp = create_file_path('Picture/game_background_pokemon.png')
        self.background_surface = pygame.image.load(background_fp).convert()
        self.background_surface = pygame.transform.scale(self.background_surface, (1000, 600))

        machine_card_fp = create_file_path('Picture/machine_card.png')
        self.machine_card_surface = pygame.image.load(machine_card_fp).convert()
        self.machine_card_surface = pygame.transform.scale(self.machine_card_surface, (68, 83))
        self.machine_card_rectangle = self.machine_card_surface.get_rect(topleft=self.machine_card_initial_position)

        pikachu_card_fp = create_file_path('Picture/pikachu_card.png')
        self.pikachu_card_surface = pygame.image.load(pikachu_card_fp).convert()
        self.pikachu_card_surface = pygame.transform.scale(self.pikachu_card_surface, (68, 83))
        self.pikachu_card_rectangle = self.pikachu_card_surface.get_rect(topleft=self.pikachu_card_initial_position)

        squirtle_card_fp = create_file_path('Picture/squirtle_card.png')
        self.squirtle_card_surface = pygame.image.load(squirtle_card_fp).convert()
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
                    self.active_pokemon = 'machine'
                elif self.pikachu_card_rectangle.collidepoint(event.pos):
                    self.active_pokemon = 'pikachu'
                elif self.squirtle_card_rectangle.collidepoint(event.pos):
                    self.active_pokemon = 'squirtle'

            # drag pokemon
            if self.active_pokemon and event.type == pygame.MOUSEMOTION:
                # card follow the mouse pos
                if self.active_pokemon == 'machine':
                    self.machine_card_rectangle.move_ip(event.rel)
                elif self.active_pokemon == 'pikachu':
                    self.pikachu_card_rectangle.move_ip(event.rel)
                elif self.active_pokemon == 'squirtle':
                    self.squirtle_card_rectangle.move_ip(event.rel)

            # pokemon released and back to the initial position
            if event.type == pygame.MOUSEBUTTONUP:
                if self.active_pokemon is not None:
                    if self.active_pokemon == 'machine':
                        self.num_ball -= 50
                        if not self.machine_card_rectangle.colliderect(self.machine_card_initial_position + (1, 1)):
                            self.machine_card_rectangle.topleft = self.machine_card_initial_position  # Snap back to initial position

                    elif self.active_pokemon == 'pikachu':
                        self.num_ball -= 150
                        if not self.pikachu_card_rectangle.colliderect(self.pikachu_card_initial_position + (1, 1)):
                            self.pikachu_card_rectangle.topleft = self.pikachu_card_initial_position  # Snap back to initial position

                    elif self.active_pokemon == 'squirtle':
                        self.num_ball -= 100
                        if not self.squirtle_card_rectangle.colliderect(self.squirtle_card_initial_position + (1, 1)):
                            self.squirtle_card_rectangle.topleft = self.squirtle_card_initial_position  # Snap back to initial position

                    self.active_pokemon = None

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
