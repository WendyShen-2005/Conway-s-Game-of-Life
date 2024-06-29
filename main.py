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

    neighbourhood = numpy.array([[neighbours[0], neighbours[3], neighbours[5]],  # left side
                     [neighbours[1], my_status, neighbours[6]],  # middle
                     [neighbours[2], neighbours[4], neighbours[7]]])  # right side

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


def update_grid(grid, grid_num):
    grid = numpy.array(grid)  # grid we will return as the final modified version
    og_grid = numpy.copy(grid)  # grid where we will only modify to mark which dead cells to check

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if og_grid[i][j] == 1:
                neighbourhood = grid
                if i != 0 and i != grid_num - 1 and j != 0 and j != grid_num - 1:  # middle pixels
                    neighbourhood = check_neighbours_me_alive(og_grid[i - 1][j - 1], og_grid[i][j - 1], og_grid[i + 1][j - 1],
                                             og_grid[i - 1][j], og_grid[i + 1][j],
                                             og_grid[i - 1][j + 1], og_grid[i][j + 1], og_grid[i + 1][j + 1])
                elif i == 0:  # pixels meet left side
                    if j == 0:  # top left corner
                        neighbourhood = check_neighbours_me_alive(og_grid[grid_num - 1][grid_num - 1], og_grid[i][grid_num - 1], og_grid[i + 1][grid_num - 1],
                                                                  og_grid[grid_num - 1][j], og_grid[i + 1][j],
                                                                  og_grid[grid_num - 1][j + 1], og_grid[i][j + 1], og_grid[i + 1][j + 1])
                    elif j == grid_num - 1:  # bottom left corner
                        neighbourhood = check_neighbours_me_alive(og_grid[grid_num - 1][j - 1], og_grid[i][j - 1], og_grid[i + 1][j - 1],
                                                                  og_grid[grid_num - 1][j], og_grid[i + 1][j],
                                                                  og_grid[grid_num - 1][0], og_grid[i][0], og_grid[i + 1][0])
                    else:  # not corner
                        neighbourhood = check_neighbours_me_alive(og_grid[grid_num - 1][j - 1], og_grid[i][j - 1], og_grid[i + 1][j - 1],
                                                                  og_grid[grid_num - 1][j], og_grid[i + 1][j],
                                                                  og_grid[grid_num - 1][j + 1], og_grid[i][j + 1], og_grid[i + 1][j + 1])
                elif i == grid_num - 1:  # pixels meet right side
                    if j == 0:  # top right corner
                        neighbourhood = check_neighbours_me_alive(og_grid[i - 1][grid_num - 1], og_grid[i][grid_num - 1], og_grid[0][grid_num - 1],
                                                                  og_grid[i - 1][j], og_grid[0][j],
                                                                  og_grid[i - 1][j + 1], og_grid[i][j + 1], og_grid[0][j + 1])
                    elif j == grid_num - 1:  # bottom right corner
                        neighbourhood = check_neighbours_me_alive(og_grid[i - 1][j - 1], og_grid[i][j - 1], og_grid[0][j - 1],
                                                                  og_grid[i - 1][j], og_grid[0][j],
                                                                  og_grid[i - 1][0], og_grid[i][0], og_grid[0][0])
                    else:  # everything else
                        neighbourhood = check_neighbours_me_alive(og_grid[i - 1][j - 1], og_grid[i][j - 1], og_grid[grid_num + 1][j - 1],
                                                                  og_grid[i - 1][j], og_grid[grid_num + 1][j],
                                                                  og_grid[i - 1][j + 1], og_grid[i][j + 1], og_grid[grid_num + 1][j + 1])
                elif j == 0:  # pixels hitting top
                    neighbourhood = check_neighbours_me_alive(og_grid[i - 1][grid_num - 1], og_grid[i][grid_num - 1], og_grid[i + 1][grid_num - 1],
                                                              og_grid[i - 1][j], og_grid[i + 1][j],
                                                              og_grid[i - 1][j + 1], og_grid[i][j + 1], og_grid[i + 1][j + 1])
                else:  # pixels hitting bottom
                    neighbourhood = check_neighbours_me_alive(og_grid[i - 1][j - 1], og_grid[i][j - 1], og_grid[i + 1][j - 1],
                                                              og_grid[i - 1][j], og_grid[i + 1][j],
                                                              og_grid[i - 1][0], og_grid[i][0], og_grid[i + 1][0])

                grid[i][j] = neighbourhood[0]

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if i != 0 and i != grid_num - 1 and j != 0 and j != grid_num - 1 and og_grid[i][j] == 0:
                grid[i][j] = check_neighbours_me_dead(og_grid[i - 1][j - 1], og_grid[i][j - 1], og_grid[i + 1][j - 1],
                                                      og_grid[i - 1][j], og_grid[i + 1][j],
                                                      og_grid[i - 1][j + 1], og_grid[i][j + 1], og_grid[i + 1][j + 1])

            elif i == 0:  # pixels meet left side
                if j == 0:  # top left corner
                    grid[i][j] = check_neighbours_me_alive(og_grid[grid_num - 1][grid_num - 1],
                                                              og_grid[i][grid_num - 1], og_grid[i + 1][grid_num - 1],
                                                              og_grid[grid_num - 1][j], og_grid[i + 1][j],
                                                              og_grid[grid_num - 1][j + 1], og_grid[i][j + 1],
                                                              og_grid[i + 1][j + 1])
                elif j == grid_num - 1:  # bottom left corner
                    grid[i][j] = check_neighbours_me_alive(og_grid[grid_num - 1][j - 1], og_grid[i][j - 1],
                                                              og_grid[i + 1][j - 1],
                                                              og_grid[grid_num - 1][j], og_grid[i + 1][j],
                                                              og_grid[grid_num - 1][0], og_grid[i][0],
                                                              og_grid[i + 1][0])
                else:  # not corner
                    grid[i][j] = check_neighbours_me_alive(og_grid[grid_num - 1][j - 1], og_grid[i][j - 1],
                                                              og_grid[i + 1][j - 1],
                                                              og_grid[grid_num - 1][j], og_grid[i + 1][j],
                                                              og_grid[grid_num - 1][j + 1], og_grid[i][j + 1],
                                                              og_grid[i + 1][j + 1])
            elif i == grid_num - 1:  # pixels meet right side
                if j == 0:  # top right corner
                    grid[i][j] = check_neighbours_me_alive(og_grid[i - 1][grid_num - 1], og_grid[i][grid_num - 1],
                                                              og_grid[0][grid_num - 1],
                                                              og_grid[i - 1][j], og_grid[0][j],
                                                              og_grid[i - 1][j + 1], og_grid[i][j + 1],
                                                              og_grid[0][j + 1])
                elif j == grid_num - 1:  # bottom right corner
                    grid[i][j] = check_neighbours_me_alive(og_grid[i - 1][j - 1], og_grid[i][j - 1],
                                                              og_grid[0][j - 1],
                                                              og_grid[i - 1][j], og_grid[0][j],
                                                              og_grid[i - 1][0], og_grid[i][0], og_grid[0][0])
                else:  # everything else
                    grid[i][j] = check_neighbours_me_alive(og_grid[i - 1][j - 1], og_grid[i][j - 1],
                                                              og_grid[grid_num + 1][j - 1],
                                                              og_grid[i - 1][j], og_grid[grid_num + 1][j],
                                                              og_grid[i - 1][j + 1], og_grid[i][j + 1],
                                                              og_grid[grid_num + 1][j + 1])
            elif j == 0:  # pixels hitting top
                grid[i][j] = check_neighbours_me_alive(og_grid[i - 1][grid_num - 1], og_grid[i][grid_num - 1],
                                                          og_grid[i + 1][grid_num - 1],
                                                          og_grid[i - 1][j], og_grid[i + 1][j],
                                                          og_grid[i - 1][j + 1], og_grid[i][j + 1],
                                                          og_grid[i + 1][j + 1])
            else:  # pixels hitting bottom
                grid[i][j] = check_neighbours_me_alive(og_grid[i - 1][j - 1], og_grid[i][j - 1],
                                                          og_grid[i + 1][j - 1],
                                                          og_grid[i - 1][j], og_grid[i + 1][j],
                                                          og_grid[i - 1][0], og_grid[i][0], og_grid[i + 1][0])

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
