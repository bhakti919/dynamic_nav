# gridmap.py
import pygame
import numpy as np

class GridMap:
    def __init__(self, width, height, cell_size):
        self.width = width
        self.height = height
        self.cell = cell_size

        self.cols = width // cell_size
        self.rows = height // cell_size

        self.grid = np.zeros((self.rows, self.cols), dtype=np.int8)

    def mark_obstacles(self, rect_obstacles, circle_obstacles):
        """Convert rectangles & circles into blocked grid cells"""

        # Mark rectangles
        for (x, y, w, h) in rect_obstacles:
            col1 = x // self.cell
            col2 = (x + w) // self.cell
            row1 = y // self.cell
            row2 = (y + h) // self.cell

            self.grid[row1:row2+1, col1:col2+1] = 1

        # Mark circles
        for (cx, cy, r) in circle_obstacles:
            for row in range(self.rows):
                for col in range(self.cols):
                    gx = col * self.cell + self.cell/2
                    gy = row * self.cell + self.cell/2

                    if (gx - cx)**2 + (gy - cy)**2 <= r*r:
                        self.grid[row, col] = 1

    def draw(self, screen):
        """OPTIONAL: Draw grid overlay"""
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r, c] == 1:
                    pygame.draw.rect(
                        screen, (80, 0, 0),
                        (c*self.cell, r*self.cell, self.cell, self.cell)
                    )
