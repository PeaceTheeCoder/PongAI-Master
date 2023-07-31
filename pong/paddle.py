from constance import *
import pygame

class Paddle:
    COLOR = WHITE
    HEIGHT = HEIGHT
    VELOCITY = 7
    def __init__(self, x, y, width, height):
        self.x = self.original_x =x
        self.y = self.original_y = y
        self.width = width
        self.height = height

    def draw(self, win):
        pygame.draw.rect(win, self.COLOR,(self.x, self.y, self.width, self.height))

    def move(self, up=True):
        if up and self.y >= 0 :
            self.y -= self.VELOCITY
        else:
            if self.y < HEIGHT-self.height:
                self.y += self.VELOCITY


    def reset(self):
        self.x = self.original_x
        self.y = self.original_y