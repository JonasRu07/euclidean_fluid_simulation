import time
import copy

import numpy as np

from vector import Vector2


class Fluid:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        
        self.u_grid = [[0 for _ in range(self.width)] for __ in range(self.height+1)]
        self.v_grid = [[0 for _ in range(self.width+1)] for __ in range(self.height)]
        
        self.directional_grid = [[Vector2(0, 0) for _ in range(self.width)] for __ in range(self.height)]
                     
    def solve_incompressible_2D_array(self):
        print(self.u_grid)
        print(self.v_grid)
        aux_u_gird = copy.deepcopy(self.u_grid)
        aux_v_gird = copy.deepcopy(self.v_grid)
        for i in range(self.height):
            for j in range(self.width):
                # print(i, j)
                # print(f'u(i, j): {i}:{j}')
                # print(f'u(i+1, j): {i+1}:{j}')
                # print(f'v(i, j): {i}:{j}')
                # print(f'v(i, j+1): {i}:{j+1}')
                divergence = \
                    + self.u_grid[i][j] \
                    - self.u_grid[i+1][j] \
                    + self.v_grid[i][j] \
                    - self.v_grid[i][j+1]
                aux_u_gird[i][j] -= divergence/4
                aux_u_gird[i+1][j] += divergence/4
                aux_v_gird[i][j] -= divergence/4
                aux_v_gird[i][j+1] += divergence/4
                x = self.v_grid[i][j] + self.v_grid[i][j+1]
                y = self.u_grid[i][j] + self.u_grid[i+1][j]
                self.directional_grid[i][j] = Vector2(x=self.v_grid[i][j] + self.v_grid[i][j+1],
                                                      y=self.u_grid[i][j] + self.u_grid[i+1][j])
                
                self.u_grid = aux_u_gird
                self.v_grid = aux_v_gird
