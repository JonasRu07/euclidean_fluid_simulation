import time
import copy

import numpy as np

from vector import Vector2


class Fluid:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        
        self._u_grid = [[0 for _ in range(self.width)] for __ in range(self.height+1)]
        self._v_grid = [[0 for _ in range(self.width+1)] for __ in range(self.height)]
        
        self.directional_grid = [[Vector2(0, 0) for _ in range(self.width)] for __ in range(self.height)]
                     
    def solve_incompressible_2D_array(self):
        aux_u_grid = copy.deepcopy(self.u_grid)
        aux_v_grid = copy.deepcopy(self.__v_grid)
        for i in range(self.height):
            for j in range(self.width):
                # print(i, j)
                # print(f'u(i, j): {i}:{j}')
                # print(f'u(i+1, j): {i+1}:{j}')
                # print(f'v(i, j): {i}:{j}')
                # print(f'v(i, j+1): {i}:{j+1}')
                if i == 0:
                    
                    divergence = \
                        + self.u_grid[i][j] \
                        - self.u_grid[i+1][j] \
                        + self.__v_grid[i][j] \
                        - self.__v_grid[i][j+1]
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
                        + self.__v_grid[i][j] \
                        - self.__v_grid[i][j+1]
                    aux_u_grid[i][j] -= divergence/3
                    aux_u_grid[i+1][j] = self.u_grid[i+1][j]
                    aux_v_grid[i][j] -= divergence/3
                    aux_v_grid[i][j+1] += divergence/3
                    x = self.__v_grid[i][j] + self.__v_grid[i][j+1]
                    y = self.u_grid[i][j] + self.u_grid[i+1][j]
                    self.directional_grid[i][j] = Vector2(x=self.__v_grid[i][j] + self._v_grid[i][j+1],
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
                
                self.u_grid = aux_u_grid
                self._v_grid = aux_v_grid


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