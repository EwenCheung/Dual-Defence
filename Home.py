import pygame
from sys import exit
from Database import database
import time


# pygame.init()
# pygame.font.init()


class LoadingBar:
    def __init__(self, x, y, height, width, colour, border_colour, border_width):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.colour = colour
        self.border_colour = border_colour
        self.border_width = border_width
        self.progress = 0  # the first progress variable is to calculate how much should it be filled in
        # if remove that the loading bar won't work

    def draw_bar(self, screen):
        """"
        first one is draw the behind the loading bar 
        second one is the loading bar
        """
        pygame.draw.rect(screen, self.border_colour, (
            self.x - self.border_width, self.y - self.border_width, self.width + 2 * self.border_width,
            self.height + 2 * self.border_width))
        pygame.draw.rect(screen, self.colour, (self.x, self.y, self.width * self.progress, self.height))


class GameHome:
    def __init__(self):
        # pygame.init()
        # pygame.font.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((1000, 600))
        pygame.display.set_caption('Home Page')
        self.loading_bar = LoadingBar(400, 500, 30, 200, (255, 255, 224), (0, 0, 0), 2)  # Fixed width initialization
        self.progress = 0  # this one is if I put 0.2 it will start the loading bar from 0.2

        self.image = pygame.image.load(
            "Stick of War/Picture/utils/background_photo.jpeg")  # Replace "home_image.jpg" with your image path
        self.image = pygame.transform.scale(self.image, (1000, 600))
        self.image_rect = self.image.get_rect(center=(1000 // 2, 600 // 2))

        self.wood_plank_surface = pygame.image.load('Bokemon vs Stick/Picture/utils/wood.png').convert()
        self.wood_plank_surface = pygame.transform.scale(self.wood_plank_surface, (200, 60))
        self.pokemon_vs_naruto_rect = None
        self.stick_of_war_rect = None

        self.text_box_surface = pygame.image.load('Bokemon vs Stick/Picture/utils/wood.png').convert()
        self.text_box_surface = pygame.transform.scale(self.text_box_surface, (400, 60))

        self.loading = True
        self.finish_loading = False

        self.font = pygame.font.Font(None, 35)
        self.choose_game_to_play = False
        self.choosing_login_method = False
        self.signing_in = False
        self.signing_up = False
        self.login_as_guest = False

        self.retry = False
        self.no_account_found = False
        self.signup_time = None
        self.signin_time = None
        self.retry_time = None
        self.acc_found_time = None
        self.go_pokemon_py = False
        self.go_level_py = False

        # sign up
        self.user_text_box_rectangle = self.text_box_surface.get_rect(center=(500, 250))
        self.ask_username = self.font.render('Create your username', True, (255, 255, 255))
        self.ask_username_rect = self.ask_username.get_rect(center=(500, 200))

        self.pass_text_box_rectangle = self.text_box_surface.get_rect(center=(500, 350))
        self.ask_password = self.font.render("Create your password", True, (255, 255, 255))
        self.ask_password_rect = self.ask_password.get_rect(center=(500, 300))

        self.enter_rectangle = self.wood_plank_surface.get_rect(center=(500, 450))
        self.enter_text = self.font.render("Enter", True, (255, 255, 255))
        self.enter_text_rect = self.enter_text.get_rect(center=self.enter_rectangle.center)

        self.back_rectangle = self.wood_plank_surface.get_rect(center=(100, 100))
        self.back_text = self.font.render("Back", True, (255, 255, 255))
        self.back_text_rect = self.back_text.get_rect(center=self.back_rectangle.center)

        self.sign_up_username = ""
        self.sign_up_password = ""
        self.signup_done = False
        self.key_user = False
        self.key_pass = False

        # sign in
        self.sign_in_user_text_box_rectangle = self.text_box_surface.get_rect(center=(500, 250))
        self.sign_in_ask_username = self.font.render('Type your username', True, (255, 255, 255))
        self.sign_in_ask_username_rect = self.sign_in_ask_username.get_rect(center=(500, 200))

        self.sign_in_pass_text_box_rectangle = self.text_box_surface.get_rect(center=(500, 350))
        self.sign_in_ask_password = self.font.render("Type your password", True, (255, 255, 255))
        self.sign_in_ask_password_rect = self.sign_in_ask_password.get_rect(center=(500, 300))

        self.sign_in_login_rectangle = self.wood_plank_surface.get_rect(center=(500, 450))
        self.sign_in_login_text = self.font.render("Login", True, (255, 255, 255))
        self.sign_in_login_text_rect = self.sign_in_login_text.get_rect(center=self.sign_in_login_rectangle.center)

        self.sign_in_back_rectangle = self.wood_plank_surface.get_rect(center=(100, 100))
        self.sign_in_back_text = self.font.render("Back", True, (255, 255, 255))
        self.sign_in_back_text_rect = self.sign_in_back_text.get_rect(center=self.sign_in_back_rectangle.center)

        self.sign_in_username = ""
        self.sign_in_password = ""
        self.sign_in_key_user = False
        self.sign_in_key_pass = False

    def event_handling(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                database.update_user()
                database.push_data()
                pygame.quit()
                exit()
            elif self.choose_game_to_play and event.type == pygame.MOUSEBUTTONDOWN:
                if self.stick_of_war_rect.collidepoint(pygame.mouse.get_pos()):
                    self.choose_game_to_play = False
                    self.home_music.stop()
                    self.go_level_py = True
                elif self.pokemon_vs_naruto_rect.collidepoint(pygame.mouse.get_pos()):
                    self.choose_game_to_play = False
                    self.home_music.stop()
                    self.go_pokemon_py = True
                elif self.back_rectangle.collidepoint(pygame.mouse.get_pos()):
                    self.choosing_login_method = True
                    self.choose_game_to_play = False
                    database.login_method = None
            elif self.choosing_login_method and event.type == pygame.MOUSEBUTTONDOWN:
                if not self.signing_up and not self.login_as_guest and self.sign_in_rect.collidepoint(pygame.mouse.get_pos()):
                    self.signing_in = True
                    self.choosing_login_method = False
                elif not self.signing_in and not self.login_as_guest and self.sign_up_rect.collidepoint(pygame.mouse.get_pos()):
                    self.signing_up = True
                    self.choosing_login_method = False
                elif not self.signing_in and not self.signing_up and self.login_as_guest_rect.collidepoint(pygame.mouse.get_pos()):
                    self.login_as_guest = True
                    self.choosing_login_method = False

            if self.signing_up:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.user_text_box_rectangle.collidepoint(pygame.mouse.get_pos()):
                        self.key_user = True
                        self.key_pass = False
                    elif self.pass_text_box_rectangle.collidepoint(pygame.mouse.get_pos()):
                        self.key_user = False
                        self.key_pass = True
                    elif self.back_rectangle.collidepoint(pygame.mouse.get_pos()):
                        self.key_user = False
                        self.key_pass = False
                        self.signing_up = False
                        self.choosing_login_method = True
                        self.sign_up_username = ""
                        self.sign_up_password = ""
                    elif self.enter_rectangle.collidepoint(pygame.mouse.get_pos()):
                        self.key_user = False
                        self.key_pass = False
                        if self.sign_up_username != "" and self.sign_up_password != "":
                            database.sign_up(self.sign_up_username, self.sign_up_password)
                            self.signup_time = time.time()
                            self.signup_done = True
                            self.signing_up = False
                            self.choosing_login_method = True
                            self.sign_up_username = ""
                            self.sign_up_password = ""
                        else:
                            self.sign_up_username = ""
                            self.sign_up_password = ""
                            self.retry = True
                            self.retry_time = time.time()
                            self.signing_up = True
                            self.choosing_login_method = False

                if event.type == pygame.KEYDOWN:
                    if self.key_user:
                        if event.key == pygame.K_BACKSPACE:
                            self.sign_up_username = self.sign_up_username[:-1]
                        else:
                            self.sign_up_username += event.unicode
                    elif self.key_pass:
                        if event.key == pygame.K_BACKSPACE:
                            self.sign_up_password = self.sign_up_password[:-1]
                        else:
                            self.sign_up_password += event.unicode

            if self.signing_in:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.sign_in_user_text_box_rectangle.collidepoint(pygame.mouse.get_pos()):
                        self.sign_in_key_user = True
                        self.sign_in_key_pass = False
                    elif self.sign_in_pass_text_box_rectangle.collidepoint(pygame.mouse.get_pos()):
                        self.sign_in_key_user = False
                        self.sign_in_key_pass = True
                    elif self.back_rectangle.collidepoint(pygame.mouse.get_pos()):
                        self.sign_in_key_user = False
                        self.sign_in_key_pass = False
                        self.signing_in = False
                        self.choosing_login_method = True
                        self.sign_in_username = ""
                        self.sign_in_password = ""
                    elif self.sign_in_login_rectangle.collidepoint(pygame.mouse.get_pos()):
                        self.sign_in_key_user = False
                        self.sign_in_key_pass = False
                        find_user = database.sign_in(self.sign_in_username, self.sign_in_password)
                        if find_user:
                            self.signing_in = False
                            self.choosing_login_method = False
                            self.sign_in_username = ""
                            self.sign_in_password = ""
                            self.choose_game_to_play = True
                        elif self.sign_in_username == "" or self.sign_in_password == "":
                            self.sign_in_username = ""
                            self.sign_in_password = ""
                            self.retry = True
                            self.retry_time = time.time()
                            self.signing_in = True
                            self.choosing_login_method = False
                        else:
                            self.sign_in_password = ""
                            self.no_account_found = True
                            self.acc_found_time = time.time()
                            self.signing_in = True
                            self.choosing_login_method = False

                if event.type == pygame.KEYDOWN:
                    if self.sign_in_key_user:
                        if event.key == pygame.K_BACKSPACE:
                            self.sign_in_username = self.sign_in_username[:-1]
                        else:
                            self.sign_in_username += event.unicode
                    elif self.sign_in_key_pass:
                        if event.key == pygame.K_BACKSPACE:
                            self.sign_in_password = self.sign_in_password[:-1]
                        else:
                            self.sign_in_password += event.unicode

            elif self.login_as_guest:
                self.choosing_login_method = False
                self.choose_game_to_play = True
                database.login_method = "Guest"
                self.login_as_guest = False

    def game_start_bg(self):
        self.screen.blit(self.image, self.image_rect)

    def update_progress(self):
        # Simulating loading progress

        if self.progress <= 1:
            self.progress += 0.03
            self.finish_loading = False

        else:
            self.progress = 1
            self.loading = False
            self.finish_loading = True
            self.choosing_login_method = True

        self.loading_bar.progress = self.progress
        self.loading_bar.draw_bar(self.screen)

    def draw_button_with_text(self, surface, rect, text):
        text_surf = self.font.render(text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=rect.center)
        self.screen.blit(surface, rect)
        self.screen.blit(text_surf, text_rect)

    def choose_game(self):
        self.draw_button_with_text(self.wood_plank_surface, self.wood_plank_surface.get_rect(center=(350, 430)), 'Bokomon vs Stick')
        self.pokemon_vs_naruto_rect = self.wood_plank_surface.get_rect(center=(350, 430))

        self.draw_button_with_text(self.wood_plank_surface, self.wood_plank_surface.get_rect(center=(650, 430)), 'Stick of War')
        self.stick_of_war_rect = self.wood_plank_surface.get_rect(center=(650, 430))

        # Draw back button
        self.screen.blit(self.wood_plank_surface, self.back_rectangle)
        self.screen.blit(self.back_text, self.back_text_rect)

    def signing_user(self):
        self.draw_button_with_text(self.wood_plank_surface, self.wood_plank_surface.get_rect(center=(350, 430)), 'Sign Up')
        self.sign_up_rect = self.wood_plank_surface.get_rect(center=(350, 430))

        self.draw_button_with_text(self.wood_plank_surface, self.wood_plank_surface.get_rect(center=(650, 430)), 'Sign In')
        self.sign_in_rect = self.wood_plank_surface.get_rect(center=(650, 430))

        self.draw_button_with_text(self.wood_plank_surface, self.wood_plank_surface.get_rect(center=(500, 300)), 'Login as Guest')
        self.login_as_guest_rect = self.wood_plank_surface.get_rect(center=(500, 300))

    def sign_in(self):
        self.screen.blit(self.sign_in_ask_username, self.sign_in_ask_username_rect)
        self.screen.blit(self.text_box_surface, self.sign_in_user_text_box_rectangle)
        username = self.font.render(self.sign_in_username, True, (255, 255, 255))
        username_rect = username.get_rect(center=self.sign_in_user_text_box_rectangle.center)
        self.screen.blit(username, username_rect.move(0, 0))

        # Draw password elements
        self.screen.blit(self.sign_in_ask_password, self.sign_in_ask_password_rect)
        self.screen.blit(self.text_box_surface, self.sign_in_pass_text_box_rectangle)
        password = self.font.render(self.sign_in_password, True, (255, 255, 255))
        password_rect = password.get_rect(center=self.sign_in_pass_text_box_rectangle.center)
        self.screen.blit(password, password_rect.move(0, 0))

        # Draw login button
        self.screen.blit(self.wood_plank_surface, self.sign_in_login_rectangle)
        self.screen.blit(self.sign_in_login_text, self.sign_in_login_text_rect)

        # Draw back button
        self.screen.blit(self.wood_plank_surface, self.sign_in_back_rectangle)
        self.screen.blit(self.sign_in_back_text, self.sign_in_back_text_rect)

    def sign_up(self):
        # Draw username elements
        self.screen.blit(self.ask_username, self.ask_username_rect)
        self.screen.blit(self.text_box_surface, self.user_text_box_rectangle)
        username = self.font.render(self.sign_up_username, True, (255, 255, 255))
        username_rect = username.get_rect(center=self.user_text_box_rectangle.center)
        self.screen.blit(username, username_rect.move(0, 0))

        # Draw password elements
        self.screen.blit(self.ask_password, self.ask_password_rect)
        self.screen.blit(self.text_box_surface, self.pass_text_box_rectangle)
        password = self.font.render(self.sign_up_password, True, (255, 255, 255))
        password_rect = password.get_rect(center=self.pass_text_box_rectangle.center)
        self.screen.blit(password, password_rect.move(0, 0))

        # Draw enter button
        self.screen.blit(self.wood_plank_surface, self.enter_rectangle)
        self.screen.blit(self.enter_text, self.enter_text_rect)

        # Draw back button
        self.screen.blit(self.wood_plank_surface, self.back_rectangle)
        self.screen.blit(self.back_text, self.back_text_rect)

    def display_message(self):
        if self.signup_done:
            current_time = time.time()
            if current_time - self.signup_time <= 5:  # Show for 5 seconds
                alpha = max(255 - int((current_time - self.signup_time) * 85), 0)  # Gradually decrease alpha
                success_message = self.font.render("Signup Successful! You can signin now", True, (50, 205, 50))
                success_message.set_alpha(alpha)
                success_message_rect = success_message.get_rect(center=(500, 550))
                self.screen.blit(success_message, success_message_rect)
            else:
                self.signup_done = False
        if self.retry:
            current_retry_time = time.time()
            if current_retry_time - self.retry_time <= 3:  # Show for 3 seconds
                alpha = max(255 - int((current_retry_time - self.retry_time) * 85), 0)  # Gradually decrease alpha
                retry_message = self.font.render("Do not leave the field blank", True, (255, 0, 0))
                retry_message.set_alpha(alpha)
                retry_message_rect = retry_message.get_rect(center=(500, 550))
                self.screen.blit(retry_message, retry_message_rect)
            else:
                self.retry = False
        if self.no_account_found:
            current_no_acc_time = time.time()
            if current_no_acc_time - self.acc_found_time <= 3:  # Show for 3 seconds
                alpha = max(255 - int((current_no_acc_time - self.acc_found_time) * 85), 0)  # Gradually decrease alpha
                no_account_message = self.font.render("No such account found, please try again or signup an account", True,
                                                      (255, 0, 0))
                no_account_message.set_alpha(alpha)
                no_account_message_rect = no_account_message.get_rect(center=(500, 550))
                self.screen.blit(no_account_message, no_account_message_rect)
            else:
                self.retry = False

    def run(self):
        self.home_music = pygame.mixer.Sound('Stick of War/Music/home_music.wav')
        self.home_music.set_volume(0.2)
        self.home_music.play(loops=-1)
        while True:
            self.screen.fill((255, 255, 255))

            self.event_handling()
            self.game_start_bg()
            if database.login_method is None:
                if self.loading:
                    self.update_progress()
                elif self.finish_loading:
                    if self.choosing_login_method:
                        self.signing_user()
                    elif self.signing_in:
                        self.sign_in()
                    elif self.signing_up:
                        self.sign_up()
                    elif self.choose_game_to_play:
                        self.choose_game()
            else:
                self.choose_game()
            self.display_message()
            pygame.display.update()
            self.clock.tick(60)


home = GameHome()
if __name__ == '__main__':
    home.run()
