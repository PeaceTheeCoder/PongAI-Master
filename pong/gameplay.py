import pygame
from constance import *
from ball import *
from paddle import *
from player import *

#Initializing pygame and puting window roperties.
pygame.init()
WINDOW = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("PongAI Master")
left_player_score = 0
right_player_score = 0



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
    if (ball.y + ball.RADIUS >= HEIGHT) or (ball.y - ball.RADIUS <= 0):
        ball.y_velocity *= -1

    #check if the ball hit the paddles.
    if ball.x_velocity < 0:
        if ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.height:
            if ball.x - ball.RADIUS <= left_paddle.x + left_paddle.width:
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
            if ball.x + ball.RADIUS >= right_paddle.x:
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
    if ball.x - ball.RADIUS < 0:
        right_player.change_score()
        ball.reset()
        left_paddle.reset()
        right_paddle.reset()

    if ball.x + ball.RADIUS > WIDTH:
        left_player.change_score()
        ball.reset()
        left_paddle.reset()
        right_paddle.reset()


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

    ball = Ball(WIDTH//2, HEIGHT//2)

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
            left_player.reset()
            right_player.reset()
            left_paddle.reset()
            right_paddle.reset()
        

    
    pygame.quit()

if __name__ == "__main__":
    main()
