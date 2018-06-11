from flappy_bird import *#import the file flappy_bird.py
import pygame as pg
#This block of code start the game
game = Game()#Create the object Game
game.composition()#Call the method/function composition
game.create_sprite_group()
climb = 0
while game.running:
    game.fps.tick(80)#Control the fps of the game
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()#Exit de Game
        if event.type == pg.KEYUP or event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                game.begin = True
                game.move = False
                game.bird_climb = True
            if event.key == pg.K_ESCAPE:
                exit()#Exit the game if the esc is press
            if event.key == pg.K_r:
                game.restart()
                game.begin = False
                game.move = True

    if game.move == True:#This block motions the init surface
        game.bird.moves()
        game.move_game_surface()
        game.show_game_surface()
        game.bird.show()
        ## TODO: Init messa
        #Call the init message here
    else:
        #Check if the bird hit the floor
        if game.bird.bird.rect.y == 350:
            game.begin = False

        if game.collide():
            #This loop makes the bird fall to the ground
            while game.bird.bird.rect.y < 350:
                game.show_game_surface()
                game.show_pipes()
                game.score.show()
                game.bird.fall()
                game.bird.show()
                game.display.flip()
            game.begin = False
            ## TODO: End_message
            #Call here the end game message

        #Make the bird fall if a command do jump is no given
        if game.bird_climb == False and game.begin == True:
            game.bird.fall()

        #Make the bird jump if the command is given
        if game.bird_climb == True and game.begin == True:
            game.bird.jump()
            climb += 1
            #Bird will move up for 15 iterations
            if climb == 20:
                climb = 0
                game.bird_climb = False
        if game.begin == True:
            game.generate_pipe()
            game.move_game_surface()
            game.show_game_surface()
            game.move_play_surface()
            game.check_score()
            game.score.show()
            game.bird.show()

    #Pygame method required to update the screen
    game.display.flip()
