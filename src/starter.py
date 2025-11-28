# src/starter.py
import pygame
import sys
import math
from robot import Robot

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Step 3 - Static Obstacles & Collision")
clock = pygame.time.Clock()
font = pygame.font.SysFont("consolas", 16)

robot = Robot(100, 300)

# Define some static obstacles (rectangles and circles) in pixel coordinates
static_rects = [
    # (center_x, center_y, width, height)
    (300, 200, 140, 60),
    (540, 380, 160, 60),
    (420, 120, 120, 50),
]

static_circles = [
    # (center_x, center_y, radius)
    (180, 450, 30),
    (660, 200, 40),
]

def clamp(v, a, b):
    return max(a, min(b, v))

def circle_rect_collision(cx, cy, cr, rx, ry, rw, rh):
    """
    cx,cy,cr: circle center & radius
    rx,ry: rect center coordinates (pixels)
    rw,rh: rect width,height
    returns True if collision
    """
    # rect bounds
    left = rx - rw/2
    right = rx + rw/2
    top = ry - rh/2
    bottom = ry + rh/2
    # closest point in rect to circle center
    closest_x = clamp(cx, left, right)
    closest_y = clamp(cy, top, bottom)
    dx = cx - closest_x
    dy = cy - closest_y
    return dx*dx + dy*dy <= cr*cr

def circle_circle_collision(x1, y1, r1, x2, y2, r2):
    dx = x1 - x2
    dy = y1 - y2
    return dx*dx + dy*dy <= (r1 + r2)**2

def collides_at(x, y):
    """Check if robot (circle at x,y) collides with any static obstacle"""
    r = robot.radius
    # rects
    for (rx, ry, rw, rh) in static_rects:
        if circle_rect_collision(x, y, r, rx, ry, rw, rh):
            return True
    # circles
    for (cx, cy, cr) in static_circles:
        if circle_circle_collision(x, y, r, cx, cy, cr):
            return True
    # bounds (keep inside window)
    if x - r < 0 or x + r > WIDTH or y - r < 0 or y + r > HEIGHT:
        return True
    return False

def draw_obstacles(screen):
    # rects filled red
    for (rx, ry, rw, rh) in static_rects:
        rect = pygame.Rect(int(rx - rw/2), int(ry - rh/2), int(rw), int(rh))
        pygame.draw.rect(screen, (200, 60, 60), rect)
        # optional border
        pygame.draw.rect(screen, (120, 20, 20), rect, 2)
    # circles orange
    for (cx, cy, cr) in static_circles:
        pygame.draw.circle(screen, (200,140,60), (int(cx), int(cy)), int(cr))
        pygame.draw.circle(screen, (120,70,20), (int(cx), int(cy)), int(cr), 2)

paused = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit(); sys.exit()
            elif event.key == pygame.K_SPACE:
                paused = not paused

    keys = pygame.key.get_pressed()
    # forward/back control: -1 back, 0 none, +1 forward
    forward = 0
    if keys[pygame.K_UP]:
        forward = 1
    elif keys[pygame.K_DOWN]:
        forward = -1
    # turn: -1 left, +1 right
    turn = 0
    if keys[pygame.K_LEFT]:
        turn = -1
    elif keys[pygame.K_RIGHT]:
        turn = 1

    if not paused:
        # get proposed pose from robot.move (without applying)
        nx, ny, nang = robot.move(forward, turn)
        # collision check at proposed location
        if not collides_at(nx, ny):
            # safe -> apply
            robot.apply_pose(nx, ny, nang)
        else:
            # collision: simple response -> do not apply forward motion,
            # but allow rotation in place (so user can turn away)
            # apply rotation only if no collision when only rotating
            # check rotating in place (same x,y but different angle) - always safe here
            # so apply only angle update:
            robot.apply_pose(robot.x, robot.y, nang)

    # draw
    screen.fill((30,30,30))
    draw_obstacles(screen)
    robot.draw(screen)

    # HUD
    hud = [
        "Step 3: Static obstacles & collision",
        "Use arrow keys to move (UP/DOWN = forward/back, LEFT/RIGHT = turn)",
        "SPACE = pause, ESC = quit",
        f"Robot pos: x={int(robot.x)}, y={int(robot.y)}"
    ]
    for i, line in enumerate(hud):
        surf = font.render(line, True, (220,220,220))
        screen.blit(surf, (8, 8 + i*18))

    pygame.display.flip()
    clock.tick(60)
