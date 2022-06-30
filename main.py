import os.path

import pygame
import sys
import random


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        walk1_path = os.path.join(abs_path, "graphics/Player/player_walk_1.png")
        walk1 = pygame.image.load(walk1_path).convert_alpha()
        walk2_path = os.path.join(abs_path, "graphics/Player/player_walk_2.png")
        walk2 = pygame.image.load(walk2_path).convert_alpha()
        self.walk = [walk1, walk2]
        self.index = 0
        jump_path = os.path.join(abs_path, "graphics/Player/jump.png")
        self.jump = pygame.image.load(jump_path).convert_alpha()
        self.image = self.walk[self.index]
        self.rect = self.image.get_rect(midbottom=(100, 300))
        self.dy = 0
        jump_sound_path = os.path.join(abs_path, "audio", "jump.wav")
        self.jump_sound = pygame.mixer.Sound(jump_sound_path)
        self.jump_sound.set_volume(0.2)

    def player_input(self):
        if self.rect.bottom >= 300 and (pygame.key.get_pressed()[pygame.K_SPACE] or (
                self.rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]) or (
                pygame.key.get_pressed()[pygame.K_UP] or pygame.key.get_pressed()[pygame.K_w])):
            self.dy = -20
            self.jump_sound.play()

        if pygame.key.get_pressed()[pygame.K_LEFT] or pygame.key.get_pressed()[pygame.K_a]:
            self.rect.x -= 10
        if pygame.key.get_pressed()[pygame.K_RIGHT] or pygame.key.get_pressed()[pygame.K_d]:
            self.rect.x += 10

        if self.rect.right >= 800:
            self.rect.right = 800
        if self.rect.left <= 0:
            self.rect.left = 0

    def apply_gravity(self):
        self.dy += 1
        self.rect.y += self.dy
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animate(self):
        if self.rect.bottom < 300:
            self.image = self.jump

        else:
            self.index += 0.1
            if self.index >= 2:
                self.index = 0
            self.image = self.walk[int(self.index)]

    def reset(self):
        if not game_active:
            self.rect.midbottom = (100, 300)

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animate()

        if not game_active:
            self.reset()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, obstacle_type):
        super().__init__()

        if obstacle_type == "snail":
            snail1_path = os.path.join(abs_path, "graphics/snail/snail1.png")
            snail1 = pygame.image.load(snail1_path).convert_alpha()
            snail2_path = os.path.join(abs_path, "graphics/snail/snail2.png")
            snail2 = pygame.image.load(snail2_path).convert_alpha()
            self.frames = [snail1, snail2]
            self.y = 300
            self.d_index = 0.1

        if obstacle_type == "fly":
            fly1_path = os.path.join(abs_path, "graphics/Fly/Fly1.png")
            fly1 = pygame.image.load(fly1_path).convert_alpha()
            fly2_path = os.path.join(abs_path, "graphics/Fly/Fly2.png")
            fly2 = pygame.image.load(fly2_path).convert_alpha()
            self.frames = [fly1, fly2]
            self.y = 200
            self.d_index = 0.2

        self.index = 0
        self.image = self.frames[self.index]
        self.rect = self.image.get_rect(midbottom=(random.randint(900, 1100), self.y))

    def animate(self):
        self.index += self.d_index
        if self.index >= 2:
            self.index = 0
        self.image = self.frames[int(self.index)]

        self.rect.x -= 5

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

        if not game_active:
            self.kill()

    def update(self):
        self.animate()
        self.destroy()


def display_score():
    global score, highscore, score_surface, highscore_surface

    running_time = pygame.time.get_ticks()  # Returns the time in ms since pygame.init()
    score_time = int(0.01 * (running_time - start_time))  # start_time will be the time at game start
    text_surface = test_font.render(str(score_time), False, "black")
    text_rect = text_surface.get_rect(center=(400, 100))
    screen.blit(text_surface, text_rect)

    score = score_time
    if score > highscore:
        highscore = score

    score_surface = test_font.render("Your score was: " + str(score), False, "black")
    highscore_surface = restart_font.render("HIGHSCORE: " + str(highscore), False, "black")


def collisions():
    global collision_n, colliding, score, game_active, highscore

    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
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


