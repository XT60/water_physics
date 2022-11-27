import pygame
import Config
import math
import random

def distance(pos1, pos2):
    return math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)


class Rock:
    def __init__(self, x, y):
        self.pos = [x,y]
        self.radius = 15
        self.color = (20,20,20)
        self.gravity = 0.4
        self.water_resistance = 0.35
        self.momentum = [0,0]
        self.in_water = False
        self.water_enter_resistance = 0.8

    
    def calculate_left_force(self, static_rock):
        # z twierdzenia cosinusów
        pass

    def update_variables(self, water):
        self.pos[0] += self.momentum[0]
        self.pos[1] += self.momentum[1]
        collision = True
        while not collision:
            collision = False
            # for s_rock in static_rocks:
            #     if distance(self.pos, s_rock.pos) < s_rock.radius + self.radius:
            #         left_force = s_rock.radius + self.radius - distance(self.pos, s_rock.pos)
            #         prev_motion_distance = math.sqrt(self.momentum[0]**2 + self.momentum[1]**2)
            #         self.pos[0] -= self.momentum[0]/prev_motion_distance * left_force
            #         self.pos[1] -= self.momentum[1]/prev_motion_distance * left_force

            #         if self.momentum[0] == 0:
            #             prev_motion_angle = math.pi/2
            #         else:
            #             prev_motion_angle = math.asin(math.sqrt(self.momentum[0]**2 + self.momentum[1]**2)/self.momentum[0])

            #         collision = True
            #         break
            
        
        
        if not self.in_water:
            area = (math.floor((max(self.pos[0] - self.radius, 0))/Config.WATER_RECT_DENSITY) , math.ceil((min(self.pos[0] + self.radius, Config.WINDOW_SIZE[0]))/Config.WATER_RECT_DENSITY))
            for i in range(*area):
                if self.pos[1] > Config.WINDOW_SIZE[1] - water.heights[i]:
                    self.in_water = True
                    self.momentum[1] *= self.water_enter_resistance
                    water.drop_force(self.pos[0], self.radius, self.momentum[1]*2)
                    break

        if self.in_water:
            self.momentum[1] += self.gravity - self.water_resistance
        else:
            self.momentum[1] += self.gravity

        


    def draw(self, surface:pygame.Surface):
        pygame.draw.circle(surface, self.color, self.pos, self.radius)
