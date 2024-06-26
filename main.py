import pygame
import math

pygame.init()
screen_x, screen_y = 720, 720
screen = pygame.display.set_mode((screen_x,screen_y))
clock = pygame.time.Clock()


def draw_grid(grid_num):
    add = screen_y / grid_num
    # vertical lines
    for i in range(grid_num - 1):
        x = add * (1 + i)
        pygame.draw.line(screen, (255, 255, 255),
                         (x, 0), (x, screen_y), 1)

    #horizontal lines
    for i in range(grid_num - 1):
        y = add * (1 + i)
        pygame.draw.line(screen, (255, 255, 255),
                         (0, y), (screen_x, y), 1)


def set_grid_array(grid_num):
    grid = []

    for i in range(grid_num):
        grid.append([])
        for j in range(grid_num):
            grid[i].append(0)

    print(str(len(grid)) + " " + str(len(grid[0])))
    return grid


def change_grid_status(grid_num, pos):
    width_of_boxes = screen_x / grid_num
    arr_x = math.ceil(pos[0] / width_of_boxes)
    arr_y = math.ceil(pos[1] / width_of_boxes)
    return arr_x, arr_y


def draw_boxes(grid):
    width_of_boxes = screen_x / len(grid)
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == 1:
                x = width_of_boxes * (i - 1)
                y = width_of_boxes * (j - 1)
                pygame.draw.rect(screen, (255, 255, 255), (x, y, width_of_boxes, width_of_boxes))


def main():

    run = True
    grid_num = 40
    grid = set_grid_array(grid_num)

    while run:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                arr_pos = change_grid_status(grid_num, pygame.mouse.get_pos())
                grid[arr_pos[0]][arr_pos[1]] = 1
            elif event.type == pygame.QUIT:
                run = False
        draw_grid(grid_num)
        draw_boxes(grid)
        pygame.display.update()

    # end run loop

    clock.tick(60)


main()