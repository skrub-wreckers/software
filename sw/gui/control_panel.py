from .window import Window

class ControlPanel(object):
    def __init__(self, robot, size = 500):
        self.robot = robot
        self.size = size
        self.name = "Control Panel"
        
    def set_size(self, size):
        self.size = size
        
    def draw(self, surface):
        surface.fill((255,255,0))
        
    def update(self, events):
        pass