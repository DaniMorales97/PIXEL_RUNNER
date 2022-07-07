import pygame
import os
import sys
import random
from player import Player
from obstacle import Obstacle


# --------------------------------GLOBAL VARIABLES DEFAULT-------------------------------------#
game_active = False
game_over = False

colliding = False
collision_n = 0

start_time = 1000
score = 0
highscore = 0

WIDTH, HEIGHT, MAX_FPS = (800, 400, 60)


class Game:
    def __init__(self):
        # -----------------------------INITIATE PYGAME AND CLOCK------------------------------------#
        pygame.init()
        self.clock = pygame.time.Clock()

        # -------------------------SCREEN DISPLAY, MUSIC AND BACKGROUND-----------------------------#
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("PIXEL RUNNER")

        background_music_path = os.path.abspath(__file__) + "/../../audio/music.wav"
        background_music = pygame.mixer.Sound(background_music_path)
        background_music.set_volume(0.3)
        background_music.play(-1)

        sky_surface_path = os.path.abspath(__file__) + "/../../graphics/sky.jpg"
        self.sky_surface = pygame.image.load(sky_surface_path).convert()
        ground_surface_path = os.path.abspath(__file__) + "/../../graphics/ground.jpg"
        self.ground_surface = pygame.image.load(ground_surface_path).convert()

        # ----------------------------------TEXT----------------------------------------------------#
        minecraft_font_path = os.path.abspath(__file__) + "/../../fonts/Minecraft.ttf"
        self.name_font = pygame.font.Font(minecraft_font_path, 70)
        self.rest_font = pygame.font.Font(minecraft_font_path, 20)
        self.test_font = pygame.font.Font(minecraft_font_path, 50)

        self.name_surface = self.name_font.render("PIXEL RUNNER", False, "black")
        self.start_surface = self.rest_font.render("CLICK ANYWHERE TO PLAY", False, "black")
        self.score_surface = self.test_font.render("Your score was: " + str(score), False, "black")
        self.game_over_surface = self.test_font.render("GAME OVER", False, "black")
        self.rest_surface = self.rest_font.render("CLICK ANYWHERE TO START AGAIN", False, "black")
        self.highscore_surface = self.rest_font.render("HIGHSCORE: " + str(highscore), False, "black")

        self.name_rect = self.name_surface.get_rect(center=(400, 200))
        self.start_rect = self.start_surface.get_rect(center=(400, 350))
        self.score_rect = self.score_surface.get_rect(center=(400, 100))
        self.game_over_rect = self.game_over_surface.get_rect(center=(400, 200))
        self.rest_rect = self.rest_surface.get_rect(center=(400, 350))
        self.highscore_rect = self.highscore_surface.get_rect(center=(400, 150))

        # -------------------------------SPRITE GROUPS----------------------------------------------#
        self.player = pygame.sprite.GroupSingle()
        self.player.add(Player())

        self.obstacle_group = pygame.sprite.Group()

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

        self.score_surface = self.test_font.render("Your score was: " + str(score), False, "black")
        self.highscore_surface = self.rest_font.render("HIGHSCORE: " + str(highscore), False, "black")

    def collisions(self):
        global collision_n, colliding, game_active, score, highscore

        if pygame.sprite.spritecollide(self.player.sprite, self.obstacle_group, False):
            if not colliding:
                collision_n += 1
                if collision_n < 2:
                    print(3 - collision_n, "lives left")
                elif collision_n == 2:
                    print("1 life left")
                else:
                    print("Game over")
                colliding = True
        else:
            colliding = False

        if collision_n == 3:
            game_active = False
            collision_n = 0

    def run(self):
        global game_active, game_over, start_time
        # ----------------------------------MAIN LOOP-----------------------------------------------#
        while True:
            # -----------------------------EVENT LOOP-----------------------------------------------#
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if game_active:
                    if event.type == self.obstacle_timer:
                        if not random.randrange(0, 4):
                            self.obstacle_group.add(Obstacle("fly"))
                        else:
                            self.obstacle_group.add(Obstacle("snail"))

            if game_active:
                # -------------------------DRAW BACKGROUND------------------------------------------#
                self.screen.blit(self.sky_surface, (0, 0))
                self.screen.blit(self.ground_surface, (0, 300))

                # ------------------------UPDATE AND DRAW SPRITES-----------------------------------#
                self.player.update()
                self.player.draw(self.screen)

                self.obstacle_group.update()
                self.obstacle_group.draw(self.screen)

                # ------------------------------CALL FUNCTIONS--------------------------------------#
                self.collisions()
                self.display_score()

            # --------------------------------START/GAME 0VER SCREEN--------------------------------#
            else:
                self.player.sprite.reset()
                self.obstacle_group.empty()
                self.screen.fill("white")
                if score:
                    self.screen.blit(self.game_over_surface, self.game_over_rect)
                    self.screen.blit(self.score_surface, self.score_rect)
                    self.screen.blit(self.rest_surface, self.rest_rect)

                else:
                    self.screen.blit(self.name_surface, self.name_rect)
                    self.screen.blit(self.start_surface, self.start_rect)

                if highscore:
                    self.screen.blit(self.highscore_surface, self.highscore_rect)

                # ----------------------------(RE)START WITH DELAY----------------------------------#
                if not game_over:
                    pygame.display.update()
                    pygame.time.delay(1000)
                    game_over = True
                else:
                    if pygame.mouse.get_pressed()[0] or pygame.key.get_pressed().__contains__(True):
                        game_active = True
                        game_over = False
                        start_time = pygame.time.get_ticks()

            # -------------------------------UPDATE DISPLAY AND MAX FPS-----------------------------#
            pygame.display.update()
            self.clock.tick(MAX_FPS)
