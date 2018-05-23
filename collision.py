import pygame as pg
pg.init()
display = pg.display
dimentions = (768,489)
display.set_mode(dimentions, 0)
display.set_caption("Flappy Bird")
icon = pg.image.load("Images/ico.png").convert_alpha()
display.set_icon(icon)
screen = pg.display.get_surface()#get the surface
background = pg.image.load("Images/initial_surface.jpg").convert()
bird = pg.image.load("Images/bird.png").convert_alpha()
bird_rect = bird.get_rect()
pipe = pg.image.load("Images/pipe.png").convert_alpha()
pipe_rect = pipe.get_rect()
bird_rect.x = 250
bird_rect.y = 150

pipe_rect.x = 250
pipe_rect.y = 150
while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()#Exit de Game
        if event.type == pg.KEYUP:
            if event.key == pg.K_RIGHT:
                bird_rect.x += 10
            else:
                bird_rect.x -= 10
            if bird_rect.colliderect(pipe_rect):
                print (bird_rect.colliderect(pipe_rect))
        screen.blit(background,(0,0))
        screen.blit(pipe,pipe_rect)
        screen.blit(bird, bird_rect)
        display.update()