if __name__ == "__main__":
    # --------------------------------GLOBAL VARIABLES DEFAULT-------------------------------------#
    abs_path = os.path.abspath(os.path.dirname(__file__))

    game_active = False
    game_over = False
    colliding = False
    collision_n = 0

    start_time = 1000
    score = 0
    highscore = 0

    # ---------------------------------INITIATE PYGAME AND CLOCK----------------------------------#
    pygame.init()
    clock = pygame.time.Clock()

    # ----------------------------SCREEN DISPLAY, MUSIC AND BACKGROUND------------------------------#
    screen = pygame.display.set_mode((800, 400))
    pygame.display.set_caption("PIXEL RUNNER")

    background_music_path = os.path.join(abs_path, "audio/music.wav")
    background_music = pygame.mixer.Sound(background_music_path)
    background_music.set_volume(0.3)
    background_music.play(-1)

    sky_surface_path = os.path.join(abs_path, "graphics/sky.jpg")
    sky_surface = pygame.image.load(sky_surface_path).convert()
    ground_surface_path = os.path.join(abs_path, "graphics/ground.jpg")
    ground_surface = pygame.image.load(ground_surface_path).convert()

    # -------------------------------------TEXT------------------------------------------------------#
    minecraft_font_path = os.path.join(abs_path, "fonts/Minecraft.ttf")
    name_font = pygame.font.Font(minecraft_font_path, 70)
    restart_font = pygame.font.Font(minecraft_font_path, 20)
    test_font = pygame.font.Font(minecraft_font_path, 50)

    name_surface = name_font.render("PIXEL RUNNER", False, "black")
    start_surface = restart_font.render("CLICK ANYWHERE TO PLAY", False, "black")
    score_surface = test_font.render("Your score was: " + str(score), False, "black")
    game_over_surface = test_font.render("GAME OVER", False, "black")
    restart_surface = restart_font.render("CLICK ANYWHERE TO START AGAIN", False, "black")
    highscore_surface = restart_font.render("HIGHSCORE: " + str(highscore), False, "black")

    name_rect = name_surface.get_rect(center=(400, 200))
    start_rect = start_surface.get_rect(center=(400, 350))
    score_rect = score_surface.get_rect(center=(400, 100))
    game_over_rect = game_over_surface.get_rect(center=(400, 200))
    restart_rect = restart_surface.get_rect(center=(400, 350))
    highscore_rect = highscore_surface.get_rect(center=(400, 150))

    # ------------------------------SPRITE GROUPS--------------------------------------------------#
    player = pygame.sprite.GroupSingle()
    player.add(Player())

    obstacle_group = pygame.sprite.Group()

    # ------------------------------------TIMER-----------------------------------------------------#
    obstacle_timer = pygame.USEREVENT + 1
    pygame.time.set_timer(obstacle_timer, 1100)

    # ----------------------------------MAIN LOOP---------------------------------------------------#
    while True:
        # -----------------------------EVENT LOOP---------------------------------------------------#
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if game_active:
                if event.type == obstacle_timer:
                    obstacle_group.add(Obstacle(random.choice(["snail", "snail", "snail", "fly"])))

        if game_active:
            # -------------------------DRAW BACKGROUND----------------------------------------------#
            screen.blit(sky_surface, (0, 0))
            screen.blit(ground_surface, (0, 300))

            # ------------------------UPDATE AND DRAW SPRITES---------------------------------------#
            player.update()
            player.draw(screen)

            obstacle_group.update()
            obstacle_group.draw(screen)

            # ------------------------------CALL FUNCTIONS-------------------------------------------#
            collisions()
            display_score()

        # --------------------------------START/GAME 0VER SCREEN-------------------------------------#
        else:
            player.update()
            obstacle_group.update()
            screen.fill("white")
            if score:
                screen.blit(game_over_surface, game_over_rect)
                screen.blit(score_surface, score_rect)
                screen.blit(restart_surface, restart_rect)

            else:
                screen.blit(name_surface, name_rect)
                screen.blit(start_surface, start_rect)

            if highscore:
                screen.blit(highscore_surface, highscore_rect)

            # ----------------------------(RE)START WITH DELAY-------------------------------------#
            if not game_over:
                pygame.display.update()
                pygame.time.delay(1000)
                game_over = True
            else:
                if pygame.mouse.get_pressed()[0] or pygame.key.get_pressed().__contains__(True):
                    game_active = True
                    game_over = False
                    start_time = pygame.time.get_ticks()

        # -------------------------------UPDATE DISPLAY AND MAX FPS---------------------------------#
        pygame.display.update()
        clock.tick(60)
