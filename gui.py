import random
import time
import sys

import pygame

from simulation import Fluid


class GUI:
    def __init__(self, grid_width: int, grid_height: int):
        pygame.init()
        
        self.grid_width = grid_width
        self.grid_height = grid_height
        
        self.width = grid_width*4 + 20
        self.height = grid_height * 4 + 50
        
        # self.render_surface = pygame.Surface((self.width, self.height))
        self.render_surface = pygame.Surface((1600, 1200))
        
        self.COLOUR = {
            'WHITE' : (255, 255, 255),
            'GRAY' :  (127, 127, 127),
            'BLACK' : (000, 000, 000)
            }
        
        # self.window = pygame.display.set_mode((self.height, self.width))
        self.window = pygame.display.set_mode((1600, 1200))
        pygame.display.set_caption('Euclidean Fluid Simulation')
        
    def draw_pressure_2(self, pressure_list:list[float], width:int):
        for index, pressure in enumerate(pressure_list):
            x = index%width * 4
            y = index//width * 4
            colour =(random.randint(0, 255), # Red channel
                     random.randint(0, 255), # Green channel
                     random.randint(0, 255)) # Blue channel)

            pygame.draw.rect(self.render_surface, colour, (x, y, 4, 4))
        
        self.window.blit(self.render_surface, (0, 0))
        pygame.display.flip()  
        
    def draw_smoke(self, smoke_list:list[float], width):
        for index, smoke_overlay in enumerate(smoke_list):
            x = index%width * 4
            y = index//width * 4
            colour = (255*smoke_overlay,
                      255*smoke_overlay,
                      255*smoke_overlay)

            pygame.draw.rect(self.render_surface, colour, (x, y, 4, 4))
        
        self.window.blit(self.render_surface, (0, 0))
        pygame.display.flip()  
        
    def draw_dir(self, direction_list: list, width:int):
        l = []
        for i in direction_list:
            for ii in i:
                l.append(ii)
        
        for index, vector in enumerate(l):
            pygame.draw.line(self.render_surface,
                             (127,127,127),
                             (index%width * 12 + 100, index//width * 12 + 100),
                             (index%width * 12 + vector.x*5 + 100, index//width * 12 + vector.y*5 + 100))
            
        self.window.blit(self.render_surface, (0,0))
        pygame.display.flip()
        self.render_surface.fill((127,69,42))
        
        
        
    def mainloop(self):
        running = True
        T = time.time()
        F = Fluid(40, 30)
        for i in range(F.height):
            print(i)
            F.v_grid[i][0] = 5
        while running:
        
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print(f'User quit the game')
                    running = False
                elif event.type == pygame.KEYDOWN:
                    print(f'User pressed key {chr(event.key)}.')
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    print(f'User pressed mouse button at {event.pos}')
            

            self.window.fill(self.COLOUR['BLACK'])    
            F.solve_incompressible_2D_array()
            for i in range(F.height):
                F.v_grid[i][0] = 5
            
            # self.draw_simulation()
            # self.draw_limit_test()
            # self.draw_pressure_2([0 for _ in range(120_000)], 400)
            # self.draw_pressure_2([0 for _ in range(14_400)], 160)
            self.draw_dir(F.directional_grid, 40)
            delta_time = time.time()
            self.__show_fps(delta_time)
            if delta_time < 1: time.sleep(1 - delta_time)
            T = time.time()
            
    def quit(self):
        pygame.quit()
        
    def __show_fps(self, delta_time:float):
        sys.stdout.write(f'\rRender time: {round(delta_time* 1000, 2)}ms {round(1/delta_time, 3)} FPS')
        sys.stdout.flush()
        
gui = GUI(60, 80)
gui.mainloop()
gui.quit()

