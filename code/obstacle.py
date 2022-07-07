import pygame
import os
import random


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, obstacle_type):
        super().__init__()

        if obstacle_type == "snail":
            snail1_path = os.path.abspath(__file__) + "/../../graphics/snail/snail1.png"
            snail1 = pygame.image.load(snail1_path).convert_alpha()
            snail2_path = os.path.abspath(__file__) + "/../../graphics/snail/snail2.png"
            snail2 = pygame.image.load(snail2_path).convert_alpha()
            self.frames = [snail1, snail2]
            self.d_index = 0.1

            self.y = 300

        if obstacle_type == "fly":
            fly1_path = os.path.abspath(__file__) + "/../../graphics/Fly/Fly1.png"
            fly1 = pygame.image.load(fly1_path).convert_alpha()
            fly2_path = os.path.abspath(__file__) + "/../../graphics/Fly/Fly2.png"
            fly2 = pygame.image.load(fly2_path).convert_alpha()
            self.frames = [fly1, fly2]
            self.d_index = 0.2

            self.y = 200

        self.index = 0
        self.image = self.frames[self.index]
        self.mask = pygame.mask.from_surface(self.image)
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

    def update(self):
        self.animate()
        self.destroy()
