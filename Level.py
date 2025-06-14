import pygame
from sys import exit
from Database import database
from Stick_of_War import stick_of_war


# pygame.init()
# pygame.font.init()


class GameLevel:
    def __init__(self):
        # pygame.init()
        # pygame.font.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((1000, 600))
        pygame.display.set_caption('Choose Level')

        self.wood_plank_surface = pygame.image.load('Bokemon vs Stick/Picture/utils/wood.png').convert()
        self.wood_plank_surface = pygame.transform.scale(self.wood_plank_surface, (100, 120))
        self.wood_plank_surface_back_and_store = pygame.transform.scale(self.wood_plank_surface, (90, 50))

        self.lock = pygame.image.load('Stick of War/Picture/utils/lock.png')
        self.lock_surf = pygame.transform.scale(self.lock, (100, 100))

        self.one_star = pygame.image.load('Stick of War/Picture/utils/one_star.png')
        self.one_star_surf = pygame.transform.scale(self.one_star, (90, 40))

        self.two_star = pygame.image.load('Stick of War/Picture/utils/two_star.png')
        self.two_star_surf = pygame.transform.scale(self.two_star, (90, 40))

        self.three_star = pygame.image.load('Stick of War/Picture/utils/three_star.png')
        self.three_star_surf = pygame.transform.scale(self.three_star, (90, 40))

        self.level_bg = pygame.image.load('Stick of War/Picture/utils/choose level.png')

        self.go_home_py = False
        self.go_store_py = False
        self.go_stick_of_war = False

        # star rect for all level
        # level one
        self.star_one_rect = self.one_star_surf.get_rect(center=(180, 290))

        # level two
        self.star_two_rect = self.one_star_surf.get_rect(center=(335, 290))

        # level three
        self.star_three_rect = self.one_star_surf.get_rect(center=(495, 290))

        # level four
        self.star_four_rect = self.one_star_surf.get_rect(center=(650, 290))

        # level five
        self.star_five_rect = self.one_star_surf.get_rect(center=(805, 290))

        # level six
        self.star_six_rect = self.one_star_surf.get_rect(center=(180, 470))

        # level seven
        self.star_seven_rect = self.one_star_surf.get_rect(center=(335, 470))

        # level eight
        self.star_eight_rect = self.one_star_surf.get_rect(center=(495, 470))

        # level nine
        self.star_nine_rect = self.one_star_surf.get_rect(center=(650, 470))

        # level ten
        self.star_ten_rect = self.one_star_surf.get_rect(center=(805, 470))

    def choose_level(self, winner, played_time):
        self.wood_plank_rectangle_back = self.wood_plank_surface.get_rect(center=(115, 100))

        self.wood_plank_rectangle_store = self.wood_plank_surface.get_rect(center=(890, 100))

        self.wood_plank_rectangle_one = self.wood_plank_surface.get_rect(center=(180, 230))

        self.wood_plank_rectangle_two = self.wood_plank_surface.get_rect(center=(335, 230))
        self.lock_two_rect = self.lock_surf.get_rect(center=(335, 230))

        self.wood_plank_rectangle_three = self.wood_plank_surface.get_rect(center=(495, 230))
        self.lock_three_rect = self.lock_surf.get_rect(center=(495, 230))

        self.wood_plank_rectangle_four = self.wood_plank_surface.get_rect(center=(650, 230))
        self.lock_four_rect = self.lock_surf.get_rect(center=(650, 230))

        self.wood_plank_rectangle_five = self.wood_plank_surface.get_rect(center=(805, 230))
        self.lock_five_rect = self.lock_surf.get_rect(center=(805, 230))

        self.wood_plank_rectangle_six = self.wood_plank_surface.get_rect(center=(180, 410))
        self.lock_six_rect = self.lock_surf.get_rect(center=(180, 410))

        self.wood_plank_rectangle_seven = self.wood_plank_surface.get_rect(center=(335, 410))
        self.lock_seven_rect = self.lock_surf.get_rect(center=(335, 410))

        self.wood_plank_rectangle_eight = self.wood_plank_surface.get_rect(center=(495, 410))
        self.lock_eight_rect = self.lock_surf.get_rect(center=(495, 410))

        self.wood_plank_rectangle_nine = self.wood_plank_surface.get_rect(center=(650, 410))
        self.lock_nine_rect = self.lock_surf.get_rect(center=(650, 410))

        self.wood_plank_rectangle_ten = self.wood_plank_surface.get_rect(center=(805, 410))
        self.lock_ten_rect = self.lock_surf.get_rect(center=(805, 410))

        if database.stage_level == 1:
            self.screen.blit(self.wood_plank_surface_back_and_store, self.wood_plank_rectangle_back)
            self.screen.blit(self.wood_plank_surface_back_and_store, self.wood_plank_rectangle_store)
            self.screen.blit(self.wood_plank_surface, self.wood_plank_rectangle_one)
            self.screen.blit(self.level_bg, (0, 0))
            self.screen.blit(self.lock_surf, self.lock_two_rect)
            self.screen.blit(self.lock_surf, self.lock_three_rect)
            self.screen.blit(self.lock_surf, self.lock_four_rect)
            self.screen.blit(self.lock_surf, self.lock_five_rect)
            self.screen.blit(self.lock_surf, self.lock_six_rect)
            self.screen.blit(self.lock_surf, self.lock_seven_rect)
            self.screen.blit(self.lock_surf, self.lock_eight_rect)
            self.screen.blit(self.lock_surf, self.lock_nine_rect)
            self.screen.blit(self.lock_surf, self.lock_ten_rect)
            self.achievement(winner, played_time)
            self.blit_star()
        elif database.stage_level == 2:
            self.screen.blit(self.wood_plank_surface_back_and_store, self.wood_plank_rectangle_back)
            self.screen.blit(self.wood_plank_surface_back_and_store, self.wood_plank_rectangle_store)
            self.screen.blit(self.wood_plank_surface, self.wood_plank_rectangle_one)
            self.screen.blit(self.wood_plank_surface, self.wood_plank_rectangle_two)
            self.screen.blit(self.level_bg, (0, 0))
            self.screen.blit(self.lock_surf, self.lock_three_rect)
            self.screen.blit(self.lock_surf, self.lock_four_rect)
            self.screen.blit(self.lock_surf, self.lock_five_rect)
            self.screen.blit(self.lock_surf, self.lock_six_rect)
            self.screen.blit(self.lock_surf, self.lock_seven_rect)
            self.screen.blit(self.lock_surf, self.lock_eight_rect)
            self.screen.blit(self.lock_surf, self.lock_nine_rect)
            self.screen.blit(self.lock_surf, self.lock_ten_rect)
            self.achievement(winner, played_time)
            self.blit_star()
        elif database.stage_level == 3:
            self.screen.blit(self.wood_plank_surface_back_and_store, self.wood_plank_rectangle_back)
            self.screen.blit(self.wood_plank_surface_back_and_store, self.wood_plank_rectangle_store)
            self.screen.blit(self.wood_plank_surface, self.wood_plank_rectangle_one)
            self.screen.blit(self.wood_plank_surface, self.wood_plank_rectangle_two)
            self.screen.blit(self.wood_plank_surface, self.wood_plank_rectangle_three)
            self.screen.blit(self.level_bg, (0, 0))
            self.screen.blit(self.lock_surf, self.lock_four_rect)
            self.screen.blit(self.lock_surf, self.lock_five_rect)
            self.screen.blit(self.lock_surf, self.lock_six_rect)
            self.screen.blit(self.lock_surf, self.lock_seven_rect)
            self.screen.blit(self.lock_surf, self.lock_eight_rect)
            self.screen.blit(self.lock_surf, self.lock_nine_rect)
            self.screen.blit(self.lock_surf, self.lock_ten_rect)
            self.achievement(winner, played_time)
            self.blit_star()
        elif database.stage_level == 4:
            self.screen.blit(self.wood_plank_surface_back_and_store, self.wood_plank_rectangle_back)
            self.screen.blit(self.wood_plank_surface_back_and_store, self.wood_plank_rectangle_store)
            self.screen.blit(self.wood_plank_surface, self.wood_plank_rectangle_one)
            self.screen.blit(self.wood_plank_surface, self.wood_plank_rectangle_two)
            self.screen.blit(self.wood_plank_surface, self.wood_plank_rectangle_three)
            self.screen.blit(self.wood_plank_surface, self.wood_plank_rectangle_four)
            self.screen.blit(self.level_bg, (0, 0))
            self.screen.blit(self.lock_surf, self.lock_five_rect)
            self.screen.blit(self.lock_surf, self.lock_six_rect)
            self.screen.blit(self.lock_surf, self.lock_seven_rect)
            self.screen.blit(self.lock_surf, self.lock_eight_rect)
            self.screen.blit(self.lock_surf, self.lock_nine_rect)
            self.screen.blit(self.lock_surf, self.lock_ten_rect)
            self.achievement(winner, played_time)
            self.blit_star()
        elif database.stage_level == 5:
            self.screen.blit(self.wood_plank_surface_back_and_store, self.wood_plank_rectangle_back)
            self.screen.blit(self.wood_plank_surface_back_and_store, self.wood_plank_rectangle_store)
            self.screen.blit(self.wood_plank_surface, self.wood_plank_rectangle_one)
            self.screen.blit(self.wood_plank_surface, self.wood_plank_rectangle_two)
            self.screen.blit(self.wood_plank_surface, self.wood_plank_rectangle_three)
            self.screen.blit(self.wood_plank_surface, self.wood_plank_rectangle_four)
            self.screen.blit(self.wood_plank_surface, self.wood_plank_rectangle_five)
            self.screen.blit(self.level_bg, (0, 0))
            self.screen.blit(self.lock_surf, self.lock_six_rect)
            self.screen.blit(self.lock_surf, self.lock_seven_rect)
            self.screen.blit(self.lock_surf, self.lock_eight_rect)
            self.screen.blit(self.lock_surf, self.lock_nine_rect)
            self.screen.blit(self.lock_surf, self.lock_ten_rect)
            self.achievement(winner, played_time)
            self.blit_star()
        elif database.stage_level == 6:
            self.screen.blit(self.wood_plank_surface_back_and_store, self.wood_plank_rectangle_back)
            self.screen.blit(self.wood_plank_surface_back_and_store, self.wood_plank_rectangle_store)
            self.screen.blit(self.wood_plank_surface, self.wood_plank_rectangle_one)
            self.screen.blit(self.wood_plank_surface, self.wood_plank_rectangle_two)
            self.screen.blit(self.wood_plank_surface, self.wood_plank_rectangle_three)
            self.screen.blit(self.wood_plank_surface, self.wood_plank_rectangle_four)
            self.screen.blit(self.wood_plank_surface, self.wood_plank_rectangle_five)
            self.screen.blit(self.wood_plank_surface, self.wood_plank_rectangle_six)
            self.screen.blit(self.level_bg, (0, 0))
            self.screen.blit(self.lock_surf, self.lock_seven_rect)
            self.screen.blit(self.lock_surf, self.lock_eight_rect)
            self.screen.blit(self.lock_surf, self.lock_nine_rect)
            self.screen.blit(self.lock_surf, self.lock_ten_rect)
            self.achievement(winner, played_time)
            self.blit_star()
        elif database.stage_level == 7:
            self.screen.blit(self.wood_plank_surface_back_and_store, self.wood_plank_rectangle_back)
            self.screen.blit(self.wood_plank_surface_back_and_store, self.wood_plank_rectangle_store)
            self.screen.blit(self.wood_plank_surface, self.wood_plank_rectangle_one)
            self.screen.blit(self.wood_plank_surface, self.wood_plank_rectangle_two)
            self.screen.blit(self.wood_plank_surface, self.wood_plank_rectangle_three)
            self.screen.blit(self.wood_plank_surface, self.wood_plank_rectangle_four)
            self.screen.blit(self.wood_plank_surface, self.wood_plank_rectangle_five)
            self.screen.blit(self.wood_plank_surface, self.wood_plank_rectangle_six)
            self.screen.blit(self.wood_plank_surface, self.wood_plank_rectangle_seven)
            self.screen.blit(self.level_bg, (0, 0))
            self.screen.blit(self.lock_surf, self.lock_eight_rect)
            self.screen.blit(self.lock_surf, self.lock_nine_rect)
            self.screen.blit(self.lock_surf, self.lock_ten_rect)
            self.achievement(winner, played_time)
            self.blit_star()
        elif database.stage_level == 8:
            self.screen.blit(self.wood_plank_surface_back_and_store, self.wood_plank_rectangle_back)
            self.screen.blit(self.wood_plank_surface_back_and_store, self.wood_plank_rectangle_store)
            self.screen.blit(self.wood_plank_surface, self.wood_plank_rectangle_one)
            self.screen.blit(self.wood_plank_surface, self.wood_plank_rectangle_two)
            self.screen.blit(self.wood_plank_surface, self.wood_plank_rectangle_three)
            self.screen.blit(self.wood_plank_surface, self.wood_plank_rectangle_four)
            self.screen.blit(self.wood_plank_surface, self.wood_plank_rectangle_five)
            self.screen.blit(self.wood_plank_surface, self.wood_plank_rectangle_six)
            self.screen.blit(self.wood_plank_surface, self.wood_plank_rectangle_seven)
            self.screen.blit(self.wood_plank_surface, self.wood_plank_rectangle_eight)
            self.screen.blit(self.level_bg, (0, 0))
            self.screen.blit(self.lock_surf, self.lock_nine_rect)
            self.screen.blit(self.lock_surf, self.lock_ten_rect)
            self.achievement(winner, played_time)
            self.blit_star()
        elif database.stage_level == 9:
            self.screen.blit(self.wood_plank_surface_back_and_store, self.wood_plank_rectangle_back)
            self.screen.blit(self.wood_plank_surface_back_and_store, self.wood_plank_rectangle_store)
            self.screen.blit(self.wood_plank_surface, self.wood_plank_rectangle_one)
            self.screen.blit(self.wood_plank_surface, self.wood_plank_rectangle_two)
            self.screen.blit(self.wood_plank_surface, self.wood_plank_rectangle_three)
            self.screen.blit(self.wood_plank_surface, self.wood_plank_rectangle_four)
            self.screen.blit(self.wood_plank_surface, self.wood_plank_rectangle_five)
            self.screen.blit(self.wood_plank_surface, self.wood_plank_rectangle_six)
            self.screen.blit(self.wood_plank_surface, self.wood_plank_rectangle_seven)
            self.screen.blit(self.wood_plank_surface, self.wood_plank_rectangle_eight)
            self.screen.blit(self.wood_plank_surface, self.wood_plank_rectangle_nine)
            self.screen.blit(self.level_bg, (0, 0))
            self.screen.blit(self.lock_surf, self.lock_ten_rect)
            self.achievement(winner, played_time)
            self.blit_star()
        elif database.stage_level == 10:
            self.screen.blit(self.wood_plank_surface_back_and_store, self.wood_plank_rectangle_back)
            self.screen.blit(self.wood_plank_surface_back_and_store, self.wood_plank_rectangle_store)
            self.screen.blit(self.wood_plank_surface, self.wood_plank_rectangle_one)
            self.screen.blit(self.wood_plank_surface, self.wood_plank_rectangle_two)
            self.screen.blit(self.wood_plank_surface, self.wood_plank_rectangle_three)
            self.screen.blit(self.wood_plank_surface, self.wood_plank_rectangle_four)
            self.screen.blit(self.wood_plank_surface, self.wood_plank_rectangle_five)
            self.screen.blit(self.wood_plank_surface, self.wood_plank_rectangle_six)
            self.screen.blit(self.wood_plank_surface, self.wood_plank_rectangle_seven)
            self.screen.blit(self.wood_plank_surface, self.wood_plank_rectangle_eight)
            self.screen.blit(self.wood_plank_surface, self.wood_plank_rectangle_nine)
            self.screen.blit(self.wood_plank_surface, self.wood_plank_rectangle_ten)
            self.screen.blit(self.level_bg, (0, 0))
            self.achievement(winner, played_time)
            self.blit_star()

    def event_handling(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                database.update_user()
                database.push_data()
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.wood_plank_rectangle_store.collidepoint(pygame.mouse.get_pos()):
                    self.level_select_music.stop()
                    self.go_store_py = True

                if self.wood_plank_rectangle_back.collidepoint(pygame.mouse.get_pos()):
                    self.level_select_music.stop()
                    self.go_home_py = True

                if database.stage_level >= 1:
                    if self.wood_plank_rectangle_one.collidepoint(pygame.mouse.get_pos()):
                        self.level_select_music.stop()
                        database.lvl_choose = 1
                        self.go_stick_of_war = True

                if database.stage_level >= 2:
                    if self.wood_plank_rectangle_two.collidepoint(pygame.mouse.get_pos()):
                        self.level_select_music.stop()
                        database.lvl_choose = 2
                        self.go_stick_of_war = True

                if database.stage_level >= 3:
                    if self.wood_plank_rectangle_three.collidepoint(pygame.mouse.get_pos()):
                        self.level_select_music.stop()
                        database.lvl_choose = 3
                        self.go_stick_of_war = True

                if database.stage_level >= 4:
                    if self.wood_plank_rectangle_four.collidepoint(pygame.mouse.get_pos()):
                        self.level_select_music.stop()
                        database.lvl_choose = 4
                        self.go_stick_of_war = True

                if database.stage_level >= 5:
                    if self.wood_plank_rectangle_five.collidepoint(pygame.mouse.get_pos()):
                        self.level_select_music.stop()
                        database.lvl_choose = 5
                        self.go_stick_of_war = True

                if database.stage_level >= 6:
                    if self.wood_plank_rectangle_six.collidepoint(pygame.mouse.get_pos()):
                        self.level_select_music.stop()
                        database.lvl_choose = 6
                        self.go_stick_of_war = True

                if database.stage_level >= 7:
                    if self.wood_plank_rectangle_seven.collidepoint(pygame.mouse.get_pos()):
                        self.level_select_music.stop()
                        database.lvl_choose = 7
                        self.go_stick_of_war = True

                if database.stage_level >= 8:
                    if self.wood_plank_rectangle_eight.collidepoint(pygame.mouse.get_pos()):
                        self.level_select_music.stop()
                        database.lvl_choose = 8
                        self.go_stick_of_war = True

                if database.stage_level >= 9:
                    if self.wood_plank_rectangle_nine.collidepoint(pygame.mouse.get_pos()):
                        self.level_select_music.stop()
                        database.lvl_choose = 9
                        self.go_stick_of_war = True

                if database.stage_level >= 10:
                    if self.wood_plank_rectangle_ten.collidepoint(pygame.mouse.get_pos()):
                        self.level_select_music.stop()
                        database.lvl_choose = 10
                        self.go_stick_of_war = True

    def blit_star(self):
        if database.stage_level >= 1:
            self.screen.blit(database.star_one_surf, self.star_one_rect)
        if database.stage_level >= 2:
            self.screen.blit(database.star_two_surf, self.star_two_rect)
        if database.stage_level >= 3:
            self.screen.blit(database.star_three_surf, self.star_three_rect)
        if database.stage_level >= 4:
            self.screen.blit(database.star_four_surf, self.star_four_rect)
        if database.stage_level >= 5:
            self.screen.blit(database.star_five_surf, self.star_five_rect)
        if database.stage_level >= 6:
            self.screen.blit(database.star_six_surf, self.star_six_rect)
        if database.stage_level >= 7:
            self.screen.blit(database.star_seven_surf, self.star_seven_rect)
        if database.stage_level >= 8:
            self.screen.blit(database.star_eight_surf, self.star_eight_rect)
        if database.stage_level >= 9:
            self.screen.blit(database.star_nine_surf, self.star_nine_rect)
        if database.stage_level >= 10:
            self.screen.blit(database.star_ten_surf, self.star_ten_rect)

    def achievement(self, winner, played_time):
        if winner == "Enemy":
            if database.lvl_choose != 100:
                database.money += int(10 + database.lvl_choose * 1.3)
                database.lvl_choose = 100
        elif winner == "User":
            if database.lvl_choose == 1:
                if 0 <= played_time <= 120000:
                    database.star_one_surf = self.three_star_surf
                    database.money += (30 + database.lvl_choose * 15)

                elif 120000 < played_time <= 240000:
                    database.star_one_surf = self.two_star_surf
                    database.money += (30 + database.lvl_choose * 5)

                elif played_time > 240000:
                    database.star_one_surf = self.one_star_surf
                    database.money += (20 + database.lvl_choose * 2)

                database.lvl_choose = 100

            if database.lvl_choose == 2:
                if 0 <= played_time <= 120000:
                    database.star_two_surf = self.three_star_surf
                    database.money += (30 + database.lvl_choose * 15)

                elif 120000 < played_time <= 240000:
                    database.star_two_surf = self.two_star_surf
                    database.money += (30 + database.lvl_choose * 5)

                elif played_time > 240000:
                    database.star_two_surf = self.one_star_surf
                    database.money += (20 + database.lvl_choose * 2)

                database.lvl_choose = 100

            if database.lvl_choose == 3:
                if 0 <= played_time <= 120000:
                    database.star_three_surf = self.three_star_surf
                    database.money += (30 + database.lvl_choose * 15)

                elif 120000 < played_time <= 240000:
                    database.star_three_surf = self.two_star_surf
                    database.money += (30 + database.lvl_choose * 5)

                elif played_time > 240000:
                    database.star_three_surf = self.one_star_surf
                    database.money += (20 + database.lvl_choose * 2)

                database.lvl_choose = 100

            if database.lvl_choose == 4:
                if 0 <= played_time <= 120000:
                    database.star_four_surf = self.three_star_surf
                    database.money += (30 + database.lvl_choose * 15)

                elif 120000 < played_time <= 240000:
                    database.star_four_surf = self.two_star_surf
                    database.money += (30 + database.lvl_choose * 5)

                elif played_time > 240000:
                    database.star_four_surf = self.one_star_surf
                    database.money += (20 + database.lvl_choose * 2)

                database.lvl_choose = 100

            if database.lvl_choose == 5:
                if 0 <= played_time <= 120000:
                    database.star_five_surf = self.three_star_surf
                    database.money += (30 + database.lvl_choose * 15)

                elif 120000 < played_time <= 240000:
                    database.star_five_surf = self.two_star_surf
                    database.money += (30 + database.lvl_choose * 5)

                elif played_time > 240000:
                    database.star_five_surf = self.one_star_surf
                    database.money += (20 + database.lvl_choose * 2)

                database.lvl_choose = 100

            if database.lvl_choose == 6:
                if 0 <= played_time <= 120000:
                    database.star_six_surf = self.three_star_surf
                    database.money += (30 + database.lvl_choose * 15)

                elif 120000 < played_time <= 240000:
                    database.star_six_surf = self.two_star_surf
                    database.money += (30 + database.lvl_choose * 5)

                elif played_time >= 240000:
                    database.star_six_surf = self.one_star_surf
                    database.money += (20 + database.lvl_choose * 2)

                database.lvl_choose = 100

            if database.lvl_choose == 7:
                if 0 <= played_time <= 120000:
                    database.star_seven_surf = self.three_star_surf
                    database.money += (30 + database.lvl_choose * 15)

                elif 120000 < played_time <= 240000:
                    database.star_seven_surf = self.two_star_surf
                    database.money += (30 + database.lvl_choose * 5)

                elif played_time >= 240000:
                    database.star_seven_surf = self.one_star_surf
                    database.money += (20 + database.lvl_choose * 2)

                database.lvl_choose = 100

            if database.lvl_choose == 8:
                if 0 <= played_time <= 120000:
                    database.star_eight_surf = self.three_star_surf
                    database.money += (30 + database.lvl_choose * 15)

                elif 120000 < played_time <= 240000:
                    database.star_eight_surf = self.two_star_surf
                    database.money += (30 + database.lvl_choose * 5)

                elif played_time >= 240000:
                    database.star_eight_surf = self.one_star_surf
                    database.money += (20 + database.lvl_choose * 2)

                database.lvl_choose = 100

            if database.lvl_choose == 9:
                if 0 <= played_time <= 120000:
                    database.star_nine_surf = self.three_star_surf
                    database.money += (30 + database.lvl_choose * 15)

                elif 120000 < played_time <= 240000:
                    database.star_nine_surf = self.two_star_surf
                    database.money += (30 + database.lvl_choose * 5)

                elif played_time > 240000:
                    database.star_nine_surf = self.one_star_surf
                    database.money += (20 + database.lvl_choose * 2)

                database.lvl_choose = 100

            if database.lvl_choose == 10:
                if 0 <= played_time <= 120000:
                    database.star_ten_surf = self.three_star_surf
                    database.money += (30 + database.lvl_choose * 15)

                elif 120000 < played_time <= 240000:
                    database.star_ten_surf = self.two_star_surf
                    database.money += (30 + database.lvl_choose * 5)

                elif played_time > 240000:
                    database.star_ten_surf = self.one_star_surf
                    database.money += (20 + database.lvl_choose * 2)

                database.lvl_choose = 100

    def run(self):
        self.level_select_music = pygame.mixer.Sound('Stick of War/Music/level.mp3')
        self.level_select_music.set_volume(0.2)
        self.level_select_music.play(loops=-1)

        while True:
            self.screen.fill((255, 255, 255))

            self.choose_level(stick_of_war.winner, stick_of_war.played_time)

            self.event_handling()

            pygame.display.update()
            self.clock.tick(60)


if __name__ == '__main__':
    GameLevel().run()
