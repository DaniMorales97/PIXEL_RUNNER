import pygame
import asyncio
import os
import sys
import random
import json
import string
from datetime import datetime
from code.player import Player
from code.obstacle import Obstacle
# from code.highscore_screen import highscore_screen


# --------------------------------GLOBAL VARIABLES DEFAULT-------------------------------------#
game_active = False
game_over = False
pressing = True
show_highscore_screen = False

colliding = False
collision_n = 0

start_time = 0
score = 0
highscore = 0
str_list = []
name = ""

WIDTH, HEIGHT, MAX_FPS = (800, 400, 60)


class Game:
    def __init__(self):
        # --------------------------------LOAD HIGHSCORE--------------------------------------------#
        self.data = {}
        self.load_highscore()

        # -----------------------------INITIATE PYGAME AND CLOCK------------------------------------#
        pygame.init()
        self.clock = pygame.time.Clock()
        self.fps = 0

        # -------------------------SCREEN DISPLAY, MUSIC AND BACKGROUND-----------------------------#
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("PIXEL RUNNER")

        background_music_path = os.path.dirname(__file__) + "/../audio/music.wav"
        background_music = pygame.mixer.Sound(background_music_path)
        background_music.set_volume(0.3)
        background_music.play(-1)

        sky_surface_path = os.path.dirname(__file__) + "/../graphics/sky.jpg"
        self.sky_surface = pygame.image.load(sky_surface_path).convert()
        ground_surface_path = os.path.dirname(__file__) + "/../graphics/ground.jpg"
        self.ground_surface = pygame.image.load(ground_surface_path).convert()

        # ----------------------------------TEXT----------------------------------------------------#
        minecraft_font_path = os.path.dirname(__file__) + "/../fonts/Minecraft.ttf"
        self.name_font = pygame.font.Font(minecraft_font_path, 70)
        self.rest_font = pygame.font.Font(minecraft_font_path, 20)
        self.test_font = pygame.font.Font(minecraft_font_path, 50)

        self.name_surface = self.name_font.render("PIXEL RUNNER", False, "black")
        self.start_surface = self.rest_font.render("CLICK ANYWHERE TO PLAY", False, "black")
        self.score_surface = self.test_font.render("Your score was: " + str(score), False, "black")
        self.game_over_surface = self.test_font.render("GAME OVER", False, "black")
        self.rest_surface = self.rest_font.render("CLICK ANYWHERE TO START AGAIN", False, "black")
        self.highscore_surface = self.rest_font.render(f"HIGHSCORE: {highscore}", False, "black")

        self.name_rect = self.name_surface.get_rect(center=(400, 200))
        self.start_rect = self.start_surface.get_rect(center=(400, 350))
        self.score_rect = self.score_surface.get_rect(center=(400, 100))
        self.game_over_rect = self.game_over_surface.get_rect(center=(400, 200))
        self.rest_rect = self.rest_surface.get_rect(center=(400, 350))
        self.highscore_rect = self.highscore_surface.get_rect(center=(400, 150))

        # -------------------------------SPRITE GROUPS----------------------------------------------#
        self.player = pygame.sprite.GroupSingle()
        self.player.add(Player())

        self.obstacles = pygame.sprite.Group()

        # -----------------------------------TIMER--------------------------------------------------#
        self.obstacle_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.obstacle_timer, 1100)

    # ---------------------------------DEFINE FUNCTIONS---------------------------------------------#
    def display_score(self):
        global score, highscore

        running_time = pygame.time.get_ticks()  # Returns the time in ms since pygame.init()
        score = int(0.01 * (running_time - start_time))  # start_time will the time at game start
        text_surface = self.test_font.render(str(score), False, "black")
        text_rect = text_surface.get_rect(center=(400, 100))
        self.screen.blit(text_surface, text_rect)

        if score > highscore:
            highscore = score

    """def display_fps(self):
        self.fps = self.clock.get_fps()
        fps_surface = self.rest_font.render(str(round(self.fps)), False, "black")
        fps_rect = fps_surface.get_rect(center=(50, 100))
        self.screen.blit(fps_surface, fps_rect)"""

    def collisions(self):
        global collision_n, colliding, game_active, score, highscore

        heart_path = os.path.dirname(__file__) + "/../graphics/heart.png"
        heart_surface = pygame.image.load(heart_path)
        heart_surface = pygame.transform.rotozoom(heart_surface, 0, 0.075).convert_alpha()

        self.screen.blit(heart_surface, (20, 20))
        if collision_n < 2:
            self.screen.blit(heart_surface, (20 + heart_surface.get_width(), 20))
            if collision_n < 1:
                self.screen.blit(heart_surface, (20 + 2 * heart_surface.get_width(), 20))

        collided = [bool(pygame.sprite.collide_mask(self.player.sprite, obstacle))
                    for obstacle in self.obstacles.sprites()]  # list of True|False for each obstacle
        if collided.__contains__(True):
            if not colliding:
                collision_n += 1
                colliding = True

        else:
            colliding = False

        if collision_n == 3:
            game_active = False
            collision_n = 0
            self.player.sprite.reset()
            self.obstacles.empty()

    def save_highscore(self):
        # from code.highscore_screen import name
        global highscore, name, show_highscore_screen

        show_highscore_screen = False

        now = datetime.now()
        self.data[f"{now.strftime('%d/%m/%y %H:%M:%S')} - {name}"] = highscore

        file_path = f"{os.path.dirname(__file__)}/highscore.txt"
        with open(file_path, "w") as file:
            json.dump(self.data, file)

    def load_highscore(self):
        global highscore

        file_path = f"{os.path.dirname(__file__)}/highscore.txt"
        try:
            with open(file_path) as file:
                self.data = json.load(file)
                highscore = max(self.data.values())

        except (json.decoder.JSONDecodeError, FileNotFoundError):
            pass

    def highscore_screen(self):
        global pressing, name
        self.screen.fill("white")

        keys = pygame.key.get_pressed()
        if not pressing:
            for character in (string.ascii_lowercase + string.digits):
                if eval(f"keys[pygame.K_{character}]"):
                    str_list.append(character.upper())
                    pressing = True

            if keys[pygame.K_SPACE]:
                str_list.append(" ")
                pressing = True
            elif keys[pygame.K_BACKSPACE]:
                str_list.pop()
                pressing = True
            elif keys[pygame.K_RETURN]:
                self.save_highscore()
                str_list.clear()

        elif not keys.__contains__(True):
            pressing = False

        name = "".join(letter for letter in str_list)

        text1 = "WELL DONE!"
        text2 = "YOU MADE A HIGH SCORE!"
        text3 = "Please enter your name:"
        text4 = f"{name}"
        texts = [text1, text2, text3, text4]

        (x, y) = (400, 50)
        for text in texts:
            surface = self.test_font.render(text, False, "black")
            rect = surface.get_rect(center=(x, y))
            self.screen.blit(surface, rect)
            y += 100

        exit_surface = pygame.Surface((50, 50))
        exit_surface.fill("red")
        exit_rect = exit_surface.get_rect(center=(20, 20))
        self.screen.blit(exit_surface, exit_rect)

        if exit_rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            name = "-"
            self.save_highscore()
            str_list.clear()

    async def run(self):
        global game_active, game_over, start_time, score, highscore, show_highscore_screen
        # ----------------------------------MAIN LOOP-----------------------------------------------#
        while True:
            # -----------------------------EVENT LOOP-----------------------------------------------#
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                """if event.type == pygame.VIDEORESIZE:  # This allows for full screen
                    self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)"""

                if game_active:
                    if event.type == self.obstacle_timer:
                        if not random.randrange(0, 4):
                            self.obstacles.add(Obstacle("fly"))
                        else:
                            self.obstacles.add(Obstacle("snail"))

            if game_active:
                # -------------------------DRAW BACKGROUND------------------------------------------#
                self.screen.blit(self.sky_surface, (0, 0))
                self.screen.blit(self.ground_surface, (0, 300))

                # ------------------------UPDATE AND DRAW SPRITES-----------------------------------#
                self.player.update()
                self.player.draw(self.screen)

                self.obstacles.update()
                self.obstacles.draw(self.screen)

                # ------------------------------CALL FUNCTIONS--------------------------------------#
                self.collisions()
                self.display_score()

            # --------------------------------START/GAME 0VER SCREEN--------------------------------#
            else:
                self.screen.fill("white")
                if show_highscore_screen:
                    self.highscore_screen()

                elif score:
                    max_score = max(self.data.values()) if self.data.values() else 0
                    if highscore > max_score:
                        show_highscore_screen = True

                    else:
                        score_text = f"Your score was: {score}"
                        self.score_surface = self.test_font.render(score_text, False, "black")
                        highscorer = [key for key, value in self.data.items()
                                      if value == max(self.data.values())][0][20:]
                        highscore_text = f"HIGHSCORE: {highscore} - {highscorer}"
                        self.highscore_surface = self.rest_font.render(highscore_text, False, "black")
                        self.highscore_rect = self.highscore_surface.get_rect(center=(400, 150))

                        self.screen.blit(self.game_over_surface, self.game_over_rect)
                        self.screen.blit(self.score_surface, self.score_rect)
                        self.screen.blit(self.highscore_surface, self.highscore_rect)
                        self.screen.blit(self.rest_surface, self.rest_rect)

                else:
                    self.screen.blit(self.name_surface, self.name_rect)
                    self.screen.blit(self.start_surface, self.start_rect)

                # ----------------------------(RE)START WITH DELAY----------------------------------#
                if not show_highscore_screen:
                    if score and not game_over:
                        if not (
                            pygame.key.get_pressed().__contains__(True) or pygame.mouse.get_pressed()[0]
                        ):
                            game_over = True

                    else:
                        if pygame.mouse.get_pressed()[0] or pygame.key.get_pressed().__contains__(True):
                            game_active = True
                            game_over = False
                            start_time = pygame.time.get_ticks()

            # -------------------------------UPDATE DISPLAY AND MAX FPS-----------------------------#
            # self.display_fps()
            pygame.display.update()
            self.clock.tick(MAX_FPS)
            await asyncio.sleep(0)
