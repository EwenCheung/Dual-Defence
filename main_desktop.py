import subprocess
import sys


def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])


try:
    import pygame
except ImportError:
    install("pygame")
    import pygame

pygame.init()
pygame.font.init()
pygame.display.set_caption('Stick_Defend')  # title name
pygame.display.set_mode((1000, 600))
from Database import database
from Bokemon_vs_Stick import GamePokemonVsStick
from Home import GameHome
from Level import GameLevel
from Store import Game_Store
from Stick_of_War import GameStickOfWar

home = GameHome()
level = GameLevel()
stick_of_war = GameStickOfWar()
pokemon_vs_stick = GamePokemonVsStick()
run_pokemon_vs_stick = False
run_home = True
run_level = False
run_store = False
run_stick_of_war = False


def main():
    global home
    global level
    global stick_of_war
    global run_pokemon_vs_stick
    global run_home
    global run_level
    global run_store
    global run_stick_of_war

    while True:
        try:
            if run_home:
                home.home_music = pygame.mixer.Sound('Stick of War/Music/home_music.wav')
                home.home_music.set_volume(0.2)
                home.home_music.play(loops=-1)
                while True:
                    home.screen.fill((255, 255, 255))

                    home.event_handling()
                    home.game_start_bg()
                    if home.go_pokemon_py:
                        run_home = False
                        run_pokemon_vs_stick = True
                        home.go_pokemon_py = False
                        break
                    if home.go_level_py:
                        run_home = False
                        run_level = True
                        home.go_level_py = False
                        break
                    if database.login_method is None:
                        if home.loading:
                            home.update_progress()
                        elif home.finish_loading:
                            if home.choosing_login_method:
                                home.signing_user()
                            elif home.signing_in:
                                home.sign_in()
                            elif home.signing_up:
                                home.sign_up()
                            elif home.choose_game_to_play:
                                home.choose_game()
                    else:
                        home.choose_game()
                    home.display_message()
                    pygame.display.update()
                    home.clock.tick(60)

            elif run_pokemon_vs_stick:
                pokemon_vs_stick.reset_func()
                pokemon_vs_stick.bg_music = pygame.mixer.Sound('Bokemon vs Stick/audio/bg_music.mp3')
                pokemon_vs_stick.bg_music.set_volume(0.1)
                pokemon_vs_stick.bg_music.play(loops=-1)
                while True:
                    if pokemon_vs_stick.go_home_py:
                        run_home = True
                        run_pokemon_vs_stick = False
                        pokemon_vs_stick.go_home_py = False
                        home.choose_game_to_play = True
                        home.choosing_login_method = False
                        database.update_user()
                        database.push_data()
                        break

                    # Clear screen
                    pokemon_vs_stick.screen.fill((255, 255, 255))

                    # event_handling_control_function
                    pokemon_vs_stick.event_handling()

                    # start function which will blit screen and etc
                    pokemon_vs_stick.game_start()

                    pygame.display.update()
                    pygame.display.flip()  # redraw the screen

                    pokemon_vs_stick.clock.tick(60)  # 60 fps

            elif run_level:
                level.level_select_music = pygame.mixer.Sound('Stick of War/Music/level.mp3')
                level.level_select_music.set_volume(0.2)
                level.level_select_music.play(loops=-1)

                while True:
                    if level.go_store_py:
                        run_level = False
                        run_store = True
                        level.go_store_py = False
                        break
                    elif level.go_home_py:
                        run_level = False
                        run_home = True
                        level.go_home_py = False
                        home.choose_game_to_play = True
                        home.choosing_login_method = False
                        database.update_user()
                        database.push_data()
                        break
                    elif level.go_stick_of_war:
                        run_level = False
                        run_stick_of_war = True
                        level.go_stick_of_war = False
                        break

                    level.screen.fill((255, 255, 255))

                    level.choose_level(stick_of_war.winner, stick_of_war.played_time)

                    level.event_handling()

                    pygame.display.update()
                    level.clock.tick(60)

            elif run_store:
                store = Game_Store()
                while True:
                    if store.go_level_py:
                        run_store = False
                        run_level = True
                        store.go_level_py = False
                        break
                    store.screen.fill((255, 255, 255))

                    store.event_handling()
                    store.game_start()
                    pygame.display.update()
                    store.clock.tick(60)

            elif run_stick_of_war:
                stick_of_war.reset_func()
                stick_of_war.game_music = pygame.mixer.Sound('Stick of War/Music/game_music.mp3')
                stick_of_war.game_music.set_volume(0.2)
                stick_of_war.game_music.play(loops=-1)
                while True:
                    if stick_of_war.go_level_py:
                        run_level = True
                        run_stick_of_war = False
                        stick_of_war.go_level_py = False
                        break
                    stick_of_war.game_start()
                    stick_of_war.event_handling()

                    pygame.display.update()  # Update the display
                    stick_of_war.clock.tick(60)  # Limit frame rate to 60 FPS
        except:
            database.update_user()
            database.push_data()
            break


if __name__ == "__main__":
    main()
