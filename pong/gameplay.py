import pygame
from constance import *

#Initializing pygame and puting window roperties.
pygame.init()
WINDOW = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("PongAI Master")
left_player_score = 0
right_player_score = 0


#player properties class
class Player:
    FONTSIZE = 25
    COLOR = WHITE
    def __init__(self, name, score, left):
        self.name = name
        self.score = score
        self.left = left

    def draw(self, win):
        font = pygame.font.SysFont(None, self.FONTSIZE)
        score_text = font.render(f"{self.name} : {str(self.score)}", True, self.COLOR)

        if self.left:
            score_rect = score_text.get_rect(topleft=(PADDING, PADDING))
        else:
            score_rect = score_text.get_rect(topright=(WIDTH-PADDING, PADDING))

        win.blit(score_text,score_rect)

    def change_score(self, add = True):
        if add:
            self.score += 1
        else:
            self.score -= 1

    def get_score(self):
        return self.score
    
    def get_name(self):
        return self.name



class Paddle:
    COLOR = WHITE
    HEIGHT = HEIGHT
    VELOCITY = 7
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
def handle_collision(ball, left_paddle, right_paddle, left_player, right_player):
    if (ball.y + ball.radius >= HEIGHT) or (ball.y - ball.radius <= 0):
        ball.y_velocity *= -1

    #check if the ball hit the paddles.
    if ball.x_velocity < 0:
        if ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.height:
            if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                ball.x_velocity *= -1
                # Change the vertical velocity based on the hit position
                ''' relative_hit_pos = (ball.y + ball.radius) - (left_paddle.y + left_paddle.height // 2)
                ball.y_velocity += relative_hit_pos // 5  # Adjust the division factor for desired sensitivity '''

                middle_y = left_paddle.y + left_paddle.height/2
                diff_in_y = ball.y - middle_y 
                reduction_factor = (left_paddle.height/2)/ball.MAX_VELOCITY
                y_velocity = diff_in_y/reduction_factor
                ball.y_velocity = y_velocity

        
    else:
        if ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.height:
            if ball.x + ball.radius >= right_paddle.x:
                ball.x_velocity *= -1
                # Change the vertical velocity based on the hit position
                ''' relative_hit_pos = (ball.y + ball.radius) - (right_paddle.y + right_paddle.height // 2)
                ball.y_velocity += relative_hit_pos // 5  # Adjust the division factor for desired sensitivity '''

                middle_y = right_paddle.y + right_paddle.height/2
                diff_in_y = ball.y - middle_y
                reduction_factor = (right_paddle.height/2)/ball.MAX_VELOCITY
                y_velocity = diff_in_y/reduction_factor
                ball.y_velocity = y_velocity

        
     # Check if the ball moves past the left or right edges
    if ball.x - ball.radius < 0:
        right_player.change_score()
        ball.x = WIDTH // 2
        ball.y = HEIGHT // 2
        ball.x_velocity = ball.MAX_VELOCITY
        ball.y_velocity = 0

    if ball.x + ball.radius > WIDTH:
        left_player.change_score()
        ball.x = WIDTH // 2
        ball.y = HEIGHT // 2
        ball.x_velocity = -ball.MAX_VELOCITY
        ball.y_velocity = 0 


#this function draws the current state of the window. 
def draw(window, paddles, ball, players):
    window.fill(BLACK)
    pygame.draw.line(window,GRAY,(WIDTH//2, 0),(WIDTH//2,HEIGHT),1)
    
    for paddle in paddles:
        paddle.draw(window)

    for player in players:
        player.draw(window)

    ball.draw(window)
    pygame.display.update()


def show_end_game_message(window, winner):
    font = pygame.font.SysFont(None, 60)
    
    text = font.render(f"Game ended! {winner.get_name()} won!", True, WHITE)
    text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))
    window.blit(text, text_rect)
    pygame.display.update()
    pygame.time.delay(5000)


def end_game(win, left_player, right_player):
    total_chances = 5 #Just have 5 chances per player
    if right_player.get_score() >= total_chances or left_player.get_score() >= total_chances:
        if right_player.get_score() >= total_chances:
            show_end_game_message(win, right_player)
            return True
        
        if left_player.get_score() >= total_chances:
            show_end_game_message(win, left_player)
            return True
        
    return False

    

def main():
    run = True
    clock = pygame.time.Clock()

    left_paddle = Paddle(PADDING, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle = Paddle(WIDTH-PADDING-PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH,PADDLE_HEIGHT)

    ball = Ball(WIDTH//2, HEIGHT//2,BALL_RADIUS)

    left_player = Player("Player 1", 0, True)
    right_player = Player("Player 2", 0, False)

    while run:
        clock.tick(FRAMES_PER_SECOND) #making sure that the while loop runs in a controllable speed, note that increasing this value also increase game speed.
        draw(WINDOW, [left_paddle, right_paddle], ball, [left_player, right_player])

        keys = pygame.key.get_pressed()
        handle_paddle_movement(keys, left_paddle, right_paddle)
        handle_collision(ball, left_paddle, right_paddle, left_player, right_player)
        

        ball.move()

        for event in pygame.event.get():
            #checking if the user pressed the red button to close the game
            if event.type == pygame.QUIT:
                run = False
                    
        if end_game(WINDOW ,left_player, right_player):
            left_player.score = 0
            right_player.score = 0
            left_paddle.y = HEIGHT//2 - PADDLE_HEIGHT//2
            right_paddle.y = HEIGHT//2 - PADDLE_HEIGHT//2
        

    
    pygame.quit()

if __name__ == "__main__":
    main()
