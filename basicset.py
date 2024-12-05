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
    '''
    Create player and related actions
    '''
    def __init__(self):
        '''
        Initialize the player
        '''
        self.image = pygame.image.load("steve.png")
        self.image = pygame.transform.smoothscale(self.image, (100, 100))
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.is_alive = True
        self.attack = 0
        self.tp_mode = False

    def draw(self, screen):
        '''
        Draw the player on the screen
        :param screen: screen to draw player on
        :return: None
        '''
        screen.blit(self.image, self.rect)

    def move(self, position):
        '''
        Move player to a certain location
        :param position: Target location of movement
        :return: None
        '''
        self.rect.center = position

    def tp(self):
        '''
        Change the player to black and white if tp mode is on, only used in level 3
        :return: None
        '''
        if self.tp_mode == False:
            self.image = pygame.image.load("steve_tp_mode.png")
            self.image = pygame.transform.smoothscale(self.image, (100, 100))
            self.image = self.image.convert_alpha()
            self.rect = self.image.get_rect()
            self.mask = pygame.mask.from_surface(self.image)
            self.tp_mode = True
        else:
            self.image = pygame.image.load("steve.png")
            self.image = pygame.transform.smoothscale(self.image, (100, 100))
            self.image = self.image.convert_alpha()
            self.rect = self.image.get_rect()
            self.mask = pygame.mask.from_surface(self.image)
            self.tp_mode = False

class Enemy:
    '''
    Create enemy
    '''
    def __init__(self, image):
        '''
        Initialize the enemies
        :param image: a photo for your lovely enemy
        '''
        self.image = pygame.image.load(image)
        self.image = pygame.transform.smoothscale(self.image, (150, 180))
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.is_alive = True
        self.attack = 0

    def draw(self, screen, font, color):
        '''
        Draw the enemy on the screen with their attack number above their head
        :param screen: screen to draw on
        :param font: the font setting to draw the words
        :param color: the color of your font
        :return: None
        '''
        screen.blit(self.image, self.rect)
        label_hp = font.render(f"ATK: {self.attack}", True, color)
        screen.blit(label_hp, (self.rect.center[0] - 120, self.rect.center[1] - 150))

    def move(self, position):
        '''
        move your enemy to a location, seem useless
        :param position: destination
        :return: None
        '''
        self.rect.center = position

class Sprite:
    '''
    Parent class of many other classes, don't ask me why I didn't make enemy and player the inheritage of this class,
    I forgot. ＞﹏＜
    '''
    def __init__(self, image, size):
        '''
        Initialize the image, size and sort of things
        :param image: the picture of object/character
        :param size: size of element you want to be
        '''
        self.image = pygame.image.load(image)
        self.image = pygame.transform.smoothscale(self.image, size)
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.active = True

    def draw(self, screen):
        '''
        Draw on the screen
        :param screen: screen to draw on
        :return: None
        '''
        screen.blit(self.image, self.rect)

    def move(self, position):
        '''
        Move to position
        :param position: destination on screen
        :return: None
        '''
        self.rect.center = position

class EyeOfEnd(Sprite):
    '''
    Level 2 keys
    '''
    def __init__(self, image, size, location):
        super().__init__(image, size)
        self.rect.center = location

class Fireball(Sprite):
    '''
    Level 2 challenges
    '''
    def __init__(self, image, size):
        super().__init__(image, size)
        self.rect.center = (1900, 700)

    def update(self, screen):
        self.rect.center = (self.rect.center[0] - 20, self.rect.center[1])
        screen.blit(self.image, self.rect)

class ChorusFruit(Sprite):
    '''
    Level 3 challenges
    '''
    def __init__(self, image, size, location):
        super().__init__(image, size)
        self.rect.center = location
        self.touched = False

class Tool(Sprite):
    '''
    Tools, only used in level 3 because only level 3 need multiple tools
    '''
    def __init__(self, location):
        super().__init__("tool.png", (150, 150))
        self.rect.center = location
        self.touched = False