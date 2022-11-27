from re import X
import pygame

import Config
from Rock import Rock
from Water import Water
from Rocks_luncher import Rocks_luncher


pygame.init()
flag = True
surface = pygame.display.set_mode(Config.WINDOW_SIZE)
clock = pygame.time.Clock()

water = Water((0, Config.WINDOW_SIZE[1]//2), Config.WINDOW_SIZE[0], Config.WINDOW_SIZE[1]//2)
rocks = Rocks_luncher() 

while flag:
    clock.tick(Config.FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            flag = False

    water.update_variables()
    rocks.update_variables(water, pygame.mouse.get_pos(), pygame.mouse.get_pressed())

    surface.fill(Config.FILL_COLOR)
    water.draw(surface)
    rocks.draw(surface)


    pygame.display.update()

        
    
    