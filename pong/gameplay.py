import pygame
from constance import *

#Initializing pygame and puting window roperties.
pygame.init()
WINDOW = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("PongAI Master")

class Paddle:
    COLOR = WHITE
    HEIGHT = HEIGHT
    VELOCITY = 5
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


#this function draws the current state of the window. 
def draw(window, paddles):
    window.fill(BLACK)
    for paddle in paddles:
        paddle.draw(window)

    pygame.draw.line(window,GRAY,(WIDTH//2, 0),(WIDTH//2,HEIGHT),1)
    pygame.display.update()

def main():
    run = True
    clock = pygame.time.Clock()

    left_paddle = Paddle(PADDING, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle = Paddle(WIDTH-PADDING-PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH,PADDLE_HEIGHT)

    while(run):
        clock.tick(FRAMES_PER_SECOND) #making sure that the while loop runs in a controllable speed, note that increasing this value also increase game speed.
        draw(WINDOW, [left_paddle, right_paddle])

        keys = pygame.key.get_pressed()
        handle_paddle_movement(keys, left_paddle, right_paddle)

        for event in pygame.event.get():

            #checking if the user pressed the red button ro close the game
            if event.type == pygame.QUIT:
                run = False
                break

        

        
    
    pygame.quit()

if __name__ == "__main__":
    main()
