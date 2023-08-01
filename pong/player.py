from .constance import *
import pygame

#player properties class
class Player:
    FONTSIZE = 25
    COLOR = WHITE
    def __init__(self, name, score, hits, left, window_width):
        self.name = name
        self.score = self.original_score  = score
        self.hits = self.original_hits = hits
        self.left = left
        self.window_width = window_width

    def draw(self, win):
        font = pygame.font.SysFont(None, self.FONTSIZE)
        score_text = font.render(f"{self.name} : {str(self.score)}", True, self.COLOR)

        if self.left:
            score_rect = score_text.get_rect(topleft=(PADDING, PADDING))
        else:
            score_rect = score_text.get_rect(topright=(self.window_width-PADDING, PADDING))

        win.blit(score_text,score_rect)

    def change_score(self, add = True):
        if add:
            self.score += 1
        else:
            self.score -= 1

    def change_hits(self, add = True):
        if add:
            self.hits += 1
        else:
            self.hits -= 1

    def get_score(self):
        return self.score
    
    def get_hits(self):
        return self.hits
    
    def get_name(self):
        return self.name
    
    def reset(self):
        self.score = self.original_score 
        self.hits = self.original_hits