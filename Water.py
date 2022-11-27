import pygame
import Config
import math
import random

def sign(value):
    if value >= 0:
        return 1
    else:
        return -1

class Water:
    def __init__(self, pos, width, height):
        self.pos = (pos[0], pos[1] + height)        # left bottom corner
        self.neutral_height = pos[1] - height
        self.width = width                          # has to be round number of base Config.WATER_RECT_DENSITY
        self.neutral_height = height

        self.heights = []                           # height of rects where rect is ()
        self.velocities = []                        # height of rects where rect is ()

        self.k = 0.03                              # string constant
        self.dampening = 0.1
        self.spread = 0.3
        self.spreading_repeats = 4

        ### paricles
        self.paricle_radius = 4
        self.particles = []             # particle template = [pos[x,y], velocity[x,y]]
        self.particle_gravity = 0.2
        self.particle_vel_scalar = 0.5
        self.force_precision = [80, 120]            # /100
        
        self.fill_data()

    def drop_force(self, x, radius = 10, force = 5): 
        r = radius//Config.WATER_RECT_DENSITY           # radius in water units           
        i = x//Config.WATER_RECT_DENSITY
        actual_area = (max(0, i - 2*r), min(len(self.heights)-1, i + 2*r))
        arg_interval = 1 / (2*r)   
        curr_arg = -1
        for i in range(*actual_area):            # żeby ładnie się rozkładało jak parabola
            self.velocities[i] -= (-curr_arg*curr_arg + 1) * force
            curr_arg += arg_interval
        self.create_particles(x, radius, force)


    def create_particles(self, x, radius, force):
        r = radius//Config.WATER_RECT_DENSITY           # radius in water units           
        i = x//Config.WATER_RECT_DENSITY
        area_left = (max(0, i - 2*r), min(len(self.heights)-1, i - r))
        area_right = (max(0, i + r), min(len(self.heights)-1, i + 2*r))
        arg_interval = 1 / r   
        curr_arg = -2               # styczna to ax + b
        force = self.particle_vel_scalar*force
        for k in range(*area_left):
            pos = [k*Config.WATER_RECT_DENSITY, Config.WINDOW_SIZE[1] - self.heights[k]]

            a = 2*curr_arg
            angle = math.atan(a)
            velocity = [-force*math.cos(angle) * random.randint(*self.force_precision)/100, force*math.sin(angle) * random.randint(*self.force_precision)/100]

            self.particles.append([pos, velocity])
            curr_arg += arg_interval

        curr_arg = 1
        for k in range(*area_right):

            pos = [k*Config.WATER_RECT_DENSITY, Config.WINDOW_SIZE[1] - self.heights[k]]

            a = 2*curr_arg
            angle = math.atan(a)
            velocity = [force*math.cos(angle) * random.randint(*self.force_precision)/100, -force*math.sin(angle) * random.randint(*self.force_precision)/100]

            self.particles.append([pos, velocity])
            curr_arg += arg_interval
        
            
    def update_paricles(self):
        trash_bin = []
        for i, particle in enumerate(self.particles):
            pos, velocity = particle
            if  pos[0] < 0  or pos[0] >= Config.WINDOW_SIZE[0] or pos[1] > Config.WINDOW_SIZE[0] - self.heights[math.floor(pos[0]/Config.WATER_RECT_DENSITY)]:
                trash_bin.append(particle)
            else:
                self.particles[i][1][1] += self.particle_gravity
                self.particles[i][0][0] += velocity[0]
                self.particles[i][0][1] += velocity[1]
        for i in trash_bin:
            self.particles.remove(i)


    def fill_data (self):
        for _ in range (math.ceil(self.width/Config.WATER_RECT_DENSITY)):
            self.heights.append(self.neutral_height)
            self.velocities.append(0)
            
    
    def spread_force(self):
        for _ in range (self.spreading_repeats):
            left_deltas = [0 for _ in range(len(self.heights))]         # height delta from left side of rect
            right_deltas = [0 for _ in range(len(self.heights))]        # similarly
            for i in range(len(self.heights)):
                if i > 0:
                    left_deltas[i] = self.spread * (self.heights[i] - self.heights[i-1])
                    self.velocities[i-1] += left_deltas[i]
                if i < len(right_deltas) -1:
                    right_deltas[i] = self.spread * (self.heights[i] - self.heights[i+1])
                    self.velocities[i+1] += right_deltas[i]

            for i in range(len(self.heights)):
                if i > 0:
                    self.heights[i-1] += left_deltas[i]
                if i < len(right_deltas) -1:
                    self.heights[i+1] += right_deltas[i]

    def update_variables(self):
        self.spread_force()
        
        for i in range (len(self.heights)):             # updating velocities
            x = self.heights[i] - self.neutral_height
            self.velocities[i] += -(self.k * x)
            
        for i in range(len(self.heights)):              # dampening
            self.velocities[i] *= 1-self.dampening*sign(self.velocities[i])
            if abs(self.velocities[i]) < 0.05:
                self.velocities[i] = 0

        for i in range(len(self.heights)):              # updating velocities
            self.heights[i] += self.velocities[i]
        
        self.update_paricles()




    def draw(self, surface:pygame.Surface):
        image = pygame.Surface(Config.WINDOW_SIZE)
        image.set_colorkey((0,0,0))
        image.set_alpha(150)
        for i in range(len(self.heights)):
            height = self.heights[i]
            rect = (self.pos[0] + Config.WATER_RECT_DENSITY*i, self.pos[1] - height, Config.WATER_RECT_DENSITY, height)
            pygame.draw.rect(image, Config.WATER_COLOR, rect)
        
        for particle in self.particles:
            pygame.draw.circle(image, Config.WATER_COLOR, particle[0], self.paricle_radius)

        surface.blit(image, (0,0))