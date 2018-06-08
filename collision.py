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
pipe_group = pg.sprite.Group()
bird = pg.sprite.Sprite()
bird.image = pg.image.load("Images/bird.png").convert_alpha()
bird.rect = bird.image.get_rect()
pipe = pg.sprite.Sprite()
pipe.image = pg.image.load("Images/pipe.png").convert_alpha() #pygame.sprite.Group()
pipe.rect = pipe.image.get_rect()
bird.rect.x = 250
bird.rect.y = 150

pipe.rect.x = 250
pipe.rect.y = 150

pipe_group.add(pipe)
while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()#Exit de Game
        if event.type == pg.KEYUP:
            if event.key == pg.K_RIGHT:
                bird.rect.x += 10
            else:
                bird.rect.x -= 10
            print(pg.sprite.spritecollideany(bird, pipe_group))
        screen.blit(background,(0,0))
        screen.blit(pipe.image,pipe.rect)
        screen.blit(bird.image, bird.rect)
        display.update()
