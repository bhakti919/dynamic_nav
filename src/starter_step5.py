# starter_step5.py
import pygame
import math

from gridmap import GridMap
from astar import AStar

pygame.init()

W, H = 900, 600
CELL = 20
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Step 5: Dynamic Obstacles + Replanning")
clock = pygame.time.Clock()

# Static obstacles
rect_obstacles = [
    (200, 200, 200, 60),
    (350, 120, 180, 50),
    (500, 400, 200, 60),
]

circle_obstacles_static = [
    (150, 500, 45),
    (700, 250, 60),
]

# Dynamic obstacle
dyn_x = 400
dyn_y = 300
dyn_r = 40
dyn_speed = 2

# Robot
robot_x = 100
robot_y = 100
goal = (750, 450)

def build_grid():
    """Build grid each frame (because dynamic obstacle moves)."""
    grid = GridMap(W, H, CELL)

    # static
    grid.mark_obstacles(rect_obstacles, circle_obstacles_static)

    # dynamic obstacle added
    grid.mark_obstacles([], [(dyn_x, dyn_y, dyn_r)])

    return grid

def compute_path():
    """Compute shortest path."""
    grid = build_grid()
    planner = AStar(grid.grid)

    start_cell = (robot_y // CELL, robot_x // CELL)
    goal_cell = (goal[1] // CELL, goal[0] // CELL)

    return planner.search(start_cell, goal_cell)

# Initial path
path = compute_path()
path_index = 0

def draw_robot(x, y):
    pygame.draw.circle(screen, (0, 255, 0), (int(x), int(y)), 12)

def draw_path(path):
    for (r, c) in path:
        px = c * CELL + CELL/2
        py = r * CELL + CELL/2
        pygame.draw.circle(screen, (0, 140, 255), (int(px), int(py)), 4)

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move dynamic obstacle left–right
    dyn_x += dyn_speed
    if dyn_x > 800 or dyn_x < 100:
        dyn_speed *= -1

    # -------------------------------
    # CHECK IF NEXT PATH CELL IS BLOCKED → REPLAN
    # -------------------------------
    if path:
        if path_index < len(path):
            target_r, target_c = path[path_index]
            grid_now = build_grid().grid

            if grid_now[target_r, target_c] == 1:
                print("⚠ Dynamic obstacle blocked path → Replanning...")
                path = compute_path()
                path_index = 0

    # -------------------------------
    # MOVE ROBOT TOWARDS NEXT PATH NODE
    # -------------------------------
    if path and path_index < len(path):
        r, c = path[path_index]
        tx = c * CELL + CELL/2
        ty = r * CELL + CELL/2

        # simple motion
        dx = tx - robot_x
        dy = ty - robot_y
        dist = math.hypot(dx, dy)

        if dist < 2:
            path_index += 1
        else:
            robot_x += dx * 0.07
            robot_y += dy * 0.07

    screen.fill((25, 25, 25))

    # Draw static obstacles
    for x, y, w, h in rect_obstacles:
        pygame.draw.rect(screen, (200, 60, 60), (x, y, w, h))

    for cx, cy, r in circle_obstacles_static:
        pygame.draw.circle(screen, (220, 150, 50), (cx, cy), r)

    # Draw dynamic obstacle
    pygame.draw.circle(screen, (255, 200, 0), (dyn_x, dyn_y), dyn_r)

    # Draw path
    if path:
        draw_path(path)

    # Draw robot
    draw_robot(robot_x, robot_y)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
