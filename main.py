import pygame
import math
import numpy

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
        else:
            neighbours[i] = 2

    my_status = 0
    if alive == 2 or alive == 3:
        my_status = 1

    neighbourhood = numpy.array([[neighbours[0], neighbours[3], neighbours[5]],
                     [neighbours[1], my_status, neighbours[6]],
                     [neighbours[2], neighbours[4], neighbours[7]]])

    return my_status, neighbourhood


def check_neighbours_me_dead(top_l, top, top_r, mid_l, mid_r, bottom_l, bottom, bottom_r):
    neighbours = [top_l, top, top_r, mid_l, mid_r, bottom_l, bottom, bottom_r]
    alive = 0
    for n in neighbours:
        if n == 1:
            alive += 1

    if alive == 3:
        return 1
    return 0


def update_grid(grid):
    grid = numpy.array(grid)  # grid we will return as the final modified version
    og_grid = numpy.copy(grid)  # grid where we will only modify to mark which dead cells to check

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if i != 0 and i != 39 and j != 0 and j != 39 and og_grid[i][j] == 1:
                neighbourhood = check_neighbours_me_alive(og_grid[i - 1][j - 1], og_grid[i][j - 1], og_grid[i + 1][j - 1],
                                         og_grid[i - 1][j], og_grid[i + 1][j],
                                         og_grid[i - 1][j + 1], og_grid[i][j + 1], og_grid[i + 1][j + 1])

                grid[i][j] = neighbourhood[0]
                og_grid[i - 1: i + 2, j - 1: j + 2] = neighbourhood[1]

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if i != 0 and i != 39 and j != 0 and j != 39 and og_grid[i][j] == 2:
                grid[i][j] = check_neighbours_me_dead(og_grid[i - 1][j - 1], og_grid[i][j - 1], og_grid[i + 1][j - 1],
                                                      og_grid[i - 1][j], og_grid[i + 1][j],
                                                      og_grid[i - 1][j + 1], og_grid[i][j + 1], og_grid[i + 1][j + 1])

    return grid


def main():

    run = True
    game_running = False
    grid_num = 40
    grid = set_grid_array(grid_num)
    timer = 0

    while run:
        sc.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if mouse_pos[0] <= grid_x and mouse_pos[1] <= grid_y:
                    arr_pos = change_grid_status(grid_num, mouse_pos, grid_x)
                    grid[arr_pos[0]][arr_pos[1]] = 1
                if mouse_pos[0] >= screen_x - 70 and mouse_pos[1] >= screen_y - 70:
                    game_running = not game_running
            elif event.type == pygame.QUIT:
                run = False

        timer += 1

        if timer >= 500 and game_running:
            grid = update_grid(grid)
            timer = 0

        draw_grid(grid_num, grid_x, grid_y, sc)
        draw_boxes(grid, sc, grid_x)
        draw_start_pause_button(game_running, screen_x, screen_y, sc)
        pygame.display.update()

    # end run loop

    clock.tick(60)


main()
