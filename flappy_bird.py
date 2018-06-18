#!/usr/bin/env python3
#font: ubuntumono
import pygame as pg
import time
import random
class Game(object):
    #Initialize the pygame module and others atributes
    def __init__(self):
        pg.init()
        self.display = pg.display
        self.dimentions = (768,489)
        self.display.set_mode(self.dimentions, 0)
        self.display.set_caption("Flappy Bird")
        self.icon = pg.image.load("Images/ico.png").convert_alpha()
        self.display.set_icon(self.icon)
        self.screen = pg.display.get_surface()#get the surface
        self.begin = False
        self.running = True
        self.move = True
        self.fps = pg.time.Clock()
        self.pipe_list = []
        self.pipe_to_show = []

    #Instantiate the objects that will compose the game
    def composition(self):
        #Create the object which represents the initial game interface
        #Bird just fly to up and down and the clouds float in the sky
        self.init_surface = Initial_Surface(self.screen)
        #Creates the object bird
        self.bird = Bird(self.screen)
        #Create object cloud in the position x=200,y=10
        self.cloud1 = Cloud(self.screen, 200, 10)
        #Create object cloud
        self.cloud2 = Cloud(self.screen, 760, 100)

        #Creates object Pipe, with opening=150 (space to the bird pass through), x=820
        self.pipe1 = Pipe(self.screen, 120, 820)
        self.pipe2 = Pipe(self.screen, 120, 820)
        self.pipe3 = Pipe(self.screen, 120, 820)
        self.pipe4 = Pipe(self.screen, 120, 820)
        self.pipe5 = Pipe(self.screen, 120, 820)
        self.pipe6 = Pipe(self.screen, 120, 820)
        self.pipe_to_show.append(self.pipe1)
        self.pipe_list.append(self.pipe2)
        self.pipe_list.append(self.pipe3)
        self.pipe_list.append(self.pipe4)
        self.pipe_list.append(self.pipe5)
        self.pipe_list.append(self.pipe6)

    def move_play_surface(self):
        for pipe in self.pipe_to_show:
            pipe.moves()
            pipe.show()

    def show_pipes(self):
        for pipe in self.pipe_to_show:
            pipe.show()

    def generate_pipe(self):
        #Take the last object of the list
        if self.pipe_to_show[-1].pipe_down_rect.x == 664:
            self.pipe_to_show.append(random.choice(self.pipe_list))
            #remove the elemet that was add in the list to show
            #Index -1 to get the last element
            self.pipe_list.remove(self.pipe_to_show[-1])
        if self.pipe_to_show[0].pipe_down_rect.x < -52:
            self.pipe_to_show[0].pipe_down_rect.x = 820
            self.pipe_to_show[0].pipe_up_rect.x = 820
            #The code line below decreases the size of hte opening
            self.pipe_to_show[0].pipe_up_rect.y += 1
            self.pipe_list.append(self.pipe_to_show[0])
            self.pipe_to_show.remove(self.pipe_list[-1])

    def move_game_surface(self):
        self.init_surface.moves()
        self.init_surface.show()

        self.cloud2.moves()
        self.cloud2.show()

        self.cloud1.moves()
        self.cloud1.show()

    #Check if the bird is colliding with the pipe up and the pipe down
    def collide(self):
        try:
            pipe = self.pipe_to_show[1]
        except IndexError:
            pipe = self.pipe_to_show[0]
        #Get the first pipe
        if pipe.pipe_down_rect.x >= 130 or pipe.pipe_down_rect.x <= 192:
            if self.bird.bird_rect.colliderect(pipe.pipe_up_rect) or self.bird.bird_rect.colliderect(pipe.pipe_down_rect):
                return True
        else:
            return False

