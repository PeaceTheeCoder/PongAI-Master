import pygame
from pong import *

import os
import neat
import pickle

'''
    In our Neural network, the output will me UP, Down or stand stll
    Our inputs will be paddle Y and ball y and distance between paddle and the ball |x|

'''

class PongGame:

    def __init__(self, window, width, height):
        self.game = Game(window, width, height)


    def test_ai(self, genome, config):
        net = neat.nn.FeedForwardNetwork.create(genome, config)

        run = True
        clock = pygame.time.Clock()

        while run:
            clock.tick(FRAMES_PER_SECOND) 
            keys = pygame.key.get_pressed()

            output = net.activate((self.game.left_paddle.y, self.game.ball.y, abs(self.game.left_paddle.x - self.game.ball.x)))
            action = output.index(max(output))

            print(action)
            if action == 1:
                self.game.move_paddle(left=True ,up = True)

            if action == 2:
                self.game.move_paddle(left=True ,up = False)

            if keys[pygame.K_UP]:
                self.game.move_paddle(left=False ,up = True)

            if keys[pygame.K_DOWN]:
                self.game.move_paddle(left=False ,up = False)


            self.game.draw()
            info = self.game.loop()
            pygame.display.update()

            for event in pygame.event.get():
                #checking if the user pressed the red button to close the game
                if event.type == pygame.QUIT:
                    run = False
                    quit()

        pygame.quit()

            

        

    def train_ai(self, genome1, genome2, config):

        net1 = neat.nn.FeedForwardNetwork.create(genome1, config)
        net2 = neat.nn.FeedForwardNetwork.create(genome2, config)

        run = True 
        while run:

            output1 = net1.activate((self.game.left_paddle.y, self.game.ball.y, abs(self.game.left_paddle.x - self.game.ball.x)))
            action1 = output1.index(max(output1))

            output2 = net2.activate((self.game.right_paddle.y, self.game.ball.y, abs(self.game.right_paddle.x - self.game.ball.x)))
            action2 = output2.index(max(output2))


            if action1 == 1:
                self.game.move_paddle(left=True ,up = True)

            if action1 == 2:
                self.game.move_paddle(left=True ,up = False)

            if action2 == 1:
                self.game.move_paddle(left=False ,up = True)

            if action2 == 2:
                self.game.move_paddle(left=False ,up = False)

            info = self.game.loop()
            self.game.draw(True)
            pygame.display.update() 

            for event in pygame.event.get():
                #checking if the user pressed the red button to close the game
                if event.type == pygame.QUIT:
                    quit()

            if info.left_player.score >=1 or info.right_player.score >=1 or info.left_player.hits > 50:
                self.calculate_fitness(genome1, genome2, info)
                break
        
    def calculate_fitness(self, genome1, genome2, info):
        genome1.fitness += info.left_player.hits
        genome2.fitness += info.right_player.hits
            
            


def eval_genomes(genomes, config):
    pygame.init()
    WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("PongAI Master - AI Taining")


    for i, (genome_id1, genome1) in enumerate(genomes):
        if i == len(genomes)-1:
            break

        genome1.fitness = 0 
        for genome_id2, genome2 in genomes[i+1:]:
            genome2.fitness = 0 if genome2.fitness == None else genome2.fitness
            game = PongGame(WINDOW, WIDTH, HEIGHT)
            game.train_ai(genome1,genome2, config)



def run_neat(config):
    #p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-79')
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    p.add_reporter(neat.StatisticsReporter())
    p.add_reporter(neat.Checkpointer(1))

    best_genome = p.run(eval_genomes, 1)

    with open("best_ai.pickle", "wb") as f:
        pickle.dump(best_genome, f)

def test_ai(config):
    pygame.init()
    WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("PongAI Master - AI vs You")

    with open("best_ai.pickle", "rb") as f:
        best_genome = pickle.load(f)
        game = PongGame(WINDOW, WIDTH,HEIGHT)
        game.test_ai(best_genome,config)



if __name__ =="__main__":
   
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir,"config.txt")

    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
    #run_neat(config)

    test_ai(config)