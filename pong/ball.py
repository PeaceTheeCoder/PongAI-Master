from .constance import *
import pygame
import math
import random


class Ball:
    MAX_VELOCITY = 7
    COLOR = WHITE
    RADIUS = BALL_RADIUS
    FONTSIZE = 25
    def __init__(self, window_width, window_height):
    
        self.window_width = window_width
        self.window_height = window_height

        self.x = self.original_x = self.window_width//2
        self.y = self.original_y = self.window_height//2

        angle = self._get_rand_angle(-30,30,[0])
        pos = 1 if random.random()< 0.5 else -1
    
        self.x_velocity = pos * abs(math.cos(angle) * self.MAX_VELOCITY)
        self.y_velocity = math.sin(angle)


    def _get_rand_angle(self, min_angle, max_angle, excluded):
        angle = 0
        while angle in excluded:
            angle = math.radians(random.randrange(min_angle, max_angle))

        return angle


    def draw(self, win):
        pygame.draw.circle(win, self.COLOR,(self.x,self.y),self.RADIUS)
        pygame.draw.line(win,GRAY,(self.original_x, 0),(self.original_x,self.window_height),1)#draw line also

    
    def draw_hits(self,win,hits):
        font = pygame.font.SysFont(None, self.FONTSIZE)
        hits_text = font.render(f"hits : {str(hits)}", True, self.COLOR)
        hits_rect = hits_text.get_rect(center=(self.window_width//2, PADDING*2))

        win.blit(hits_text,hits_rect)
        

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
        
        angle = self._get_rand_angle(-30,30,[0])
        pos = 1 if random.random()< 0.5 else -1
    
        self.x_velocity = pos * abs(math.cos(angle) * self.MAX_VELOCITY)
        self.y_velocity = math.sin(angle)