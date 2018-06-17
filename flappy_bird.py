#!/usr/bin/env python3
#font: ubuntumono
import pygame as pg
import time
import random

class Game(object):
    #Initialize the pygame module and others atributes
    def __init__(self):
        #Atributes of the pygame settings
        pg.init()
        self.display = pg.display
        self.dimentions = (768,489)
        self.display.set_mode(self.dimentions, 0)
        self.display.set_caption("Flappy Bird")
        self.icon = pg.image.load("Images/ico.png").convert_alpha()
        self.display.set_icon(self.icon)
        self.screen = pg.display.get_surface()#get the surface

        #Atributes of the game control
        self.begin = False
        self.running = True
        self.move = True
        self.fps = pg.time.Clock()
        self.pipe_list = []
        self.pipe_to_show = []
        #Sprite group, use de make the collisions
        self.pipe_group = pg.sprite.Group()
        self.bird_climb = False

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
        self.score = Score(self.screen)

        #Creates object Pipe, with opening=130 (space to the bird pass through), x=820
        self.pipe1 = Pipe(self.screen, 130, 820)
        self.pipe2 = Pipe(self.screen, 130, 820)
        self.pipe3 = Pipe(self.screen, 130, 820)
        self.pipe4 = Pipe(self.screen, 130, 820)
        self.pipe5 = Pipe(self.screen, 130, 820)
        self.pipe6 = Pipe(self.screen, 130, 820)
        self.pipe7 = Pipe(self.screen, 130, 820)
        self.pipe_to_show.append(self.pipe1)#First pipe that is showed
        self.pipe_group.add(self.pipe1.pipe_up, self.pipe1.pipe_down)
        self.pipe_list.append(self.pipe2)
        self.pipe_list.append(self.pipe3)
        self.pipe_list.append(self.pipe4)
        self.pipe_list.append(self.pipe5)
        self.pipe_list.append(self.pipe6)
        self.pipe_list.append(self.pipe7)

    def create_sprite_group(self):
        #Add the pipes into the sprite_group to after check the collision
        for el in self.pipe_list:
            self.pipe_group.add(el.pipe_up, el.pipe_down)

    #Moves and shows the pipes for each pipe object of the list pipe_to_show
    def move_play_surface(self):
        for pipe in self.pipe_to_show:
            pipe.moves()
            pipe.show()

    def show_pipes(self):
        for pipe in self.pipe_to_show:
            pipe.show()

    def generate_pipe(self):
        #When the last pipe of list pipe_to_show is at the possition 656
        #the next pipe is inserted to be showed
        if self.pipe_to_show[-1].pipe_down.rect.x == 656:
            self.pipe_to_show.append(random.choice(self.pipe_list))
            #remove the elemet that was add in the list to show
            #Index -1 to get the last element
            self.pipe_list.remove(self.pipe_to_show[-1])

        #position 52 represents when the tube reaches the end of the path
        if self.pipe_to_show[0].pipe_down.rect.x < -52:
            #reposition the pipe
            self.pipe_to_show[0].pipe_down.rect.x = 820
            self.pipe_to_show[0].pipe_up.rect.x = 820
            #The code line below decreases the size of the opening of the pipe
            #The decrease is bases in the score of the game
            self.pipe_to_show[0].pipe_up.rect.y += int(self.score.score / 2)
            self.pipe_list.append(self.pipe_to_show[0])
            self.pipe_to_show.remove(self.pipe_list[-1])

    def move_game_surface(self):
        self.init_surface.moves()
        self.cloud2.moves()
        self.cloud1.moves()

    def show_game_surface(self):
        self.init_surface.show()
        self.cloud2.show()
        self.cloud1.show()
        self.score.show()


    #Check if the bird is colliding with the sprite_group that contains the pipes
    def collide(self):
        if pg.sprite.spritecollideany(self.bird.bird, self.pipe_group) != None:
            return True
        else:
            return False
    def end_game(self):
        x = self.bird.bird.rect.x
        y = self.bird.bird.rect.y
        self.bird.bird.image = self.bird.bird_end
        self.bird.rect = self.bird.bird_end_rect
        self.bird.rect.x = x
        self.bird.rect.y = y

    def restart(self):
        #Set the bird to your initial position
        self.bird.bird.image = self.bird.bird_init
        self.bird.bird.rect = pg.Rect((130, 200), (48, 32))
        self.score.num_to_show = [self.score.num0]
        self.score.score = 0
        #Set each pipe to yours initials positions
        for el in self.pipe_to_show:
            el.pipe_down.rect.x = 820
            el.pipe_up.rect.x = 820
            el.pipe_up.rect.y -= 5 #increase the opening of the pipes
            self.pipe_list.append(el)
        #Remove al pipes os the list
        self.pipe_to_show.clear()
        #Add just one pipe to be showed
        self.pipe_to_show.append(el)
        self.pipe_list.remove(el)

    def check_score(self):
        if len(self.pipe_to_show) <= 5:
            if self.pipe_to_show[0].pipe_down.rect.x + 52 == 130:
                self.score.increase()
        else:
            if self.pipe_to_show[1].pipe_down.rect.x + 52 == 130:
                self.score.increase()

    #Write the code here
    # the iniciate message

    def game_start(self):
        pg.font.init()
        font= pg.font.Font('fonts/BradBunR.ttf',50)
        init_mes= font.render(" Press space to start ", True , (175,238,238))
        self.screen.blit(init_mes, (150, 225))

    #the game over message
    def game_over(self):
        pg.font.init()
        font = pg.font.Font('fonts/BradBunR.ttf',80)
        font2 = pg.font.Font('fonts/BradBunR.ttf',30) # to change the little text size
        over_mes = font.render(" GAME OVER ", True , (255,0,0))
        end_mes = font2.render(" press R to restart or esc to exit", True , (255,255,255))
        self.screen.blit(over_mes,(170, 150))
        self.screen.blit(end_mes,(160, 225))

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

