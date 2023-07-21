import pygame
from constance import *

#Initializing pygame and puting window roperties.
pygame.init()
WINDOW = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("PongAI Master")

class Paddle:
    COLOR = WHITE
    HEIGHT = HEIGHT
    VELOCITY = 10
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
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

class Ball:
    MAX_VELOCITY = 5
    COLOR = WHITE
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius  = radius

        self.x_velocity = self.MAX_VELOCITY
        self.y_velocity = 0

    def draw(self, win):
        pygame.draw.circle(win, self.COLOR,(self.x,self.y),self.radius)

    def move(self):
        self.x += self.x_velocity
        self.y += self.y_velocity






#this is for moving the paddles
def handle_paddle_movement(keys, left_paddle, right_paddle):
    if keys[pygame.K_w]:
        left_paddle.move(up = True)

    if keys[pygame.K_s]:
        left_paddle.move(up = False)

    if keys[pygame.K_UP]:
        right_paddle.move(up = True)

    if keys[pygame.K_DOWN]:
        right_paddle.move(up = False)


#this is for collision 
def handle_collision(ball, left_paddle, right_paddle):
    if (ball.y + ball.radius >= HEIGHT) or (ball.y - ball.radius <= 0):
        ball.y_velocity *= -1

    if ball.x_velocity < 0:
        if ball.y >= left_paddle.y and ball.y <= left_paddle.y+left_paddle.height:
            if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                ball.x_velocity *= -1

    else:
        if ball.y >= right_paddle.y and ball.y <= right_paddle.y+right_paddle.height:
            if ball.x + ball.radius >= right_paddle.x:
                ball.x_velocity *= -1




#this function draws the current state of the window. 
def draw(window, paddles, ball):
    window.fill(BLACK)
    pygame.draw.line(window,GRAY,(WIDTH//2, 0),(WIDTH//2,HEIGHT),1)
    for paddle in paddles:
        paddle.draw(window)

    ball.draw(window)
    
    pygame.display.update()

    

def main():
    run = True
    clock = pygame.time.Clock()

    left_paddle = Paddle(PADDING, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle = Paddle(WIDTH-PADDING-PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH,PADDLE_HEIGHT)

    ball = Ball(WIDTH//2, HEIGHT//2,BALL_RADIUS)

    while(run):
        clock.tick(FRAMES_PER_SECOND) #making sure that the while loop runs in a controllable speed, note that increasing this value also increase game speed.
        draw(WINDOW, [left_paddle, right_paddle], ball)

        keys = pygame.key.get_pressed()
        handle_paddle_movement(keys, left_paddle, right_paddle)
        handle_collision(ball, left_paddle, right_paddle)

        ball.move()

        for event in pygame.event.get():

            #checking if the user pressed the red button ro close the game
            if event.type == pygame.QUIT:
                run = False
                break

        

        
    
    pygame.quit()

if __name__ == "__main__":
    main()
