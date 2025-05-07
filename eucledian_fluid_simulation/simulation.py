import sys

from fluid import *
from gui import SimulationGUI

class Simulation:
    
    def __init__(self, width:int= 160, height:int=90, tps=30):

        self.tps = tps
        self.fluid = Fluid(width, height, tps)
        self.gui: SimulationGUI = SimulationGUI(width,
                                                height,
                                                self.fluid.get_flow_dir,
                                                self.fluid.solve_incompressible_2D_array,
                                                self.__show_fps)
        
        
    def mainloop(self):
        self.gui.loop()

    def __show_fps(self, delta_time:float):
        sys.stdout.write(f'\rRender time: {round(delta_time* 1000, 2)}ms {round(1/delta_time, 3)} FPS')
        sys.stdout.flush()
    