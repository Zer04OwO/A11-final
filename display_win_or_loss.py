import pygame

def display_loss_screen(screen):
    lose_widget = pygame.image.load("WP_lose.png")
    lose_widget = pygame.transform.scale(lose_widget, (2000, 1400))
    lose_widget_rect = lose_widget.get_rect()
    screen.blit(lose_widget, lose_widget_rect)
    pygame.display.update()

def display_win_screen(screen):
    win_widget = pygame.image.load("WP_win.png")
    win_widget = pygame.transform.scale(win_widget, (2000, 1400))
    win_widget_rect = win_widget.get_rect()
    screen.blit(win_widget, win_widget_rect)
    pygame.display.update()