class Bird():
    def __init__(self, screen):
        self.screen = screen
        self.fly = 0
        self.bird = pg.sprite.Sprite()
        self.bird_end = pg.image.load("Images/bird_end.png").convert_alpha()
        self.bird_end_rect = self.bird_end.get_rect()
        self.bird_init = pg.image.load("Images/bird1.png").convert_alpha()
        self.bird.image = self.bird_init
        self.bird.rect = pg.Rect((130, 200), (48, 32))

    def show(self):
        self.screen.blit(self.bird.image, self.bird.rect)#put the bird

    #Initial motion, bird up and down
    def moves(self):
        if self.fly == 0:
            self.bird.rect.y -= 1
        if self.bird.rect.y == 190:
            self.fly = 1
        if self.fly == 1:
            self.bird.rect.y += 1
        if self.bird.rect.y == 230:
            self.fly = 0

    #Make the bird falls
    def fall(self):
        self.bird.rect.y += 2

    def jump(self):
        self.bird.rect.y -= 3

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
            #Gets a random position to reposition the cloud
            self.xcloud = random.choice(self.new_x_position)
        else:
            self.xcloud -= 1

#Class that model the pipes - Bird obstacles
class Pipe():
    def __init__(self, screen, opening, x):
        self.screen = screen
        self.pipe_down = pg.sprite.Sprite()
        self.pipe_up = pg.sprite.Sprite()
        #gets a random image that represents the down pipe
        self.pipe_down.image = pg.image.load(random.choice(["Images/pipe_down1.png","Images/pipe_down2.png","Images/pipe_down3.png"])).convert_alpha()
        self.pipe_up.image = pg.image.load("Images/pipe_up.png")

        self.pipe_down.rect = self.pipe_down.image.get_rect()
        self.pipe_up.rect = self.pipe_up.image.get_rect()
        #Atributes about the position of the pipes
        self.pipe_down.rect.x = x
        self.pipe_up.rect.x = x
        #386 is the y value that represents the floor
        self.pipe_down.rect.y = (386 - self.pipe_down.image.get_height())
        #positions the pipe_up based in the size of the pipe_down
        self.pipe_up.rect.y = (self.pipe_down.rect.y - opening - self.pipe_up.image.get_height())

    def show(self):
        self.screen.blit(self.pipe_down.image, self.pipe_down.rect)#put pipe down
        self.screen.blit(self.pipe_up.image, self.pipe_up.rect)#put pipe up

    def moves(self):
        self.pipe_down.rect.x -= 2
        self.pipe_up.rect.x -= 2


class Score(object):
    def __init__(self, screen):
        self.screen = screen
        self.num0 = pg.image.load("Images/0.png")
        self.num1 = pg.image.load("Images/1.png")
        self.num2 = pg.image.load("Images/2.png")
        self.num3 = pg.image.load("Images/3.png")
        self.num4 = pg.image.load("Images/4.png")
        self.num5 = pg.image.load("Images/5.png")
        self.num6 = pg.image.load("Images/6.png")
        self.num7 = pg.image.load("Images/7.png")
        self.num8 = pg.image.load("Images/8.png")
        self.num9= pg.image.load("Images/9.png")
        self.num_list = [self.num0,self.num1,self.num2,self.num3,
                        self.num4,self.num5,self.num6,self.num7,
                        self.num8,self.num9]
        self.num_to_show = [self.num0]
        self.num_x = 336
        self.score = 0

    def increase(self):
        self.score += 1
        self.num_to_show = []
        #Gets each character of the string
        #Ex: score 10 = num_list[1] + num_list[0]
        for i in str(self.score):
            self.num_to_show.append(self.num_list[int(i)])

    def show(self):
        for num in self.num_to_show:
            self.screen.blit(num, (self.num_x, 100))
            self.num_x += 25#
        self.num_x = 336
