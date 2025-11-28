# src/robot.py
import pygame
import math

class Robot:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 20  # pixels
        self.speed = 3.0  # pixels per frame (adjust)
        self.angle = 0.0  # radians

    def move(self, forward, turn):
        """
        forward: -1..1  (back, stop, forward)
        turn: -1..1 (left, none, right)
        This method updates pose but DOES NOT check collisions.
        """
        # update angle from turn
        self.angle += turn * 0.06  # turning speed
        # compute displacement
        dx = forward * self.speed * math.cos(self.angle)
        dy = forward * self.speed * math.sin(self.angle)
        # return proposed new pos (without applying)
        return self.x + dx, self.y + dy, self.angle

    def apply_pose(self, x, y, angle):
        self.x = x; self.y = y; self.angle = angle

    def draw(self, screen):
        # body
        pygame.draw.circle(screen, (0, 200, 0), (int(self.x), int(self.y)), self.radius)
        # heading
        hx = self.x + math.cos(self.angle) * (self.radius + 12)
        hy = self.y + math.sin(self.angle) * (self.radius + 12)
        pygame.draw.line(screen, (255, 255, 0), (int(self.x), int(self.y)), (int(hx), int(hy)), 3)
