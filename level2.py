import pygame, sys, display_win_or_loss
from basicset import *

def level2():
    pygame.init()

    # Load the path for player and the barrier.
    map_barrier = pygame.image.load("MP_level2_barrier.png")
    map_barrier = pygame.transform.smoothscale(map_barrier, (2000, 1400))
    map_path = pygame.image.load("MP_level2_path.png")
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
    tool_rect.center = (1900, 300)
    tool_mask = pygame.mask.from_surface(tool)

    # load start signs
    start = pygame.image.load("start.png")
    start = pygame.transform.scale(start, (100, 100))
    start_rect = start.get_rect()
    start_rect.center = (300, 300)
    start_mask = pygame.mask.from_surface(start)

    # load player file and get elements of it
    player = Player()
    player.attack = 1

    # load enemy file and get elements of it
    piglin = Enemy("piglin.png")
    piglin.attack = 1

    # load destination (activated/not activated)
    the_end_portal_activated = pygame.image.load("End_Portal_on.png")
    the_end_portal_activated = pygame.transform.scale(the_end_portal_activated, (150, 100))
    the_end_portal_activated_rect = the_end_portal_activated.get_rect()
    the_end_portal_activated_rect.center = (1300, 1300)
    the_end_portal_activated_mask = pygame.mask.from_surface(the_end_portal_activated)
    # not activated
    the_end_portal_not_activated = pygame.image.load("End_Portal_off.png")
    the_end_portal_not_activated = pygame.transform.scale(the_end_portal_not_activated, (150, 100))
    the_end_portal_not_activated_rect = the_end_portal_not_activated.get_rect()
    the_end_portal_not_activated_rect.center = (1300, 1300)

    # load eye_of_ender/key
    eyes = []
    eye_of_ender_1 = EyeOfEnd("Eye_of_Ender.png", (100, 100), (300, 1100))
    eyes.append(eye_of_ender_1)
    eye_of_ender_2 = EyeOfEnd("Eye_of_Ender.png", (100, 100), (700, 500))
    eyes.append(eye_of_ender_2)
    eye_of_ender_3 = EyeOfEnd("Eye_of_Ender.png", (100, 100), (1300, 900))
    eyes.append(eye_of_ender_3)

    # load special enemy for this level
    eoe = pygame.image.load("EOE.png")
    eoe = pygame.transform.scale(eoe, (150, 150))
    eoe_rect = eoe.get_rect()
    eoe_rect.center = (1900, 700)

    # fireball lists
    fireballs = []
    fireball = Fireball("Fireball.png", (100, 100))
    fireballs.append(fireball)

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
    eyes_collected = 0
    last_tick = 0

    while player.is_alive:
        # Check events by looping over the list of events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_play = False
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and pixel_collision(player.mask, player.rect, start_mask,
                                                                        start_rect):
                is_play = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                print(pygame.mouse.get_pos())

        # check if the player hit the grass
        if pixel_collision(player.mask, player.rect, barrier_mask, barrier_rect) and is_play:
            player.is_alive = False

        # Position the player to the mouse location
        pos = pygame.mouse.get_pos()
        player.rect.center = pos

        # draw the map
        screen.blit(map_path, path_rect)
        screen.blit(map_barrier, barrier_rect)

        # Draw the enemy
        if piglin.is_alive:
            piglin.move((1700, 900))
            piglin.draw(screen, message_font, (0, 0, 255))

        if pixel_collision(player.mask, player.rect, piglin.mask, piglin.rect) and is_play:
            if player.attack > piglin.attack:
                piglin.is_alive = False
            else:
                player.is_alive = False

        # keep the eye that not touched
        eyes = [eye for eye in eyes if eye.active == True]
        for eye in eyes:
            if pixel_collision(player.mask, player.rect, eye.mask, eye.rect) and is_play:
                eyes_collected += 1
                eye.active = False

        # draw the eye_of_ender_1/key
        for eye in eyes:
            eye.draw(screen)

        # draw special enemy for this level
        screen.blit(eoe, eoe_rect)

        # create fireballs and move them
        fireballs = [fireball for fireball in fireballs if fireball.rect.center[0] > 500]
        if pygame.time.get_ticks() - last_tick > 2000:
            fireball = Fireball("Fireball.png", (100, 100))
            fireballs.append(fireball)
            last_tick = pygame.time.get_ticks()
        for fireball in fireballs:
            fireball.update(screen)
            if pixel_collision(player.mask, player.rect, fireball.mask, fireball.rect) and is_play:
                player.is_alive = False

        # draw the destination
        if eyes_collected == 3:
            screen.blit(the_end_portal_activated, the_end_portal_activated_rect)
        else:
            screen.blit(the_end_portal_not_activated, the_end_portal_not_activated_rect)

        # draw the start sign at the beginning
        if not is_play:
            screen.blit(start, start_rect)

        # Draw tool icon if not touched by player
        if (pixel_collision(player.mask, player.rect, tool_mask, tool_rect) and is_play
                and not tool_gathered):
            tool_gathered = True
            player.attack += 1

        if not tool_gathered:
            screen.blit(tool, tool_rect)

        # check if player hit the destination when they are alive
        if pixel_collision(player.mask, player.rect, the_end_portal_activated_mask,
                           the_end_portal_activated_rect) and eyes_collected == 3:
            break

        # draw player's attack data
        label_hp = message_font.render(f"Player ATK: {player.attack}", True, (0, 0, 255))
        screen.blit(label_hp, (25, 50))

        # draw the player
        player.move(pos)
        player.draw(screen)

        # Bring drawn changes to the front
        pygame.display.flip()

        # This tries to force the loop to run at 30 fps
        clock.tick(30)

    if player.is_alive:
        return True
    else:
        return False