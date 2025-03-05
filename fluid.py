import time
import copy

import numpy as np

from vector import Vector2
from objects import Rectangle, Circle


class Fluid:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        
        self._u_grid = [[0 for _ in range(self.width)] for __ in range(self.height+1)]
        self._v_grid = [[0 for _ in range(self.width+1)] for __ in range(self.height)]
        
        self.directional_grid = [[Vector2(0, 0) for _ in range(self.width)] for __ in range(self.height)]
        
        self.objects:list = [Circle(30, 45, 25)]
                     
    def solve_incompressible_2D_array(self):
        self.apply_object_interaction()
        aux_u_grid = copy.deepcopy(self.u_grid)
        aux_v_grid = copy.deepcopy(self._v_grid)
        for i in range(self.height):
            for j in range(self.width):
                if self._u_grid[i][j] != 0 or self._v_grid[i][j] != 0:
                    if i == 0:
                        
                        divergence = \
                            + self.u_grid[i][j] \
                            - self.u_grid[i+1][j] \
                            + self._v_grid[i][j] \
                            - self._v_grid[i][j+1]
                        aux_u_grid[i][j] -= self.u_grid[i][j]
                        aux_u_grid[i+1][j] += divergence/3
                        aux_v_grid[i][j] -= divergence/3
                        aux_v_grid[i][j+1] += divergence/3
                        x = self._v_grid[i][j] + self._v_grid[i][j+1]
                        y = self.u_grid[i][j] + self.u_grid[i+1][j]
                        self.directional_grid[i][j] = Vector2(x=self._v_grid[i][j] + self._v_grid[i][j+1],
                                                            y=self.u_grid[i][j] + self.u_grid[i+1][j])
                    
                    elif i == self.height-1:
                        divergence = \
                            + self.u_grid[i][j] \
                            - self.u_grid[i+1][j] \
                            + self._v_grid[i][j] \
                            - self._v_grid[i][j+1]
                        aux_u_grid[i][j] -= divergence/3
                        aux_u_grid[i+1][j] = self.u_grid[i+1][j]
                        aux_v_grid[i][j] -= divergence/3
                        aux_v_grid[i][j+1] += divergence/3
                        x = self._v_grid[i][j] + self._v_grid[i][j+1]
                        y = self.u_grid[i][j] + self.u_grid[i+1][j]
                        self.directional_grid[i][j] = Vector2(x=self._v_grid[i][j] + self._v_grid[i][j+1],
                                                            y=self.u_grid[i][j] + self.u_grid[i+1][j])
                    else:
                        divergence = \
                            + self.u_grid[i][j] \
                            - self.u_grid[i+1][j] \
                            + self._v_grid[i][j] \
                            - self._v_grid[i][j+1]
                        aux_u_grid[i][j] -= divergence/4
                        aux_u_grid[i+1][j] += divergence/4
                        aux_v_grid[i][j] -= divergence/4
                        aux_v_grid[i][j+1] += divergence/4
                        x = self._v_grid[i][j] + self._v_grid[i][j+1]
                        y = self.u_grid[i][j] + self.u_grid[i+1][j]
                        self.directional_grid[i][j] = Vector2(x=self._v_grid[i][j] + self._v_grid[i][j+1],
                                                            y=self.u_grid[i][j] + self.u_grid[i+1][j])
                
                self._u_grid = aux_u_grid
                self._v_grid = aux_v_grid
        self.reset_wind_channel(0, self.height, 25)
        
    def apply_object_interaction(self):
        for obj in self.objects:
            for i in range(self.height):
                for j in range(self.width):
                    if obj.occupies(i, j):
                        self._u_grid[i][j] = 0 
                        if j < self.width:
                            self._v_grid[i][j] = 0
                        self.directional_grid[i][j] = Vector2(0, 0)
    
                    
    def reset_wind_channel(self, height:int, size:int, power:float):
        for i in range(self.height-height-size, self.height-height):
            self._v_grid[i][0] = power
            
                
    def get_flow_dir(self): return self.flow_directions

    @property
    def u_grid(self):
        return self._u_grid
    
    @property
    def v_grid(self):
        return self._v_grid
    
    @property
    def flow_directions(self):
        return self.directional_grid
    
    @property
    def fluid_width(self):
        return self.width
    
    @property
    def fluid_height(self):
        return self.height