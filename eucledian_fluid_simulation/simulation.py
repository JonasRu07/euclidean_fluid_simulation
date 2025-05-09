import sys

from fluid import *
from gui import SimulationGUI

class Simulation:
    
    def __init__(self, width:int= 160, height:int=90, tps=50, objects=[]):

        self.tps = tps
        self.fluid = Fluid(width, height, tps, objects)
        self.gui: SimulationGUI = SimulationGUI(width,
                                                height,
                                                self.fluid.get_flow_dir,
                                                objects,
                                                self.action,
                                                self.__show_fps,
                                                self.tps)
        
    def action(self):
        self.fluid.solve_incompressible_2D_array()
        self.fluid.advect_velocity()
        
        
    def mainloop(self):
        self.gui.loop()

    def __show_fps(self, delta_time:float):
        sys.stdout.write(f'\rRender time: {round(delta_time* 1000, 2)}{'0'*(6-len(str(round(delta_time* 1000, 2))))} ms {round(1/delta_time, 3)} FPS')
        sys.stdout.flush()
    