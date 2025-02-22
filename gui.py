import random
import tkinter as tk
import pygame

pygame.init()

class Colour:
    BLACK = (0, 0, 0)
    GRAY = (85,85,85)
    LIGHTGREY = (170,170,170)
    WHITE = (255,255,255)
    RED = (228,3,3)
    ORANGE = (255,140,0)
    YELLOW = (255,237,0)
    GREEN = (0,128,38)
    BLUE = (0,77,255)
    PURPLE = (117, 7, 135)
    LIGHTRED = (242,132,130)
    LIGHTGREEN = (167,201,87)
    
    @classmethod
    def hex_to_rgb(hex_colour: str) -> tuple[int, int, int]:
        if hex_colour[0] == '#':
            hex_colour = hex_colour[1:]
        return (int(hex_colour[0:2], 16), int(hex_colour[2:4], 16), int(hex_colour[4:6], 16))
    
    @classmethod
    def rgb_to_hex(rgb: tuple[int, int, int]) -> str:
        return f'#{hex(rgb[0])}{hex(rgb[1])}{hex(rgb[2])}'


class SimulationGUI:
    def __init__(self, grid_width: int, grid_height: int, action):
        
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.action = action
        
        self.width = grid_width*4 + 20
        self.height = grid_height * 4 + 50
        
        self.render_surface = pygame.Surface((self.width, self.height))
        
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
        self.render_surface.fill((127, 69, 42))
        
    def frame(self):
        self.window.fill(Colour.BLACK)
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
        return True
            
    def quit(self):
        print('GUI quitting.')
        pygame.quit()

