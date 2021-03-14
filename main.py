import sys

import pygame
from pygame.locals import *  # import pygame modules

clock = pygame.time.Clock()
# elapsed = 0

pygame.init()  # initiate pygame

path = "localAssets/"
resolution = (160, 144)
window_scale_factor = 3
window = (resolution[0] * window_scale_factor, resolution[1] * window_scale_factor)
screen = pygame.display.set_mode(window, 0, 32)  # initiate screen
display = pygame.Surface(resolution)
pygame.display.set_caption("first pygame")  # title bar name

background_img = pygame.image.load(path + "bg.png")
bg_PV = 0.25  # Parallax Value
player_img = pygame.image.load(path + "tile_0006.png")
player_img.set_colorkey((0, 0, 0))
grass_img = pygame.image.load(path + "tile_0110.png")
dirt_img = pygame.image.load(path + "tile_0124.png")

tile_size = grass_img.get_width()


def load_map(path):
    f = open(path + ".txt", "r")
    data = f.read()
    f.close()
    data = data.split("\n")
    game_map = []
    for row in data:
        game_map.append(list(row))
    return game_map


game_map = load_map(path + "map")


def collision_test(rect, tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list


def move(rect, movement, tiles):
    collision_types = {"top": False, "bottom": False, "left": False, "right": False}
    rect.x += movement[0]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types["right"] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types["left"] = True
    rect.y += movement[1]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types["bottom"] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types["top"] = True
    return rect, collision_types


player_y_momentum = 0
air_timer = 0
mv_left = False
mv_right = False

true_scroll = [0, 0]
scroll = [0, 0]

# collision shape of player
player_rect = pygame.Rect(10, 10, player_img.get_width(), player_img.get_height())
"""
def update_player(seconds):
    player_rect = ( player_rect.x + int(player_movement[0]*seconds),
                    player_rect.y + int(player_movement[1]*seconds))
    return player_rect
"""

# ################################################################################################
# GAME LOOP
# ################################################################################################

running = True
while running:  # game loop
    # seconds = elapsed/1000.0
    display.fill((146, 244, 255))

    true_scroll[0] += (
        player_rect.x - true_scroll[0] - (resolution[0] + player_img.get_width()) / 2
    ) / 6
    true_scroll[1] += (
        player_rect.y - true_scroll[1] - (resolution[1] + player_img.get_height()) / 2
    ) / 6
    scroll[0] = int(true_scroll[0])
    scroll[1] = int(true_scroll[1])

    display.blit(background_img, (-90 - scroll[0] * bg_PV, -10 - scroll[1] * bg_PV))

    tile_rects = []
    y = 0
    for tile_row in game_map:
        x = 0
        for tile in tile_row:
            if tile == "1":
                display.blit(
                    dirt_img, (x * tile_size - scroll[0], y * tile_size - scroll[1])
                )
            if tile == "2":
                display.blit(
                    grass_img, (x * tile_size - scroll[0], y * tile_size - scroll[1])
                )
            if tile != "0":
                tile_rects.append(
                    pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size)
                )
            x += 1
        y += 1

    player_movement = [0, 0]
    if mv_right:
        player_movement[0] += 2
    if mv_left:
        player_movement[0] -= 2

    player_movement[1] += player_y_momentum
    player_y_momentum += 0.3
    if player_y_momentum >= 3:
        player_y_momentum = 3

    player_rect, collisions = move(player_rect, player_movement, tile_rects)
    if collisions["bottom"]:
        player_y_momentum = 0
        air_timer = 0
    elif collisions["top"]:
        player_y_momentum = 0
    else:
        air_timer += 1

    #    update_player(seconds)

    display.blit(player_img, (player_rect.x - scroll[0], player_rect.y - scroll[1]))

    for event in pygame.event.get():  # event loop
        if event.type == pygame.QUIT:  # check for window quit
            running = False
        if event.type == KEYDOWN:  # check for key down presses
            if event.key == K_LEFT:
                mv_left = True
            if event.key == K_RIGHT:
                mv_right = True
            if event.key == K_UP:
                if air_timer < 6:
                    player_y_momentum -= 4
        if event.type == KEYUP:  # check for key releases
            if event.key == K_LEFT:
                mv_left = False
            if event.key == K_RIGHT:
                mv_right = False
    if player_rect.y > resolution[1]:
        running = False
    screen.blit(pygame.transform.scale(display, window), (0, 0))  # window scaling
    pygame.display.update()
    #    elapsed = clock.tick(60)
    clock.tick(60)
pygame.quit()
sys.exit()