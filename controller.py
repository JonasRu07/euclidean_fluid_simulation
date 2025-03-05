from gui import Menu_GUI
from simulation import Simulation

class Controller:
    """
        Main Control unit
    """
    def __init__(self):
        self.gui = Menu_GUI(self.start_simulation)
        self.new_sim_width: int = -1        
        self.new_sim_height: int = -1
        self.new_sim_tps: int = -1
        self.valid_config: bool = False
        self.simulation = None
        
    def start_simulation(self, width=40, height=30, tps=30):
        self.set_sim_values(width, height, tps)
        if self.valid_config:
            self.simulation = Simulation(self.new_sim_width,
                                         self.new_sim_height,
                                         self.new_sim_tps)
        
    def set_sim_values(self, width=40, height=30, tps=30):
        self.valid_config = True
        if isinstance(width, int) and width > 0:
            self.new_sim_width = width
        else: 
            self.valid_config = False
        if isinstance(height, int) and height > 0:
            self.new_sim_height = height
        else: 
            self.valid_config = False
        if isinstance(tps, int) and tps > 0:
            self.new_sim_tps = tps
        else: 
            self.valid_config = False

        
    def start(self):
        self.gui.start()