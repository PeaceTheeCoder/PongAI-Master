from .constance import *
import pygame

class Paddle:
    COLOR = WHITE
    PADDLE_HEIGHT= PADDLE_HEIGHT
    PADDLE_WIDTH = PADDLE_WIDTH
    VELOCITY = 7
    def __init__(self, x, y):
        self.x = self.original_x =x
        self.y = self.original_y = y
        

    def draw(self, win):
        pygame.draw.rect(win, self.COLOR,(self.x, self.y, self.PADDLE_WIDTH, self.PADDLE_HEIGHT))

    def move(self, up=True):
        if up :
            self.y -= self.VELOCITY
        else:
            if self.y:
                self.y += self.VELOCITY


    def reset(self):
        self.x = self.original_x
        self.y = self.original_y