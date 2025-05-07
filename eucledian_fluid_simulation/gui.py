import random
import tkinter as tk
import time

import pygame

from objects import *

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
    def __init__(self, grid_width: int, grid_height: int, get_visualize_data, objects, action, fps):
        self.get_visualize_data = get_visualize_data
        self.objects = objects
        self.action = action
        self.print_fps = fps
        
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.size_per_square = 1200//self.grid_width
        
        self.width = grid_width*self.size_per_square + 40
        self.height = grid_height*self.size_per_square + 40
        self.window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Euclidean Fluid Simulation')
        
        self.render_surface = pygame.Surface((self.width, self.height))
        
    def draw_dir(self, direction_list: list, width:int):
        width = width + 2
        l = []
        for i in direction_list:
            for ii in i:
                l.append(ii)       

        for index, vector in enumerate(l):
            if not -0.1 < vector.x < 0.1 or not -0.1 < vector.y < 0.1:
                from_x = float(index%width *self.size_per_square + 20)
                from_y = float(index//width *self.size_per_square + 20)
                to_x = float(from_x + vector.x)
                to_y = float(from_y + vector.y)
                pygame.draw.line(self.render_surface, Colour.WHITE, (from_x, from_y), (to_x, to_y))
        
    def draw_objects(self):
        for obj in self.objects:
            if obj.of_type == 'Circle':
                pygame.draw.circle(self.render_surface,
                                   Colour.LIGHTRED,
                                   (obj.x*self.size_per_square + 20, obj.y*self.size_per_square + 20),
                                   obj.radian*self.size_per_square)
            if obj.of_type == 'Rectangle':
                pygame.draw.rect(self.render_surface,
                                 Colour.GREEN,
                                 (obj.x * self.size_per_square + 20,
                                  obj.y * self.size_per_square + 20,
                                  obj.width * self.size_per_square,
                                  obj.height * self.size_per_square))
        
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
                self.draw_objects()
                
                self.window.blit(self.render_surface, (0,0))
                pygame.display.flip()
                self.render_surface = pygame.Surface((self.width, self.height))
                
                self.print_fps(time.time()-T)
            self.quit()            
        except Exception as e:
            self.quit()  
            raise e          
            
    def quit(self):
        print('\n --> GUI quitting.')
        pygame.quit()


class Menu_GUI:
    def __init__(self, start_simulation, add_object):
        self.__start_simulation = start_simulation # Start func of the controller
        self.__add_object = add_object
        
        self.window = tk.Tk()
        self.window.title('Setup')
        self.window.geometry('230x230')
        
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
        self.button_start_sim.place(x=20, y=140, width=190, height=30)
        
        # Obstacles setup
        self.button_new_obstacle = tk.Button(master=self.window,
                                             text='New Obstacle',
                                             command=self.new_obstacle_window,
                                             activebackground=Colour.rgb_to_hex(Colour.GREEN),
                                             fg=Colour.rgb_to_hex(Colour.BLACK),
                                             font='Aral, 20')
        self.button_new_obstacle.place(x=20, y=180, width=190, height=30)
        
        # Key bindings
        self.window.bind('<Return>', self.start_simulation_call)
        self.window.bind('<Escape>', lambda event: self.window.destroy())
        self.window.bind('<n>', self.new_obstacle_window)
        self.entry_sim_height.bind('<Any-Enter>', self.easy_focus)
        self.entry_sim_width.bind('<Any-Enter>', self.easy_focus)
        self.entry_sim_tps.bind('<Any-Enter>', self.easy_focus)
        self.button_start_sim.bind('<Any-Enter>', self.easy_focus)
        
        # Setup
        self.check_valid()
        
    def new_obstacle_window(self, *event):
        
        def create_options():
            if new_object.get() == 'Circle':
                e_radian.place(x=130, y=180, width=30, height=30)
                l_radian.place(x=20, y=180, width=80, height=30)
                e_height.place_forget()
                e_width.place_forget()
                l_height.place_forget()
                l_width.place_forget()
                b_create_obj.place_forget()
                b_create_obj.place(x=20, y=220, width=140, height=30)
                obj_window.geometry('180x270')
            elif new_object.get() == 'Rectangle':
                e_height.place(x=130, y=180, width=30, height=30)
                e_width.place(x=130, y=220, width=30, height=30)
                l_height.place(x=20, y=180, width=80, height=30)
                l_width.place(x=20, y=220, width=80, height=30)
                e_radian.place_forget()
                l_radian.place_forget()
                b_create_obj.place_forget()
                b_create_obj.place(x=20, y=260, width=140, height=30)
                obj_window.geometry('180x310')
                
            validity()
                
                
                
            e_x.place(x=130, y=100, width=30, height=30)
            e_y.place(x=130, y=140, width=30, height=30)
            l_x.place(x=20, y=100, width=80, height=30)
            l_y.place(x=20, y=140, width=80, height=30)
            
        def validity(*event):
            
            all_good = True
            
            x = e_x.get()
            if not x.isdecimal():
                    l_x.config(bg=Colour.rgb_to_hex(Colour.LIGHTRED))
                    all_good = False
            else:
                l_x.config(bg=Colour.rgb_to_hex(Colour.LIGHTGREY))
                
            y = e_y.get()
            if not y.isdecimal():
                    l_y.config(bg=Colour.rgb_to_hex(Colour.LIGHTRED))
                    all_good = False
            else:
                l_y.config(bg=Colour.rgb_to_hex(Colour.LIGHTGREY))
                
            if new_object.get() == 'Circle':
                radian = e_radian.get()
                if not radian.isdecimal():
                    l_radian.config(bg=Colour.rgb_to_hex(Colour.LIGHTRED))
                    all_good = False
                else:
                    l_radian.config(bg=Colour.rgb_to_hex(Colour.LIGHTGREY))
                    
            elif new_object.get() == 'Rectangle':
                height = e_height.get()
                if not height.isdecimal():
                    l_height.config(bg=Colour.rgb_to_hex(Colour.LIGHTRED))
                    all_good = False
                else:
                    l_height.config(bg=Colour.rgb_to_hex(Colour.LIGHTGREY))
                    
                width = e_width.get()
                if not width.isdecimal():
                    l_width.config(bg=Colour.rgb_to_hex(Colour.LIGHTRED))
                    all_good = False
                else:
                    l_width.config(bg=Colour.rgb_to_hex(Colour.LIGHTGREY))
                    
            
            if all_good:
                b_create_obj.config(state='normal', background=Colour.rgb_to_hex(Colour.LIGHTGREEN))
            else:
                b_create_obj.config(state='disabled', background=Colour.rgb_to_hex(Colour.LIGHTRED))
                      
        def create_new_object(*event):
            if new_object.get() == 'Circle':
                self.__add_object(Circle(x=int(e_x.get()),
                                         y=int(e_y.get()),
                                         radian=int(e_radian.get())))
                print(f'Added Circle @ (x={e_x.get()}| y={e_y.get()}), radian={e_radian.get()}')
                
            elif new_object.get() == 'Rectangle':
                self.__add_object(Rectangle(x=int(e_x.get()),
                                            y=int(e_y.get()),
                                            width=int(e_width.get()),
                                            height=int(e_height.get())))      
                print(f'Added Rectangle @ (x={e_x.get()}| y={e_y.get()}), height={e_height.get()}, width={e_width.get()}')
                
            obj_window.destroy()
                         
                
        
        obj_window = tk.Toplevel(self.window)
        obj_window.title('Create object')
        obj_window.geometry('180x150')
        
        new_object = tk.StringVar(value='None')
        
        l_circle = tk.Label(master=obj_window, text='Circle:', background=Colour.rgb_to_hex(Colour.LIGHTGREY))
        l_rect = tk.Label(master=obj_window, text='Rectangle:', background=Colour.rgb_to_hex(Colour.LIGHTGREY))
        rb_circle = tk.Radiobutton(obj_window, variable=new_object, value='Circle', background=Colour.rgb_to_hex(Colour.LIGHTGREY), command=create_options)
        rb_rect = tk.Radiobutton(obj_window, variable=new_object, value='Rectangle', background=Colour.rgb_to_hex(Colour.LIGHTGREY), command=create_options)
        
        e_x = tk.Entry(master=obj_window)
        e_x.bind('<Any-Enter>', validity)
        l_x = tk.Label(master=obj_window, text='X-Position', background=Colour.rgb_to_hex(Colour.LIGHTGREY))
        e_y = tk.Entry(master=obj_window)
        e_y.bind('<Any-Enter>', validity)
        l_y = tk.Label(master=obj_window, text='Y-Position', background=Colour.rgb_to_hex(Colour.LIGHTGREY))
        e_radian = tk.Entry(master=obj_window)
        e_radian.bind('<Any-Enter>', validity)
        l_radian = tk.Label(master=obj_window, text='Radian', background=Colour.rgb_to_hex(Colour.LIGHTGREY))
        e_height = tk.Entry(master=obj_window)
        e_height.bind('<Any-Enter>', validity)
        l_height = tk.Label(master=obj_window, text='Height', background=Colour.rgb_to_hex(Colour.LIGHTGREY))
        e_width = tk.Entry(master=obj_window)
        e_width.bind('<Any-Enter>', validity)
        l_width = tk.Label(master=obj_window, text='Width', background=Colour.rgb_to_hex(Colour.LIGHTGREY))
        
        b_create_obj =tk.Button(master=obj_window, command=create_new_object, background=Colour.rgb_to_hex(Colour.LIGHTRED), text='Add new object', state='disabled')
        
        l_circle.place(x=20, y=20, width=80, height = 30)
        l_rect.place(x=20, y=60, width=80, height = 30)
        rb_circle.place(x=130, y=20, width=30, height=30)
        rb_rect.place(x=130, y=60, width=30, height=30)
        b_create_obj.place(x=20, y=100, width=140, height=30)
        
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
        
    def start(self): self.window.mainloop()
        
    def close(self): self.window.destroy()
    
