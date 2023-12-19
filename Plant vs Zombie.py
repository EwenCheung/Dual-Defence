# coding: utf-8

import os

# Get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the file path relative to the current script
file_path = os.path.join(current_dir, 'Data/user.txt')

print(file_path)

def sign_up(username, password):
    with open(file_path, mode='a') as f:
        f.write(f'{username}----{password}\n')


def check_username_taken(input_username):
    with open(file_path, mode='rt', encoding='utf-8') as f:
        for line in f:
            username, password = line.strip().split('----')
            if input_username == username:
                print('Username Taken, Please choose an another one')
                break
        else:
            return 'y'


def check_user_pass(input_username, input_password):
    with open(file_path, mode='rt', encoding='utf-8') as f:
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

while asking_log_in_method:
    if log_in_method == 'G':  # log in as guest
        print('Logged in as guest')
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
        asking_log_in_method = False

    elif log_in_method == 'I':
        while True:
            input_username = input('Enter your username: ').strip()
            input_password = input('Enter your password: ').strip()
            res = check_user_pass(input_username, input_password)
            if res == 'y':
                print('Logged in')
                break

        asking_log_in_method = False

    else:
        print('Please key in the correct symbol')
