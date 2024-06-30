import pygame
import math
import numpy
from pixel import Pixel

pygame.init()
grid_x, grid_y = 720, 720
screen_x, screen_y = 1000, 750
sc = pygame.display.set_mode((screen_x, screen_y))
clock = pygame.time.Clock()


def draw_grid(grid_num, gr_x, gr_y, screen):
    add = gr_x / grid_num
    # vertical lines
    for i in range(grid_num - 1):
        x = add * (1 + i)
        pygame.draw.line(screen, (255, 255, 255),
                         (x, 0), (x, gr_y), 1)

    # horizontal lines
    for i in range(grid_num - 1):
        y = add * (1 + i)
        pygame.draw.line(screen, (255, 255, 255),
                         (0, y), (gr_x, y), 1)


def set_grid_array(grid_num):
    grid = []

    for i in range(grid_num):
        grid.append([])
        for j in range(grid_num):
            grid[i].append(0)

    return grid


def change_grid_status(grid_num, pos, gr_x):
    width_of_boxes = gr_x / grid_num
    arr_x = math.floor(pos[0] / width_of_boxes)
    arr_y = math.floor(pos[1] / width_of_boxes)
    return arr_x, arr_y


def draw_boxes(grid, screen, gr_x):
    width_of_boxes = gr_x / len(grid)
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == 1:
                x = width_of_boxes * i
                y = width_of_boxes * j
                pygame.draw.rect(screen, (255, 255, 255), (x, y, width_of_boxes, width_of_boxes))
            elif grid[i][j] == 2:
                x = width_of_boxes * i
                y = width_of_boxes * j
                pygame.draw.rect(screen, (255, 0, 0), (x, y, width_of_boxes, width_of_boxes))


def draw_start_pause_button(pause,gr_x, gr_y, screen):
    red = (255, 0, 0)
    green = (0, 255, 0)

    start_coordinates = ((gr_x - 60, gr_y - 60), (gr_x - 60, gr_y - 10), (gr_x - 10, gr_y - 35))
    rect_1_coordinates = (gr_x - 60, gr_y - 60, 20, 50)
    rect_2_coordinates = (gr_x - 30, gr_y - 60, 20, 50)

    if not pause:
        pygame.draw.polygon(screen, green, start_coordinates)
    else:
        pygame.draw.rect(screen, red, rect_1_coordinates)
        pygame.draw.rect(screen, red, rect_2_coordinates)


def check_neighbours_me_alive(top_l, top, top_r, mid_l, mid_r, bottom_l, bottom, bottom_r):
    neighbours = [top_l, top, top_r, mid_l, mid_r, bottom_l, bottom, bottom_r]
    alive = 0
    for i in range(len(neighbours)):
        if neighbours[i] == 1:
            alive += 1

    my_status = 0
    if alive == 2 or alive == 3:
        my_status = 1

    return my_status


def check_neighbours_me_dead(top_l, top, top_r, mid_l, mid_r, bottom_l, bottom, bottom_r):
    neighbours = [top_l, top, top_r, mid_l, mid_r, bottom_l, bottom, bottom_r]
    alive = 0
    for n in neighbours:
        if n == 1:
            alive += 1

    if alive == 3:
        return 1
    return 0


def find_and_check_neighbours(grid, i, j, alive):
    left = i - 1
    right = i + 1
    top = j - 1
    bottom = j + 1

    if left < 0:
        left = len(grid) - 1
    elif right > len(grid) - 1:
        right = 0

    if top < 0:
        top = len(grid[0]) - 1
    elif bottom > len(grid[0]) - 1:
        bottom = 0

    top_l = Pixel(grid, left, top)
    top_m = Pixel(grid, i, top)
    top_r = Pixel(grid, right, top)

    mid_l = Pixel(grid, left, j)
    mid_r = Pixel(grid, right, j)

    bottom_l = Pixel(grid, left, bottom)
    bottom_m = Pixel(grid, i, bottom)
    bottom_r = Pixel(grid, right, bottom)

    if alive:
        pos = [top_l, top_m, top_r, mid_l, mid_r, bottom_l, bottom_m, bottom_r]
        list_of_dead_to_check = []
        for p in pos:
            if p.value == 0:
                list_of_dead_to_check.append(p)

        return check_neighbours_me_alive(top_l.value, top_m.value, top_r.value,
                                         mid_l.value, mid_r.value,
                                         bottom_l.value, bottom_m.value, bottom_r.value), list_of_dead_to_check
    else:
        return check_neighbours_me_dead(top_l.value, top_m.value, top_r.value,
                                        mid_l.value, mid_r.value,
                                        bottom_l.value, bottom_m.value, bottom_r.value)


def update_grid(grid, grid_num):
    grid = numpy.array(grid)  # grid we will return as the final modified version
    og_grid = numpy.copy(grid)  # grid where we will only modify to mark which dead cells to check

    dead_to_check = []

    for i in range(grid_num):
        for j in range(grid_num):
            if og_grid[i][j] == 1:
                neighbourhood = find_and_check_neighbours(og_grid, i, j, True)
                grid[i][j] = neighbourhood[0]
                for p in neighbourhood[1]:
                    dead_to_check.append(p)

    for p in dead_to_check:
        i, j = p.i, p.j
        grid[i][j] = find_and_check_neighbours(og_grid, i, j, False)

    return grid


def draw_speed_bar(x, y, speed, mouse_pos, screen):
    speed = speed / 2
    pygame.draw.rect(screen, (50, 50, 50), (x, y, 100, 25))
    pygame.draw.rect(screen, (100, 100, 100), (x + speed, y, 25, 25))

    if x < mouse_pos[0] < x + 100 and y < mouse_pos[1] < y + 25:
        print(str(x) + " " + str(y) + "||" + str(mouse_pos))
        speed = mouse_pos[0] - x

    return speed * 2

def main():

    run = True
    game_running = False
    grid_num = 100
    grid = set_grid_array(grid_num)
    timer = 0
    speed = 100

    while run:
        mouse_p = (-100, -100)

        sc.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                mouse_p = mouse_pos

                if mouse_pos[0] <= grid_x and mouse_pos[1] <= grid_y:  # making a pixel dead or alive
                    arr_pos = change_grid_status(grid_num, mouse_pos, grid_x)

                    # toggle a pixel dead or alive
                    if grid[arr_pos[0]][arr_pos[1]] == 1:
                        grid[arr_pos[0]][arr_pos[1]] = 0
                    else:
                        grid[arr_pos[0]][arr_pos[1]] = 1
                elif mouse_pos[0] >= screen_x - 70 and mouse_pos[1] >= screen_y - 70:  # start or pause game
                    game_running = not game_running
            elif event.type == pygame.QUIT:
                run = False

        timer += 1

        if timer >= (200 - speed) and game_running:
            grid = update_grid(grid, grid_num)
            timer = 0

        speed = draw_speed_bar(screen_x - 110, screen_y - 200, speed, mouse_p, sc)
        draw_grid(grid_num, grid_x, grid_y, sc)
        draw_boxes(grid, sc, grid_x)
        draw_start_pause_button(game_running, screen_x, screen_y, sc)
        pygame.display.update()

    # end run loop

    clock.tick(60)


main()
