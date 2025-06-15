import ast
import pygame


class Data:
    def __init__(self):
        self.all_user = []
        self.fetch_data()
        self.login_method = None
        self.username = "Guest"
        self.password = "888888"
        self.stage_level = 1
        self.money = 500
        # troop : [have or not, level, equipped or not, health, attack damage, speed, upgrades_price]
        # health = (current health * 1.1)//1
        # attack = (current attack* 1.1)
        # upgrades_price = (current price * 1.1)//1
        self.troop_storage = {
            "warrior": [True, 1, True, 100, 1.2, 1, 150],
            "archer": [False, 1, False, 200, 10, 1.1, 150],
            "wizard": [False, 1, False, 250, 10, 0.8, 200],
            "sparta": [False, 1, False, 300, 2.5, 1, 350],
            "giant": [False, 1, False, 350, 3.5, 0.6, 500]
        }

        # spell :[have or not, level, equpped or not, functionality, upgrades price]
        # rage = rage + 0.05
        # healing = healing + 100
        # freeze = freeze + 0.05
        self.spell_storage = {
            "rage": [False, 1, False, 0.1, 150],
            "healing": [False, 1, False, 100, 150],
            "freeze": [False, 1, False, 0.1, 150]
        }
        # first upgrades for health, second is formining speed level
        # middle two coloum 1000 stand for health and 10 stand for mining speed
        # and the last two coloum first stand for the health upgrades price, second stand for mining speed upgrades price
        self.castle_storage = {
            "default_castle": [True, 1, 1, 1000, 1, 150, 150]  # two upgrades
        }

        self.warrior_gold = 200
        self.warrior_diamond = 0
        self.archer_gold = 300
        self.archer_diamond = 200
        self.wizard_gold = 300
        self.wizard_diamond = 500
        self.sparta_gold = 500
        self.sparta_diamond = 350
        self.giant_gold = 1000
        self.giant_diamond = 500

        self.lvl_choose = 100

        self.no_star = pygame.image.load('Stick of War/Picture/utils/no_star.png')
        self.no_star_surf = pygame.transform.scale(self.no_star, (90, 40))
        self.star_one_surf = self.no_star_surf
        self.star_two_surf = self.no_star_surf
        self.star_three_surf = self.no_star_surf
        self.star_four_surf = self.no_star_surf
        self.star_five_surf = self.no_star_surf
        self.star_six_surf = self.no_star_surf
        self.star_seven_surf = self.no_star_surf
        self.star_eight_surf = self.no_star_surf
        self.star_nine_surf = self.no_star_surf
        self.star_ten_surf = self.no_star_surf

    # sign in and take the info of the data
    def sign_in(self, username, password):
        for user in self.all_user:
            if user["username"] == username and user["password"] == password:
                self.username = user["username"]
                self.password = user["password"]
                self.stage_level = user["stage_level"]
                self.money = user["money"]
                self.troop_storage = user["troop_storage"]
                self.spell_storage = user["spell_storage"]
                self.castle_storage = user["castle_storage"]
                self.login_method = "sign_in"
                return True
        else:
            return False

    # sign up a new account with default info
    def sign_up(self, username, password):
        data = {'username': username,
                'password': password,
                'stage_level': 1,
                'money': 500,
                'troop_storage': {
                    "warrior": [True, 1, True, 100, 1.1, 1, 150],
                    "archer": [False, 1, False, 200, 10, 1.1, 150],
                    "wizard": [False, 1, False, 250, 10, 0.8, 200],
                    "sparta": [False, 1, False, 300, 2.5, 1, 350],
                    "giant": [False, 1, False, 350, 3.5, 0.6, 500]
                },
                'spell_storage': {
                    "rage": [False, 1, False, 0.1, 150],
                    "healing": [False, 1, False, 100, 150],
                    "freeze": [False, 1, False, 0.1, 150]
                },
                'castle_storage': {
                    "default_castle": [True, 1, 1, 1000, 1, 150, 150]  # two upgrades
                }}
        self.all_user.append(data)

    # read current user data
    def read_data(self):
        all_data = {
            "username": self.username,
            "password": self.password,
            "stage_level": self.stage_level,  # can be list if you want else just integer
            "money": self.money,  # money that the user has
            "troop_storage": self.troop_storage,
            "spell_storage": self.spell_storage,
            "castle_storage": self.castle_storage,
        }
        return all_data

    # update user latest info to self.all_user (after update you can push_data)
    def update_user(self):
        all_data = self.read_data()
        for i, user in enumerate(self.all_user):
            if user["username"] == self.username:
                self.all_user[i] = all_data
                break

    # fetch every user from database
    def fetch_data(self):
        with open('database.txt', mode='rt', encoding='utf-8') as f:
            for line in f:
                user_data = ast.literal_eval(line.strip())
                self.all_user.append(user_data)

    def push_data(self):
        with open('database.txt', mode='w', encoding='utf-8') as f:
            for user in self.all_user:
                f.write(f"{user}\n")

    # logout and reset to default guest values
    def logout(self):
        self.login_method = None
        self.username = "Guest"
        self.password = "888888"
        self.stage_level = 1
        self.money = 500
        # Reset troop storage to default values
        self.troop_storage = {
            "warrior": [True, 1, True, 100, 1.2, 1, 150],
            "archer": [False, 1, False, 200, 10, 1.1, 150],
            "wizard": [False, 1, False, 250, 10, 0.8, 200],
            "sparta": [False, 1, False, 300, 2.5, 1, 350],
            "giant": [False, 1, False, 350, 3.5, 0.6, 500]
        }
        # Reset spell storage to default values
        self.spell_storage = {
            "rage": [False, 1, False, 0.1, 150],
            "healing": [False, 1, False, 100, 150],
            "freeze": [False, 1, False, 0.1, 150]
        }
        # Reset castle storage to default values
        self.castle_storage = {
            "default_castle": [True, 1, 1, 1000, 1, 150, 150]
        }

database = Data()