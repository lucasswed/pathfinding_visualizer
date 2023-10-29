import sys
import tkinter
import pygame as pg
from Spot import Spot
from astar import astar

WIDTH = 800
window = pg.display.set_mode((WIDTH, WIDTH))
pg.display.set_caption("Path finding algorithm visualizer")

# Colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos
    
    row = y // gap
    col = x // gap
    
    return row, col
    
def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, rows)
            grid[i].append(spot)
    return grid

def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pg.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pg.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


def draw(win, grid, rows, width):
    win.fill(WHITE)

    for row in grid:
        for spot in row:
            spot.draw(win)
    draw_grid(win, rows, width)
    pg.display.update()

def main(win, width, algorithm):
    rows = 50
    grid = make_grid(rows, width)
    
    start = None
    end = None
    
    run = True
    started = False
    while run:
        draw(window, grid, rows, width)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            if started:
                continue
            if pg.mouse.get_pressed()[0]:
                pos = pg.mouse.get_pos()
                row, col = get_clicked_pos(pos, rows, width)
                spot = grid[row][col]
                if not start and spot != end:
                    start = spot
                    start.make_start()
                elif not end and spot != start:
                    end = spot
                    end.make_end()
                elif spot != end and spot != start:
                    spot.make_barrier()
            elif pg.mouse.get_pressed()[2]:  # RIGHT BUTTON
                pos = pg.mouse.get_pos()
                row, col = get_clicked_pos(pos, rows, width)
                spot = grid[row][col]
                spot.reset()
                if spot == start:
                    start = None
                elif spot == end:
                    end = None
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE and not started:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)
                    algorithm(lambda: draw(win, grid, rows, width), grid, start, end)
                if event.key == pg.K_c:
                    start = None
                    end = None
                    grid = make_grid(rows, width)
    pg.quit()
    sys.exit()

if __name__ == "__main__":
    main(window, WIDTH, astar)