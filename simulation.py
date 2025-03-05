import sys

from fluid import *
from gui import SimulationGUI

class Simulation:
    
    def __init__(self, width:int= 160, height:int=90, tps=30):

        self._gui: SimulationGUI = SimulationGUI(width, height, None)
        self._fluid = Fluid(width, height)
        self.tps = tps
        
        
    def mainloop(self):
        while self._gui.frame():
            self._fluid.solve_incompressible_2D_array()
            self._gui.draw_dir(self.fluid.flow_directions)
            
        
            
    def __show_fps(self, delta_time:float):
        sys.stdout.write(f'\rRender time: {round(delta_time* 1000, 2)}ms {round(1/delta_time, 3)} TPS')
        sys.stdout.flush()
    