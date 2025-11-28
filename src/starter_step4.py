# starter_step4.py
import pygame
import math

from gridmap import GridMap
from astar import AStar

pygame.init()

W, H = 900, 600
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Step 4: A* Pathfinding")

clock = pygame.time.Clock()

# Obstacles (same as your STEP 3)
rect_obstacles = [
    (200, 200, 200, 60),
    (350, 120, 180, 50),
    (500, 400, 200, 60),
]

circle_obstacles = [
    (150, 500, 45),
    (700, 250, 60),
]

# Robot start + goal
robot_x = 100
robot_y = 100
goal = (750, 450)

# Generate grid automatically
grid = GridMap(W, H, 20)
grid.mark_obstacles(rect_obstacles, circle_obstacles)

planner = AStar(grid.grid)

start_cell = (robot_y // 20, robot_x // 20)
goal_cell = (goal[1] // 20, goal[0] // 20)

path = planner.search(start_cell, goal_cell)

def draw_robot(x, y):
    pygame.draw.circle(screen, (0, 255, 0), (int(x), int(y)), 12)

def draw_path(path, cell):
    for (r, c) in path:
        px = c * cell + cell/2
        py = r * cell + cell/2
        pygame.draw.circle(screen, (0, 150, 255), (int(px), int(py)), 4)

running = True
i = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((25, 25, 25))

    # Draw obstacles
    for x, y, w, h in rect_obstacles:
        pygame.draw.rect(screen, (200, 60, 60), (x, y, w, h))

    for cx, cy, r in circle_obstacles:
        pygame.draw.circle(screen, (220, 150, 50), (cx, cy), r)

    # Draw A* path
    
    if path:
        draw_path(path, 20)

    # Simulate robot following path
    if path and i < len(path):
        r, c = path[i]
        robot_x = c * 20 + 10
        robot_y = r * 20 + 10
        i += 1

    draw_robot(robot_x, robot_y)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
