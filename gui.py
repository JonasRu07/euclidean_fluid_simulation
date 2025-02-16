import random
import time

import pygame


class GUI:
    def __init__(self, grid_width: int, grid_height: int):
        pygame.init()
        
        self.grid_width = grid_width
        self.grid_height = grid_height
        
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
        
    def draw_simulation(self, pressure_grid: list = [0 for i in range(100_000)], width: int = 50):
        for index, pressure in enumerate(pressure_grid):
            x, y = index//width, index %width
            pygame.draw.rect(self.window, 
                             (random.randint(0, 255),
                              random.randint(0, 255),
                              random.randint(0, 255)
                              ),
                            pygame.Rect(x*6, y*6, 5, 5))
        pygame.display.update()
            
            
            
    def draw_limit_test(self):
        rects = [(random.randint(0, self.width - 4), # X position
                      random.randint(0, self.height - 4), # Y position
                      random.randint(0, 255), # Red channel
                      random.randint(0, 255), # Green channel
                      random.randint(0, 255)) # Blue channel
                     for _ in range(300*400)]

            # Draw all rectangles to the offscreen surface
        for rect in rects:
            x, y, r, g, b = rect
            pygame.draw.rect(self.render_surface, (r, g, b), (x, y, 4, 4))
                
                
        # Blit the offscreen surface to the screen
        self.window.blit(self.render_surface, (0, 0))

        # Update the display
        pygame.display.flip()
        
    def mainloop(self):
        running = True
        T = time.time()
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
            
            
            # self.draw_simulation()
            self.draw_limit_test()
            print(f'Render time: {round((time.time()-T)* 1000, 2)}ms {round(1/(time.time()-T), 3)} FPS')
            T = time.time()
            
    def quit(self):
        pygame.quit()
        
        
gui = GUI(60, 80)
gui.mainloop()
gui.quit()