from gui import Menu_GUI

class Controller:
    """
        Main Control unit
    """
    def __init__(self):
        self.gui = Menu_GUI()
        
    def start(self):
        self.gui.start()