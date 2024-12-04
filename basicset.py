#This file includes some basic function that apply to every level
import pygame

def pixel_collision(mask1, rect1, mask2, rect2):
    """
    Check if the non-transparent pixels of one mask contacts the non-transparent pixels of another.
    """
    offset_x = rect2[0] - rect1[0]
    offset_y = rect2[1] - rect1[1]
    # See if the two masks at the offset are overlapping.
    overlap = mask1.overlap(mask2, (offset_x, offset_y))
    return overlap != None

class Player:
    def __init__(self):
        self.image = pygame.image.load("steve.png")
        self.image = pygame.transform.smoothscale(self.image, (100, 100))
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.is_alive = True
        self.attack = 0

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def move(self, position):
        self.rect.center = position

class Enemy:
    def __init__(self, image):
        self.image = pygame.image.load(image)
        self.image = pygame.transform.smoothscale(self.image, (150, 180))
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.is_alive = True
        self.attack = 0

    def draw(self, screen, font):
        screen.blit(self.image, self.rect)
        label_hp = font.render(f"ATK: {self.attack}", True, (255, 0, 0))
        screen.blit(label_hp, (self.rect.center[0] - 120, self.rect.center[0] - 150))

    def move(self, position):
        self.rect.center = position