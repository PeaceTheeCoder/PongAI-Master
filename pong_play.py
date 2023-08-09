import pygame
from pong import *


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


if __name__ =="__main__":
    pygame.init()
    WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("PongAI Master")

    run = True
    clock = pygame.time.Clock()

    gm = Game(WINDOW, WIDTH, HEIGHT)

    while run:
        clock.tick(FRAMES_PER_SECOND) 
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            gm.move_paddle(left=True ,up = True)

        if keys[pygame.K_s]:
            gm.move_paddle(left=True ,up = False)

        if keys[pygame.K_UP]:
            gm.move_paddle(left=False ,up = True)

        if keys[pygame.K_DOWN]:
            gm.move_paddle(left=False ,up = False)


        gm.draw()
        info = gm.loop()
        pygame.display.update()

        for event in pygame.event.get():
            #checking if the user pressed the red button to close the game
            if event.type == pygame.QUIT:
                run = False

        if end_game(WINDOW ,info.left_player, info.right_player):
            gm.reset()

    pygame.quit()