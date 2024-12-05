from idlelib.browser import transform_children

import pygame, sys, display_win_or_loss
from basicset import *

def level1():
    pygame.init()

    # Load the path for player and the barrier.
    map_barrier = pygame.image.load("MP_level1_barrier.png")
    map_barrier = pygame.transform.smoothscale(map_barrier, (2000, 1400))
    map_path = pygame.image.load("MP_level1_path.png")
    map_path = pygame.transform.smoothscale(map_path, (2000, 1400))
    map_size = map_barrier.get_size()

    # create the window based on the map size
    screen = pygame.display.set_mode(map_size)

    # Get element for maps

    map_barrier = map_barrier.convert_alpha()
    barrier_rect = map_barrier.get_rect()
    barrier_mask = pygame.mask.from_surface(map_barrier)
    path_rect = map_path.get_rect()

    # load image of interactive element and get necessary elements
    tool = pygame.image.load("tool.png")
    tool = pygame.transform.scale(tool, (100, 100))
    tool_rect = tool.get_rect()
    tool_rect.center = (1700, 300)
    tool_mask = pygame.mask.from_surface(tool)

    # load start signs
    start = pygame.image.load("start.png")
    start = pygame.transform.scale(start, (100, 100))
    start_rect = start.get_rect()
    start_rect.center = (100, 300)
    start_mask = pygame.mask.from_surface(start)

    # load player file and get elements of it
    player = Player()

    # load enemy file and get elements of it
    zombie_1 = Enemy("zombie.png")

    # load destination (activated/not activated)
    nether_gate_activated = pygame.image.load("nether_gate_on.png")
    nether_gate_activated = pygame.transform.scale(nether_gate_activated, (100, 150))
    nether_gate_activated_rect = nether_gate_activated.get_rect()
    nether_gate_activated_rect.center = (1900, 900)
    nether_gate_activated_mask = pygame.mask.from_surface(nether_gate_activated)
    # not activated
    nether_gate_not_activated = pygame.image.load("nether_gate_off.png")
    nether_gate_not_activated = pygame.transform.scale(nether_gate_not_activated, (100, 150))
    nether_gate_not_activated_rect = nether_gate_not_activated.get_rect()
    nether_gate_not_activated_rect.center = (1900, 900)

    # load lighter/key
    lighter = pygame.image.load("lighter.png")
    lighter = pygame.transform.scale(lighter, (100, 100))
    lighter_rect = lighter.get_rect()
    lighter_rect.center = (300, 1100)
    lighter_mask = pygame.mask.from_surface(lighter)

    # Get a font to use to write on the screen.
    message_font = pygame.font.SysFont('bold', 100)

    # Hide the arrow cursor and replace it with a sprite.
    pygame.mouse.set_visible(False)

    # The clock helps us manage the frames per second of the animation
    clock = pygame.time.Clock()

    # some game flag to check during the game
    is_play = False
    gate_on = False
    tool_gathered = False

    while player.is_alive:
        # Check events by looping over the list of events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and pixel_collision(player.mask, player.rect, start_mask, start_rect):
                is_play = True

        # check if the player hit the grass
        if pixel_collision(player.mask, player.rect, barrier_mask, barrier_rect) and is_play:
            player.is_alive = False

        # Position the player to the mouse location
        pos = pygame.mouse.get_pos()
        player.rect.center = pos

        #draw the map
        screen.blit(map_barrier, barrier_rect)
        screen.blit(map_path, path_rect)

        # Draw the enemy
        if player.is_alive and zombie_1.is_alive:
            zombie_1.move((700, 700))
            zombie_1.draw(screen, message_font, (255, 0, 0))

        if pixel_collision(player.mask, player.rect, zombie_1.mask, zombie_1.rect) and is_play:
            if player.attack > zombie_1.attack:
                zombie_1.is_alive = False
            else:
                player.is_alive = False

        if pixel_collision(player.mask, player.rect, lighter_mask, lighter_rect) and is_play:
            gate_on = True

        # draw the lighter/key
        if not gate_on:
            screen.blit(lighter, lighter_rect)

        # draw the destination
        if gate_on:
            screen.blit(nether_gate_activated, nether_gate_activated_rect)
        else:
            screen.blit(nether_gate_not_activated, nether_gate_not_activated_rect)

        # draw the start sign at the beginning
        if not is_play:
            screen.blit(start, start_rect)

        #Draw tool icon if not touched by player
        if (pixel_collision(player.mask, player.rect, tool_mask, tool_rect) and is_play
                and not tool_gathered):
            tool_gathered = True
            player.attack += 1

        if not tool_gathered:
            screen.blit(tool, tool_rect)

        # check if player hit the destination when they are alive
        if pixel_collision(player.mask, player.rect, nether_gate_activated_mask, nether_gate_activated_rect) and gate_on:
            break

        #draw player's attack data
        label_hp = message_font.render(f"Player ATK: {player.attack}", True, (255, 0, 0))
        screen.blit(label_hp, (25, 50))

        # draw the player
        player.move(pos)
        player.draw(screen)

        # Bring drawn changes to the front
        pygame.display.flip()

        # This tries to force the loop to run at 30 fps
        clock.tick(30)

    if player.is_alive:
        # print('triggered')
        return True
    else:
        return False