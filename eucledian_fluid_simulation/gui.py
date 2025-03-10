import random
import tkinter as tk
import time
import traceback

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
    def hex_to_rgb(cls, hex_colour: str) -> tuple[int, int, int]:
        if hex_colour[0] == '#':
            hex_colour = hex_colour[1:]
        return (int(hex_colour[0:2], 16), int(hex_colour[2:4], 16), int(hex_colour[4:6], 16))
    
    @classmethod
    def rgb_to_hex(cls, rgb: tuple[int, int, int]) -> str:
        return f'#{str(hex(rgb[0]))[2:].zfill(2)}{str(hex(rgb[1]))[2:].zfill(2)}{str(hex(rgb[2]))[2:].zfill(2)}'


class SimulationGUI:
    def __init__(self, grid_width: int, grid_height: int, get_visualize_data, action, fps):
        self.get_visualize_data = get_visualize_data
        self.action = action
        self.print_fps = fps
        
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.size_per_square = 1200//self.grid_width
        
        self.width = grid_width*self.size_per_square + 40
        self.height = grid_height*self.size_per_square + 40
        self.window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Euclidean Fluid Simulation')
        
    def draw_pressure(self, pressure_list:list[float], width:int):
        surface = pygame.Surface((self.width, self.height))
        for index, pressure in enumerate(pressure_list):
            x = index%width * 4
            y = index//width * 4
            colour =(random.randint(0, 255), # Red channel
                     random.randint(0, 255), # Green channel
                     random.randint(0, 255)) # Blue channel)

            pygame.draw.rect(surface, colour, (x, y, 4, 4))
        
        self.window.blit(surface, (0, 0))
        pygame.display.flip()  
        
    def draw_smoke(self, smoke_list:list[float], width):
        surface = pygame.Surface((self.width, self.height))
        for index, smoke_overlay in enumerate(smoke_list):
            x = index%width * 4
            y = index//width * 4
            colour = (255*smoke_overlay,
                      255*smoke_overlay,
                      255*smoke_overlay)

            pygame.draw.rect(surface, colour, (x, y, 4, 4))
        
        self.window.blit(surface, (0, 0))
        pygame.display.flip()  
        
    def draw_dir(self, direction_list: list, width:int):
        surface = pygame.Surface((self.width, self.height))
        l = []
        for i in direction_list:
            for ii in i:
                l.append(ii)

        for index, vector in enumerate(l):
            if not -0.1 < vector.x < 0.1 or not -0.1 < vector.y < 0.1:
                pygame.draw.line(surface,
                                Colour.WHITE,
                                (index%width *self.size_per_square + 20, index//width * self.size_per_square + 20),
                                (index%width * self.size_per_square + vector.x + 20, index//width * self.size_per_square + vector.y + 20))
                
        self.window.blit(surface, (0,0))
        pygame.display.flip()
        
    def loop(self):
        try:
            run = True
            while run:
                T = time.time()
                self.window.fill(Colour.BLACK)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        print(f'\n User quit the simulation')
                        run = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            print(f'\n User quit the simulation')
                            run = False
                        else:
                            try:      
                                print(f'\n User pressed key {chr(event.key)}.')
                            except: pass
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        print(f'\n User pressed mouse button at {event.pos}')
                self.action()
                self.draw_dir(self.get_visualize_data(), self.grid_width)
                # self.draw_pressure([0 for _ in range(self.grid_height*self.grid_width)], self.grid_width)
                self.print_fps(time.time()-T)
            self.quit()            
        except Exception as e:
            self.quit()  
            raise e          
            
    def quit(self):
        print('\n --> GUI quitting.')
        pygame.quit()


class Menu_GUI:
    def __init__(self, start_simulation):
        self.__start_simulation = start_simulation # Start func of the controller
        
        self.window = tk.Tk()
        self.window.title('Setup')
        self.window.geometry('230x190')
        
        # Width of the Simulation
        self.label_sim_width = tk.Label(master=self.window,
                                        text='Width of the sim:')
        self.label_sim_width.place(x=20, y=20, width=120, height=30)
        self.entry_sim_width = tk.Entry(master=self.window)
        self.entry_sim_width.insert(tk.END, '160')
        self.entry_sim_width.place(x=160, y=20, width=50, height=30)
        self.entry_sim_width.bind('<FocusOut>', self.check_valid)
        
        # Height for the simulation
        self.label_sim_height = tk.Label(master=self.window,
                                        text='Height of the sim:')
        self.label_sim_height.place(x=20, y=60, width=120, height=30)
        self.entry_sim_height = tk.Entry(master=self.window)
        self.entry_sim_height.insert(tk.END, '90')
        self.entry_sim_height.place(x=160, y=60, width=50, height=30)
        self.entry_sim_height.bind('<FocusOut>', self.check_valid)
        
        # Ticks per second (tps) for the simulation
        self.label_sim_tps = tk.Label(master=self.window,
                                      text='tps of the sim:')
        self.label_sim_tps.place(x=20, y=100, width=120, height=30)
        self.entry_sim_tps = tk.Entry(master=self.window)
        self.entry_sim_tps.insert(tk.END, '30')
        self.entry_sim_tps.place(x=160, y=100, width=50, height=30)
        self.entry_sim_tps.bind('<FocusOut>', self.check_valid)
        
        # Start button
        self.button_start_sim = tk.Button(master=self.window,
                                          text='Start',
                                          command=self.start_simulation_call,
                                          activebackground=Colour.rgb_to_hex(Colour.GREEN),
                                          fg=Colour.rgb_to_hex(Colour.BLACK),
                                          font='Aral, 20')
        self.button_start_sim.place(x=50, y=140, width=130, height=30)
        
        # Key bindings
        self.window.bind('<Return>', self.start_simulation_call)
        self.window.bind('<Escape>', lambda event: self.window.destroy())
        self.entry_sim_height.bind('<Any-Enter>', self.easy_focus)
        self.entry_sim_width.bind('<Any-Enter>', self.easy_focus)
        self.entry_sim_tps.bind('<Any-Enter>', self.easy_focus)
        self.button_start_sim.bind('<Any-Enter>', self.easy_focus)
        
        # Setup
        self.check_valid()
        
    def easy_focus(self, event):
        event.widget.focus()
        
    def start_simulation_call(self, event=None):
        if self.check_valid():
            self.__start_simulation(int(self.entry_sim_width.get()),
                                    int(self.entry_sim_height.get()),
                                    int(self.entry_sim_tps.get()))
        
    def check_valid(self, event=None) -> bool:
        something_false = False
        #Sim width:
        user_input: str = self.entry_sim_width.get()
        if user_input.isnumeric() and int(user_input) > 1:
            self.entry_sim_width.configure(bg=Colour.rgb_to_hex(Colour.LIGHTGREEN))
        else:
            self.entry_sim_width.configure(bg=Colour.rgb_to_hex((Colour.LIGHTRED)))
            something_false = True
        #Sim height:
        user_input: str = self.entry_sim_height.get()
        if user_input.isnumeric() and int(user_input) > 1:
            self.entry_sim_height.configure(bg=Colour.rgb_to_hex(Colour.LIGHTGREEN))
        else:
            self.entry_sim_height.configure(bg=Colour.rgb_to_hex(Colour.LIGHTRED))
            something_false = True
        # TPS check
        user_input: str = self.entry_sim_tps.get()
        if user_input.isnumeric() and int(user_input) > 1:
            self.entry_sim_tps.configure(bg=Colour.rgb_to_hex(Colour.LIGHTGREEN))
        else:
            self.entry_sim_tps.configure(bg=Colour.rgb_to_hex(Colour.LIGHTRED))
            something_false = True
        
        if something_false:
            self.button_start_sim.config(bg=Colour.rgb_to_hex(Colour.LIGHTRED), state='disabled')
        else:
            self.button_start_sim.config(bg=Colour.rgb_to_hex(Colour.LIGHTGREEN), state='normal')
        
        return not something_false
        
    def start(self):
        self.window.mainloop()
        
