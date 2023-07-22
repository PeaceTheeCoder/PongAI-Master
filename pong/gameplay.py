import pygame
from constance import *

#Initializing pygame and puting window roperties.
pygame.init()
WINDOW = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("PongAI Master")
left_player_score = 0
right_player_score = 0

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
        self.y_velocity = self.MAX_VELOCITY

    def draw(self, win):
        pygame.draw.circle(win, self.COLOR,(self.x,self.y),self.radius)

    def move(self):
        self.x += self.x_velocity
        self.y += self.y_velocity
        
        if self.y_velocity > self.MAX_VELOCITY:
            self.y_velocity = self.MAX_VELOCITY
        elif self.y_velocity < -self.MAX_VELOCITY:
            self.y_velocity = -self.MAX_VELOCITY

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
        if ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.height:
            if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                ball.x_velocity *= -1
                # Change the vertical velocity based on the hit position
                relative_hit_pos = (ball.y + ball.radius) - (left_paddle.y + left_paddle.height / 2)
                ball.y_velocity += relative_hit_pos / 15  # Adjust the division factor for desired sensitivity

    else:
        if ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.height:
            if ball.x + ball.radius >= right_paddle.x:
                ball.x_velocity *= -1
                # Change the vertical velocity based on the hit position
                relative_hit_pos = (ball.y + ball.radius) - (right_paddle.y + right_paddle.height / 2)
                ball.y_velocity += relative_hit_pos / 15  # Adjust the division factor for desired sensitivity

#this function draws the current state of the window. 
def draw(window, paddles, ball, font):
    window.fill(BLACK)
    pygame.draw.line(window,GRAY,(WIDTH//2, 0),(WIDTH//2,HEIGHT),1)
    
    # Draw left player's score near the left paddle
    left_score_text = font.render("Player1: " + str(left_player_score), True, WHITE)
    left_score_rect = left_score_text.get_rect(topleft=(PADDING, 20))
    window.blit(left_score_text, left_score_rect)

    # Draw right player's score near the right paddle
    right_score_text = font.render("Player2: " + str(right_player_score), True, WHITE)
    right_score_rect = right_score_text.get_rect(topright=(WIDTH - PADDING, 20))
    window.blit(right_score_text, right_score_rect)
    
    for paddle in paddles:
        paddle.draw(window)

    ball.draw(window)
    pygame.display.update()

def show_end_game_message(window, winner):
    font = pygame.font.SysFont(None, 60)
    if winner == "None":
        text = font.render("Game ended in a tie!", True, WHITE)
    else:
        text = font.render(f"Game ended! Player {winner} won!", True, WHITE)
    text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))
    window.blit(text, text_rect)
    pygame.display.update()
    pygame.time.delay(2000)

    

def main():
    run = True
    clock = pygame.time.Clock()
    global left_player_score, right_player_score
    winner = None
    chances_remaining = 5 #Just have 5 chances per player

    left_paddle = Paddle(PADDING, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle = Paddle(WIDTH-PADDING-PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH,PADDLE_HEIGHT)

    ball = Ball(WIDTH//2, HEIGHT//2,BALL_RADIUS)
    font = pygame.font.SysFont(None, 40)

    while run and chances_remaining > 0:
        clock.tick(FRAMES_PER_SECOND) #making sure that the while loop runs in a controllable speed, note that increasing this value also increase game speed.
        draw(WINDOW, [left_paddle, right_paddle], ball, font)

        keys = pygame.key.get_pressed()
        handle_paddle_movement(keys, left_paddle, right_paddle)
        handle_collision(ball, left_paddle, right_paddle)
        
        # Check if the ball moves past the left or right edges
        if ball.x - ball.radius <= 0:
            right_player_score += 1
            ball.x = WIDTH // 2
            ball.y = HEIGHT // 2
            ball.x_velocity = ball.MAX_VELOCITY
            ball.y_velocity = 0

        if ball.x + ball.radius >= WIDTH:
            left_player_score += 1
            ball.x = WIDTH // 2
            ball.y = HEIGHT // 2
            ball.x_velocity = -ball.MAX_VELOCITY
            ball.y_velocity = 0

        ball.move()

        for event in pygame.event.get():
            #checking if the user pressed the red button to close the game
            if event.type == pygame.QUIT:
                run = False
                    
        if run and (right_player_score >= chances_remaining or left_player_score >= chances_remaining):
            # Determine the winner based on the scores
            if left_player_score > right_player_score:
                winner = "1"
            elif right_player_score > left_player_score:
                winner = "2"
            else:
                winner = "None"  # It's a tie
            chances_remaining = 0 # End the game loop
        
    if winner == "None":
        show_end_game_message(WINDOW, winner)
    elif winner:
        show_end_game_message(WINDOW, winner)
    
    pygame.quit()

if __name__ == "__main__":
    main()
