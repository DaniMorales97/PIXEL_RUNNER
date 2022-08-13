import os.path

import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
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

    def player_input(self):
        keys = pygame.key.get_pressed()
        if self.rect.bottom >= 300 and (keys[pygame.K_SPACE] or (
                self.rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]) or (
                keys[pygame.K_UP] or keys[pygame.K_w])):
            self.dy = -20
            self.jump_sound.play()

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= 10
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
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
        self.player_input()
        self.apply_gravity()
        self.animate()
