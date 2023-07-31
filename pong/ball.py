from constance import *
import pygame


class Ball:
    MAX_VELOCITY = 5
    COLOR = WHITE
    RADIUS = BALL_RADIUS
    def __init__(self, x, y):
        self.x = self.original_x = x
        self.y = self.original_y = y
    
        self.x_velocity = self.MAX_VELOCITY
        self.y_velocity = 0

    def draw(self, win):
        pygame.draw.circle(win, self.COLOR,(self.x,self.y),self.RADIUS)

    def move(self):
        self.x += self.x_velocity
        self.y += self.y_velocity
        
        if self.y_velocity > self.MAX_VELOCITY:
            self.y_velocity = self.MAX_VELOCITY
        elif self.y_velocity < -self.MAX_VELOCITY:
            self.y_velocity = -self.MAX_VELOCITY

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.y_velocity = 0