import time
import copy

import numpy as np

from vector import Vector2
from objects import Rectangle, Circle


class Fluid:
    def __init__(self, width: int, height: int, tps:int, objects:list):
        
        self.delta_time = 1/tps
        
        self.width = width + 2
        self.height = height + 2
        
        self.u_grid = [[0 for _ in range(self.width)] for __ in range(self.height+1)]
        self.v_grid = [[0 for _ in range(self.width+1)] for __ in range(self.height)]
        
        self.scalars = np.ndarray((self.height+1, self.width+1))
        self.scalars.fill(1)
        
        
        self.directional_grid = [[Vector2(0, 0) for _ in range(self.width)] for __ in range(self.height)]
        
        self.objects:list = objects
        
        self.reset_wind_channel(0, self.height, 25)
        
        # Scaler setup
        for i in range(self.width+1):
            self.scalars[0][i] = 0
            self.scalars[self.height][i] = 0
            
        for i in range(self.height+1): 
            self.scalars[i][0] = 0
            
        self.apply_object_interaction()
        
    def solve_incompressible_2D_array(self):
        aux_u_grid = copy.deepcopy(self.u_grid)
        aux_v_grid = copy.deepcopy(self.v_grid)
        for i in range(self.height):
            for j in range(self.width):
                
                #Scalers
                scaler_x_0 = self.scalars[i-1][j]
                scaler_x_1 = self.scalars[i+1][j]
                scaler_y_0 = self.scalars[i][j-1]
                scaler_y_1 = self.scalars[i][j+1]
                
                scaler = scaler_x_0 + scaler_x_1 + scaler_y_0 + scaler_y_1
                
                if scaler == 0: continue
                
                divergence = \
                            + self.u_grid[i][j] \
                            - self.u_grid[i+1][j] \
                            + self.v_grid[i][j] \
                            - self.v_grid[i][j+1]
                            
                pressure = divergence / scaler
                
                aux_u_grid[i][j] -= pressure * scaler_x_0
                aux_u_grid[i+1][j] += pressure * scaler_x_1
                aux_v_grid[i][j] -= pressure * scaler_y_0
                aux_v_grid[i][j+1] += pressure * scaler_y_1
                
                self.directional_grid[i][j] = Vector2(x=self.v_grid[i][j] + self.v_grid[i][j+1],
                                                      y=self.u_grid[i][j] + self.u_grid[i+1][j])
                
        self.u_grid = aux_u_grid
        self.v_grid = aux_v_grid
                     
    def advect_velocity_simple(self):
        
        new_u = copy.deepcopy(self.u_grid)
        new_v = copy.deepcopy(self.v_grid)

        # Up Down
        for j in range(1, self.height):
            for i in range(1, self.width - 1):

                u_val = self.u_grid[j][i]
                v_val = (self.v_grid[j-1][i] + self.v_grid[j][i]) * 0.5

                i_from = i - int(np.sign(u_val))
                j_from = j - int(np.sign(v_val))
                i_from = max(0, min(self.width - 2, i_from))
                j_from = max(0, min(self.height - 1, j_from))

                new_u[j][i] = self.u_grid[j_from][i_from]
                
        # Left right
        for j in range(1, self.height - 1):
            for i in range(1, self.width):
                u_val = (self.u_grid[j][i-1] + self.u_grid[j][i]) * 0.5
                v_val = self.v_grid[j][i]

                i_from = i - int(np.sign(u_val))
                j_from = j - int(np.sign(v_val))
                
                i_from = max(0, min(self.width - 1, i_from))
                j_from = max(0, min(self.height - 2, j_from))

                new_v[j][i] = self.v_grid[j_from][i_from]

        self.u_grid = new_u
        self.v_grid = new_v
            
    def apply_object_interaction(self):
        for obj in self.objects:
            for i in range(self.width+1):
                for j in range(self.height+1):
                    if obj.occupies(i, j):
                        self.scalars[i][j] = 0        
                    
    def reset_wind_channel(self, height:int, size:int, power:float):
        for i in range(self.height-height-size, self.height-height):
            self.v_grid[i][0] = power
                
    def get_flow_dir(self): return self.directional_grid
    
    def get_objects(self): return self.objects
