import asyncio
import sys
import pygame

# Initialize pygame properly for web
pygame.init()
pygame.font.init()
pygame.display.set_caption('Stick_Defend')  # title name
screen = pygame.display.set_mode((1000, 600))

# Import database first
from Database import database

# Global game state variables - will be initialized in main()
home = None
level = None
stick_of_war = None
pokemon_vs_stick = None
run_pokemon_vs_stick = False
run_home = True
run_level = False
run_store = False
run_stick_of_war = False

async def main():
    global home, level, stick_of_war, pokemon_vs_stick
    global run_pokemon_vs_stick, run_home, run_level, run_store, run_stick_of_war

    # Initialize game classes after pygame display is ready
    if home is None:
        print("Initializing game classes...")
        try:
            from Home import GameHome
            home = GameHome()
            print("✅ Home initialized")
            
            from Level import GameLevel
            level = GameLevel()
            print("✅ Level initialized")
            
            from Stick_of_War import GameStickOfWar
            stick_of_war = GameStickOfWar()
            print("✅ Stick_of_War initialized")
            
            from Bokemon_vs_Stick import GamePokemonVsStick
            pokemon_vs_stick = GamePokemonVsStick()
            print("✅ Bokemon_vs_Stick initialized")
            
            print("All game classes initialized successfully!")
        except Exception as e:
            print(f"❌ Error initializing game classes: {e}")
            return

    while True:
        try:
            if run_home:
                # Skip audio loading for web version
                if sys.platform != "emscripten":
                    try:
                        home.home_music = pygame.mixer.Sound('Stick of War/Music/home_music.wav')
                        home.home_music.set_volume(0.2)
                        home.home_music.play(loops=-1)
                    except:
                        pass  # Skip audio if not available
                
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
                    await asyncio.sleep(0)  # Required for Pygbag

            elif run_pokemon_vs_stick:
                pokemon_vs_stick.reset_func()
                # Skip audio loading for web version
                if sys.platform != "emscripten":
                    try:
                        pokemon_vs_stick.bg_music = pygame.mixer.Sound('Bokemon vs Stick/audio/bg_music.mp3')
                        pokemon_vs_stick.bg_music.set_volume(0.1)
                        pokemon_vs_stick.bg_music.play(loops=-1)
                    except:
                        pass  # Skip audio if not available
                
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
                    await asyncio.sleep(0)  # Required for Pygbag

            elif run_level:
                # Skip audio loading for web version
                if sys.platform != "emscripten":
                    try:
                        level.level_select_music = pygame.mixer.Sound('Stick of War/Music/level.mp3')
                        level.level_select_music.set_volume(0.2)
                        level.level_select_music.play(loops=-1)
                    except:
                        pass  # Skip audio if not available

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
                    await asyncio.sleep(0)  # Required for Pygbag

            elif run_store:
                from Store import Game_Store
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
                    await asyncio.sleep(0)  # Required for Pygbag

            elif run_stick_of_war:
                stick_of_war.reset_func()
                # Skip audio loading for web version
                if sys.platform != "emscripten":
                    try:
                        stick_of_war.game_music = pygame.mixer.Sound('Stick of War/Music/game_music.mp3')
                        stick_of_war.game_music.set_volume(0.2)
                        stick_of_war.game_music.play(loops=-1)
                    except:
                        pass  # Skip audio if not available
                
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
                    await asyncio.sleep(0)  # Required for Pygbag
        except Exception as e:
            print(f"Error occurred: {e}")
            database.update_user()
            database.push_data()
            break

asyncio.run(main())
