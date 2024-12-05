from idlelib.browser import transform_children

import pygame, sys
from basicset import *

def level3():
    pygame.init()

    # Load the path for player and the barrier.
    map_barrier = pygame.image.load("MP_level3_barrier.png")
    map_barrier = pygame.transform.smoothscale(map_barrier, (2000, 1400))
    map_path = pygame.image.load("MP_level3_path.png")
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
    tool_locations = [(1300, 300), (700, 500), (700, 1100), (1500, 900)]
    tools = []
    for location in tool_locations:
        tool = Tool(location)
        tools.append(tool)

    # load start signs
    start = pygame.image.load("start.png")
    start = pygame.transform.scale(start, (100, 100))
    start_rect = start.get_rect()
    start_rect.center = (300, 300)
    start_mask = pygame.mask.from_surface(start)

    # load player file and get elements of it
    player = Player()
    player.attack = 2

    # load enemy file and get elements of it, and set different locations
    ender_man_locations = [(300, 500), (1500, 1100), (500, 1100)]
    endermans = []
    enderman_attacks = [1, 5, 4]
    for index in range(3):
        enderman = Enemy("enderman.png")
        enderman.rect.center = ender_man_locations[index]
        enderman.attack = enderman_attacks[index]
        endermans.append(enderman)

    # load destination (activated/not activated)
    final_destination = pygame.image.load("endergate.png")
    final_destination = pygame.transform.scale(final_destination, (100, 150))
    final_destination_rect = final_destination.get_rect()
    final_destination_rect.center = (1100, 1100)
    final_destination_mask = pygame.mask.from_surface(final_destination)

    # load chorus fruit and add them to the list
    chorus_fruits = []
    chorus_fruits_locations = [(300, 700), (700, 900), (300, 1100), (700, 300), (900, 500), (1100, 300),
                               (1500, 300), (1500, 700)]
    for location in chorus_fruits_locations:
        chorus_fruit = ChorusFruit("chorusfruit.png", (100, 100), location)
        chorus_fruits.append(chorus_fruit)


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
    tp_on = False
    tp_trigger = False
    collision_time = 0

    while player.is_alive:
        # Check events by looping over the list of events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and pixel_collision(player.mask, player.rect, start_mask, start_rect):
                is_play = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                print(pygame.mouse.get_pos())

        # check if the player hit the grass
        if pixel_collision(player.mask, player.rect, barrier_mask, barrier_rect) and is_play and not tp_on:
            player.is_alive = False

        # Position the player to the mouse location
        pos = pygame.mouse.get_pos()
        player.rect.center = pos

        #draw the map
        screen.blit(map_path, path_rect)
        screen.blit(map_barrier, barrier_rect)

        # updates alive enemies and draw the enemy
        endermans = [enderman for enderman in endermans if enderman.is_alive]

        for enderman in endermans:
            enderman.draw(screen, message_font, (255, 0, 0))
            if pixel_collision(player.mask, player.rect, enderman.mask, enderman.rect) and is_play and not tp_on:
                if player.attack > enderman.attack:
                    enderman.is_alive = False
                else:
                    player.is_alive = False

        # update chorus fruit and draw it

        chorus_fruits = [chorus_fruit for chorus_fruit in chorus_fruits if not chorus_fruit.touched]

        for chorus_fruit in chorus_fruits:
            chorus_fruit.draw(screen)
            if pixel_collision(player.mask, player.rect, chorus_fruit.mask, chorus_fruit.rect) and is_play:
                chorus_fruit.touched = True
                if tp_on:
                    collision_time = pygame.time.get_ticks()
                    tp_trigger = True
                else:
                    tp_on = True
                    player.tp()

        if pygame.time.get_ticks() - collision_time >= 500 and tp_trigger:
            tp_on = False
            tp_trigger = False
            player.tp()

        # if pixel_collision(player.mask, player.rect, chorus_fruit_mask, chorus_fruit_rect) and is_play:
        #     gate_on = True
        #
        # # draw the lighter/key
        # if not gate_on:
        #     screen.blit(chorus_fruit, chorus_fruit_rect)

        # draw the destination
        screen.blit(final_destination, final_destination_rect)

        # draw the start sign at the beginning
        if not is_play:
            screen.blit(start, start_rect)

        #Draw tool icon if not touched by player
        tools = [tool for tool in tools if not tool.touched]
        for tool in tools:
            tool.draw(screen)
            if pixel_collision(player.mask, player.rect, tool.mask, tool.rect) and is_play and not tp_on:
                tool.touched = True
                player.attack += 1

        # check if player hit the destination when they are alive
        if (pixel_collision(player.mask, player.rect, final_destination_mask, final_destination_rect)
                and not tp_on and is_play):
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