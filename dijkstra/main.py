from tkinter import messagebox, Tk
import pygame as pg
import sys

WIDTH = 800
HEIGHT = WIDTH
win = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Dijkstra's Path Finding Algorithm")

# COLORS
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

columns = 50
rows = 50

box_width = WIDTH // columns
box_height = HEIGHT // rows

grid = []
queue = []
path = []

class Box:
    def __init__(self, i, j) -> None:
        self.x = i
        self.y = j
        self.start = False
        self.wall = False
        self.target = False
        self.queued = False
        self.visited = False
        self.neighbors = []
        self.prior = None
        
    def draw(self, win, color):
        pg.draw.rect(win, color, (self.x * box_width, self.y * box_height, box_width -2, box_height -2))
        
    def set_neighbors(self):
        if self.x > 0:
            self.neighbors.append(grid[self.x-1][self.y])
        if self.x < columns -1:
            self.neighbors.append(grid[self.x+1][self.y])
        if self.y > 0:
            self.neighbors.append(grid[self.x][self.y-1])
        if self.y < rows -1:
            self.neighbors.append(grid[self.x][self.y+1])
        
for i in range(columns):
    arr = []
    for j in range(rows):
        arr.append(Box(i, j))
    grid.append(arr)
    
for i in range(columns):
    for j in range(rows):
        grid[i][j].set_neighbors()

start_box = grid[0][0]
start_box.start = True
start_box.visited = True
queue.append(start_box)

def main():
    begin_search = False
    target_box_set = False
    searching = True
    target_box = None
    
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.MOUSEMOTION:
                x = pg.mouse.get_pos()[0]
                y = pg.mouse.get_pos()[1]
                # Draw wall
                if event.buttons[0]:
                    i = x // box_width
                    j = y // box_height
                    grid[i][j].wall = True
                if event.buttons[2] and not target_box_set:
                    i = x // box_width
                    j = y // box_height
                    target_box = grid[i][j]
                    target_box.target = True
                    target_box_set = True
            if event.type == pg.KEYDOWN and target_box_set:
                begin_search = True
        
        if begin_search:
            if len(queue) > 0 and searching:
                current_box = queue.pop(0)
                current_box.visited = True
                if current_box == target_box:
                    searching = False
                    while current_box.prior != start_box:
                        path.append(current_box.prior)
                        current_box = current_box.prior
                else:
                    for neighbor in current_box.neighbors:
                        if not neighbor.queued and not neighbor.wall:
                            neighbor.queued = True
                            neighbor.prior = current_box
                            queue.append(neighbor)
            else:
                if searching:
                    Tk().wm_withdraw()
                    messagebox.showinfo("No Solution", "There is no solution!")
                    searching = False
                
        win.fill(BLACK)
        for i in range(columns):
            for j in range(rows):
                box = grid[i][j]
                box.draw(win, WHITE)
                if box.queued:
                    box.draw(win, GREEN)
                if box.visited:
                    box.draw(win, RED)
                if box in path:
                    box.draw(win, PURPLE)
                if box.start:
                    box.draw(win, ORANGE)
                if box.wall:
                    box.draw(win, BLACK)
                if box.target:
                    box.draw(win, TURQUOISE)
            
        pg.display.flip()

if __name__ == "__main__":
	main()
