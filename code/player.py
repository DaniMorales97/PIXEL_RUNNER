import os.path
import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.screen = pygame.display.get_surface()

        walk1_path = os.path.dirname(__file__) + "/../graphics/Player/player_walk_1.png"
        walk1 = pygame.image.load(walk1_path).convert_alpha()
        walk2_path = os.path.dirname(__file__) + "/../graphics/Player/player_walk_2.png"
        walk2 = pygame.image.load(walk2_path).convert_alpha()
        self.walk = [walk1, walk2]
        self.index = 0

        jump_path = os.path.dirname(__file__) + "/../graphics/Player/jump.png"
        self.jump = pygame.image.load(jump_path).convert_alpha()

        self.image = self.walk[self.index]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(midbottom=(100, 300))

        jump_sound_path = os.path.dirname(__file__) + "/../audio/jump.wav"
        self.jump_sound = pygame.mixer.Sound(jump_sound_path)
        self.jump_sound.set_volume(0.2)

        self.dy = 0

        self.right_arrow = pygame.Surface((50, 50), pygame.SRCALPHA)
        pygame.draw.polygon(self.right_arrow, "grey", ((0, 0), (0, 50), (50, 25)))
        self.right_arrow.set_alpha(200)
        self.right_arrow_rect = self.right_arrow.get_rect(center=(680, 350))

        self.left_arrow = pygame.transform.flip(self.right_arrow, True, False)
        self.left_arrow.set_alpha(200)
        self.left_arrow_rect = self.left_arrow.get_rect(center=(600, 350))

    def draw_arrows(self):
        self.screen.blit(self.right_arrow, self.right_arrow_rect)
        self.screen.blit(self.left_arrow, self.left_arrow_rect)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if self.rect.bottom >= 300 and (
            keys[pygame.K_SPACE] or
            (pygame.mouse.get_pressed()[0] and not (
                self.left_arrow_rect.collidepoint(pygame.mouse.get_pos()) or
                self.right_arrow_rect.collidepoint(pygame.mouse.get_pos())
            )) or
            keys[pygame.K_UP] or
            keys[pygame.K_w]
        ):
            self.dy = -20
            self.jump_sound.play()

        if (
            keys[pygame.K_LEFT] or
            keys[pygame.K_a] or
            (pygame.mouse.get_pressed()[0] and
                self.left_arrow_rect.collidepoint(pygame.mouse.get_pos()))
        ):
            self.rect.x -= 10

        if (
            keys[pygame.K_RIGHT] or
            keys[pygame.K_d] or
            (pygame.mouse.get_pressed()[0] and
                self.right_arrow_rect.collidepoint(pygame.mouse.get_pos()))
        ):
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
        self.rect.midbottom = (100, 300)

    def update(self):
        self.draw_arrows()
        self.player_input()
        self.apply_gravity()
        self.animate()
