# coding: utf-8

# block 3 to 12 is on creating file path
import os


def create_file_path(file):
    # Get the directory of the current script
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the file path relative to the current script
    file_path = os.path.join(current_dir, file)
    return file_path


# block 14 to 85 is on log_in_method chosen , user can signup , signin or log in as guest
data_user = create_file_path('Data/user.txt')


def sign_up(username, password):
    with open(data_user, mode='a') as f:
        f.write(f'{username}----{password}\n')


def check_username_taken(input_username):
    with open(data_user, mode='rt', encoding='utf-8') as f:
        for line in f:
            username, password = line.strip().split('----')
            if input_username == username:
                print('Username Taken, Please choose an another one')
                break
        else:
            return 'y'


def check_user_pass(input_username, input_password):
    with open(data_user, mode='rt', encoding='utf-8') as f:
        for line in f:
            username, password = line.strip().split('----')
            if input_username == username and input_password == password:
                return 'y'

        else:
            print('No account found. Check your username and password. You have to register an account to sign in')


asking_log_in_method = True
log_in_as = ''

while asking_log_in_method:
    log_in_method = input('Sign up an account enter "U" \n'
                          'Sign in an account enter "I"\n'
                          'Log in as guest enter "G"\n\n'
                          'Please enter your choice here :  ').strip().upper()

    if log_in_method == 'G':  # log in as guest
        print('Logged in as guest')
        log_in_as = 'Guest'
        asking_log_in_method = False

    elif log_in_method == 'U':  # sign up an account
        while True:
            input_username = input('Enter your username: ').strip()
            res = check_username_taken(input_username)
            if res == 'y':
                input_password = input('Enter your password: ').strip()
                print('Successfully registered\n')
                break

        sign_up(input_username, input_password)


    elif log_in_method == 'I':
        while True:
            input_username = input('Enter your username: ').strip()
            input_password = input('Enter your password: ').strip()
            res = check_user_pass(input_username, input_password)
            if res == 'y':
                print('Logged in')
                break

        log_in_as = input_username
        asking_log_in_method = False

    else:
        print('Please key in the correct symbol')

# game
import pygame
from sys import exit
from random import randint, choice

pygame.init()  # starting code

screen = pygame.display.set_mode((1000, 600))  # screen size
pygame.display.set_caption('Pokemon vs Naruto')  # title name
clock = pygame.time.Clock()
game_active = True
bg_music = pygame.mixer.Sound('audio/Plants vs. Zombies (Main Theme).mp3')
bg_music.play(loops=-1)

# load images
naruto_frames = [pygame.image.load('Picture/naruto/naruto_walk_1.png').convert_alpha(),
                 pygame.image.load('Picture/naruto/naruto_walk_2.png').convert_alpha(),
                 pygame.image.load('Picture/naruto/naruto_walk_3.png').convert_alpha()]

sasuke_frame = [pygame.image.load('Picture/sasuke/sasuke_walk_1.png').convert_alpha(),
                pygame.image.load('Picture/sasuke/sasuke_walk_2.png').convert_alpha(),
                pygame.image.load('Picture/sasuke/sasuke_walk_3.png').convert_alpha()]

kakashi_frame = [pygame.image.load('Picture/kakashi/kakashi_run_1.png').convert_alpha(),
                 pygame.image.load('Picture/kakashi/kakashi_run_2.png').convert_alpha(),
                 pygame.image.load('Picture/kakashi/kakashi_run_3.png').convert_alpha()]

naruto_frames = [pygame.transform.scale(frame, (84, 40)) for frame in naruto_frames]
sasuke_frame = [pygame.transform.scale(frame, (84, 40)) for frame in sasuke_frame]
kakashi_frame = [pygame.transform.scale(frame, (84, 40)) for frame in kakashi_frame]


class Zombie(pygame.sprite.Sprite):
    def __init__(self, type, position_list_y):
        super().__init__()

        self.speed = 0.7

        if type == 'naruto':
            self.frames = naruto_frames

        elif type == 'sasuke':
            self.frames = sasuke_frame

        else:
            self.frames = kakashi_frame
            self.speed = 2

        self.position_list_y = position_list_y

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(center=(randint(1100, 1300), choice(position_list_y)))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= self.speed


# Groups
zombie_groups = pygame.sprite.Group()

# Set up surface and rectangle
welcome_fp = create_file_path('Picture/welcome.png')
welcome_surface = pygame.image.load(welcome_fp).convert()
welcome_surface = pygame.transform.scale(welcome_surface, (1000, 600))

white_fp = create_file_path('Picture/white_screen.jpeg')
white_surface = pygame.image.load(white_fp).convert()
white_surface = pygame.transform.scale(white_surface, (400, 100))
white_rectangle = white_surface.get_rect(topleft=(500, 90))

username_font = pygame.font.Font(None, 30)
username_surface = username_font.render(log_in_as, None, 'White')
username_rectangle = username_surface.get_rect(center=(210, 100))

background_fp = create_file_path('Picture/game_background_pokemon.png')
background_surface = pygame.image.load(background_fp).convert()
background_surface = pygame.transform.scale(background_surface, (1000, 600))

# set up Zombie timer
zombie_timer = pygame.USEREVENT + 1
pygame.time.set_timer(zombie_timer, 1500)

game_start = False

while True:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.MOUSEBUTTONDOWN and white_rectangle.collidepoint(event.pos):
            game_start = True

        if event.type == zombie_timer and game_start:
            zombie_groups.add(Zombie(choice(['naruto', 'naruto', 'sasuke', 'sasuke', 'kakashi']),
                                     position_list_y=[150, 230, 310, 395, 480]))

    if game_active:
        screen.blit(white_surface, white_rectangle)
        screen.blit(welcome_surface, (0, 0))
        screen.blit(username_surface, username_rectangle)

        if game_start:
            screen.blit(background_surface, (0, 0))

            zombie_groups.draw(screen)
            zombie_groups.update()

    pygame.display.update()
    clock.tick(60)

# both
# line (x,y)
# zombie
# xueliang
# yidong shudu

# sound effect (last)

# pokemon
# pikachu(pen dian)
# shui wa (pen shui )
# machine ( tai yang hua) (create ball)


# def zombie( ):

# zombie ( xuelieang  , mibgzi , zhao pian,shudu)