class Initial_Surface():
    def __init__(self, screen):
        self.screen = screen
        self.xbar = 0
        self.xbar1 = 768
        self.background = pg.image.load("Images/initial_surface.jpg").convert()
        self.bar = pg.image.load("Images/bar.png").convert_alpha()
        self.bar1 = pg.image.load("Images/bar.png").convert_alpha()

    def show(self):
        self.screen.blit(self.background, (0,0))#put de default image
        self.screen.blit(self.bar, (self.xbar, 385))#put bar
        self.screen.blit(self.bar1, (self.xbar1, 385))#put bar1

    def moves(self):
        if self.xbar == -766:
            self.xbar = 768
        if self.xbar1 == -766:
            self.xbar1 = 768
        else:
            self.xbar -= 2
            self.xbar1 -= 2
        #self.bar.scroll(self.xbar, 385)
        #self.bar1.scroll(self.xbar1, 385)

class Bird():
    def __init__(self, screen):
        self.screen = screen
        self.fly = 0
        self.bird = pg.image.load("Images/bird.png").convert_alpha()
        self.bird_rect = self.bird.get_rect()
        self.bird_rect.x = 130
        self.bird_rect.y = 200

    def show(self):
        self.screen.blit(self.bird, self.bird_rect)#put the bird

    def moves(self):
        #time.sleep(0.002)
        if self.fly == 0:
            self.bird_rect.y -= 1
        if self.bird_rect.y == 190:
            self.fly = 1
        if self.fly == 1:
            self.bird_rect.y += 1
        if self.bird_rect.y == 230:
            self.fly = 0

    #Faz o bird cair
    def fall(self):
        self.bird_rect.y += 1

    def jump(self):
        self.bird_rect.y -= 30

class Cloud():
    def __init__(self,screen, x, y):
        self.screen = screen
        self.xcloud = x #740
        self.ycloud = y #40
        self.cloud = pg.image.load("Images/cloud.png").convert_alpha()
        self.new_x_position = [200, 350, 900, 800, 1000]

    def show(self):
        self.screen.blit(self.cloud, (self.xcloud, self.ycloud))

    def moves(self):
        if self.xcloud == -205:
            self.xcloud = random.choice(self.new_x_position)
        else:
            self.xcloud -= 1
        #self.cloud.scroll(self.xsun, self.ysun)

#Class that creates the pipes - Bird obstacles
class Pipe():
    def __init__(self, screen, opening, x):
        self.screen = screen
        self.pipe_down = pg.image.load(random.choice(["Images/pipe_down1.png","Images/pipe_down2.png","Images/pipe_down3.png"])).convert_alpha()
        self.pipe_up = pg.image.load("Images/pipe_up.png")

        self.pipe_down_rect = self.pipe_down.get_rect()
        self.pipe_up_rect = self.pipe_up.get_rect()
        #Atributes about the position of the pipes
        self.pipe_down_rect.x = x
        self.pipe_up_rect.x = x
        #386 is the y value that represents the floor
        self.pipe_down_rect.y = (386 - self.pipe_down.get_height())
        self.pipe_up_rect.y = (self.pipe_down_rect.y - opening - self.pipe_up.get_height())

    def show(self):
        self.screen.blit(self.pipe_down, self.pipe_down_rect)#put pipe down
        self.screen.blit(self.pipe_up, self.pipe_up_rect)#put pipe up

    def moves(self):
        if self.pipe_down_rect.x < -52 and self.pipe_up_rect.x < -52:
            self.pipe_down_rect.x = 820
            self.pipe_up_rect.x = 820
        else:
            self.pipe_down_rect.x -= 2
            self.pipe_up_rect.x -= 2

#This block of code start the game
game = Game()#Create the object Game
game.composition()#Call the method/function composition
while game.running:
    game.fps.tick(90)
    if game.move:
        game.move_game_surface()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()#Exit de Game
        if event.type == pg.KEYUP:
            if event.key == pg.K_SPACE and game.move == True:
                game.begin = True
                game.bird.jump()

    if game.collide():
        #Set game.move = False to stop the play_surface
        game.move = False
        game.show_pipes()
    #Check if the bird touch the floor
    if game.bird.bird_rect.y == 350:
        game.move = False
        game.show_pipes()
    if game.begin == True and game.move == True:
        game.bird.fall()
        game.generate_pipe()
        game.move_play_surface()
    #Check if the bird is'nt start
    if game.begin == False:
        game.bird.moves()
    game.bird.show()
    game.display.flip()
