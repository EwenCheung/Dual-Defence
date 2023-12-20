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


log_in_method = input('Sign up an account enter "U" \n'
                      'Sign in an account enter "I"\n'
                      'Log in as guest enter "G"\n\n'
                      'Please enter your choice here :  ').strip().upper()

asking_log_in_method = True
log_in_as = ''

while asking_log_in_method:
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
                print('Successfully registered')
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
import time

pygame.init()  # starting code

screen = pygame.display.set_mode((1000, 600))  # screen size
pygame.display.set_caption('Plant vs Zombie')  # title name
clock = pygame.time.Clock()
game_active = True
bg_music = pygame.mixer.Sound('audio/Plants vs. Zombies (Main Theme).mp3')
bg_music.play(loops=-1)

welcome_fp = create_file_path('Picture/welcome.webp')
welcome_surface = pygame.image.load(welcome_fp).convert()
welcome_surface = pygame.transform.scale(welcome_surface, (1000, 600))

white_fp = create_file_path('Picture/white_screen.jpeg')
white_surface = pygame.image.load(white_fp).convert()
white_surface = pygame.transform.scale(white_surface, (400, 100))
white_rectangle = white_surface.get_rect(topleft=(500, 90))

username_font = pygame.font.Font(None, 30)
username_surface = username_font.render(log_in_as, None, 'White')
username_rectangle = username_surface.get_rect(center=(210, 100))

background_fp = create_file_path('Picture/background 1.webp')
background_surface = pygame.image.load(background_fp).convert()
background_surface = pygame.transform.scale(background_surface, (1000, 600))

zombie_naruto_fp = create_file_path('Picture/zombie_naruto.png')
zombie_naruto_surface = pygame.image.load(zombie_naruto_fp).convert_alpha()
zombie_naruto_surface = pygame.transform.scale(zombie_naruto_surface, (30, 30))
zombie_naruto_rectangle = zombie_naruto_surface.get_rect(center=(100, 200))

game_start = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.MOUSEBUTTONDOWN and white_rectangle.collidepoint(event.pos):
            game_start = True

    if game_active:
        screen.blit(white_surface, white_rectangle)
        screen.blit(welcome_surface, (0, 0))
        screen.blit(username_surface, username_rectangle)
        if game_start:
            time.sleep(1)
            screen.blit(background_surface, (0, 0))
            screen.blit(zombie_naruto_surface,zombie_naruto_rectangle)
    pygame.display.update()
    clock.tick(60)
