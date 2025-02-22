import random

import pygame


class SimulationGUI:
    def __init__(self, grid_width: int, grid_height: int, action):
        pygame.init()
        
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.action = action
        
        self.width = grid_width*4 + 20
        self.height = grid_height * 4 + 50
        
        self.render_surface = pygame.Surface((self.width, self.height))
        
        self.COLOUR = {
            'WHITE' : (255, 255, 255),
            'GRAY' :  (127, 127, 127),
            'BLACK' : (000, 000, 000)
            }
        
        self.window = pygame.display.set_mode((self.height, self.width))
        pygame.display.set_caption('Euclidean Fluid Simulation')
        
    def draw_pressure(self, pressure_list:list[float], width:int):
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
                             (index%width * 20 + 50, index//width * 20 + 50),
                             (index%width * 20 + vector.x*5 + 50, index//width * 20 + vector.y*5 + 50))
            
        self.window.blit(self.render_surface, (0,0))
        pygame.display.flip()
        self.render_surface.fill((127,69,42))
        
    def frame(self):
        self.window.fill(self.COLOUR['BLACK'])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print(f'User quit the game')
                return(False)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print(f'User quit the game')
                    return False 
                else:                   
                    print(f'User pressed key {chr(event.key)}.')
            elif event.type == pygame.MOUSEBUTTONDOWN:
                print(f'User pressed mouse button at {event.pos}')
            
    def quit(self):
        print('GUI quitting.')
        pygame.quit()
