from .ball import Ball
from .paddle import Paddle
from .player import Player
from .constance import *
import random


class GameInformation:
    
    def __init__(self, left_player, right_player):
        self.left_player = left_player
        self.right_player = right_player


class Game:

    def __init__(self, window, window_width, window_height):
        self.window = window
        self.window_width = window_width
        self.window_height = window_height

        self.left_paddle = Paddle(PADDING, self.window_height//2 - PADDLE_HEIGHT//2)
        self.right_paddle = Paddle(self.window_width-PADDING-PADDLE_WIDTH, self.window_height//2 - PADDLE_HEIGHT//2)

        self.ball = Ball(self.window_width, self.window_height)
        
        self.left_player = Player("Player 1", 0, 0 , True,self.window_width)
        self.right_player = Player("Player 2", 0, 0, False, self.window_width)


    def __handle_collision(self):
        ball = self.ball
        left_paddle = self.left_paddle
        right_paddle = self.right_paddle

        left_player = self.left_player
        right_player = self.right_player

        #check if the ball hit the top or down.
        if (ball.y + ball.RADIUS >= self.window_height) or (ball.y - ball.RADIUS <= 0):
            ball.y_velocity = (ball.y_velocity *-1)+random.randint(-2,2)

        #check if the ball hit the paddles.
        if ball.x_velocity < 0:
            if ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.PADDLE_HEIGHT:
                if ball.x - ball.RADIUS <= left_paddle.x + left_paddle.PADDLE_WIDTH:
                    ball.x_velocity *= -1
                    # Change the vertical velocity based on the hit position
                    ''' relative_hit_pos = (ball.y + ball.radius) - (left_paddle.y + left_paddle.height // 2)
                    ball.y_velocity += relative_hit_pos // 5  # Adjust the division factor for desired sensitivity '''

                    middle_y = left_paddle.y + left_paddle.PADDLE_HEIGHT/2
                    diff_in_y = ball.y - middle_y 
                    reduction_factor = (left_paddle.PADDLE_HEIGHT/2)/ball.MAX_VELOCITY
                    y_velocity = diff_in_y/reduction_factor
                    ball.y_velocity = y_velocity
                    left_player.change_hits()

            
        else:
            if ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.PADDLE_HEIGHT:
                if ball.x + ball.RADIUS >= right_paddle.x:
                    ball.x_velocity *= -1
                    # Change the vertical velocity based on the hit position
                    ''' relative_hit_pos = (ball.y + ball.radius) - (right_paddle.y + right_paddle.height // 2)
                    ball.y_velocity += relative_hit_pos // 5  # Adjust the division factor for desired sensitivity '''

                    middle_y = right_paddle.y + right_paddle.PADDLE_HEIGHT/2
                    diff_in_y = ball.y - middle_y
                    reduction_factor = (right_paddle.PADDLE_HEIGHT/2)/ball.MAX_VELOCITY
                    y_velocity = diff_in_y/reduction_factor
                    ball.y_velocity = y_velocity
                    right_player.change_hits()

         # Check if the ball moves past the left or right edges
        if ball.x - ball.RADIUS < 0:
            right_player.change_score()
            right_paddle.reset()
            left_paddle.reset()
            ball.reset()

            

        if ball.x + ball.RADIUS > self.window_width:
            left_player.change_score()
            right_paddle.reset()
            left_paddle.reset()
            ball.reset()
            

    
    def draw(self, hits=False):
        
        self.window.fill(BLACK)
        
        self.left_paddle.draw(self.window)
        self.right_paddle.draw(self.window)

        self.ball.draw(self.window)
        
        if hits:
            self.ball.draw_hits(self.window, self.left_player.hits+self.right_player.hits)
        else:
            self.left_player.draw(self.window)
            self.right_player.draw(self.window)
        

    


    def move_paddle(self, left = True, up = True):

        if left:
            if up and self.left_paddle.y - Paddle.VELOCITY < 0:
                return False
            
            if not up and (self.left_paddle.y + Paddle.PADDLE_HEIGHT > self.window_height ):
                return False
            
            self.left_paddle.move(up)

        else:
            if up and self.right_paddle.y - Paddle.VELOCITY < 0:
                return False
            
            if not up and self.right_paddle.y + Paddle.PADDLE_HEIGHT > self.window_height:
                return False
            
            self.right_paddle.move(up)

        return True
    
    def loop(self):
        self.ball.move()
        self.__handle_collision()

        return GameInformation(self.left_player, self.right_player)
    

    def reset(self):
        self.left_player.reset()
        self.right_player.reset()
        self.left_paddle.reset()
        self.right_paddle.reset()
        self.ball.reset()










