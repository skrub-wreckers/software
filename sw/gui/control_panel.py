from .window import Window
from ..hal import ColorSensor, BreakBeams, DigitalIR
from ..vision import Colors
from tamproxy.devices import LongIR
import pygame
import numpy as np

class ControlPanel(object):
    def __init__(self, robot, size = 500):
        self.robot = robot
        self.size = size
        self.name = "Control"
        pygame.font.init()
        self.font = pygame.font.Font(None, 20)
        
    def set_size(self, size):
        self.size = size
        
    def draw(self, surface):
        surface.fill((50,50,50))
        pygame.draw.rect(surface, (0,200,0), (350,350,100,100))
        #IR Sensors
        pygame.draw.rect(surface, (150,150,150), (250,10,150,80))
        for id, sensor in enumerate((self.robot.left_long_ir, self.robot.right_long_ir, self.robot.left_short_ir, self.robot.right_short_ir, self.robot.back_short_ir)):
            if type(sensor) is LongIR:
                d = sensor.distInches
                if not np.isfinite(d):
                    d = 24
                pygame.draw.rect(surface, (255,255,255), (325, 15+15*id, int((d/24.0)*50), 10))
                for tick in range(0, 4):
                    pygame.draw.line(surface, (255,0,0), (325+(int(((tick+1)*0.25)*50)), 20+15*id), (325+(int(((tick+1)*0.25)*50)), 25+15*id))
                #surface.blit(self.font.render(str(sensor.distInches)[:5], True, (255,255,255)), [325, 15+15*id])
            elif type(sensor) is DigitalIR:
                pygame.draw.rect(surface, (255,255,255), (325, 15+15*id, int(sensor.val*50), 15))
                
        #Color sensor
        pygame.draw.rect(surface, (150,150,150), (410, 10, 80, 80))
        pygame.draw.rect(surface, Colors.to_rgb(self.robot.color_sensor.val), (415,15,70,70))
            
        #Breakbeams
        pygame.draw.rect(surface, (150,150,150), (10,10,230,80))
        if self.robot.break_beams.l_beam.broken:
            pygame.draw.rect(surface, (255,255,255), (15,15,105,50))
        pygame.draw.rect(surface, (255,255,255), (15,70,int(105*(self.robot.break_beams.l_beam._recv_pin.val/65536.0)),10))
        pygame.draw.line(surface, (255,0,0), (15+int(105*(self.robot.break_beams.l_beam._thres/65536.0)), 75), (15+int(105*(self.robot.break_beams.l_beam._thres/65536.0)),80))
        if self.robot.break_beams.r_beam.broken:
            pygame.draw.rect(surface, (255,255,255), (130,15,105,50))
        pygame.draw.rect(surface, (255,255,255), (130,70,int(105*(self.robot.break_beams.r_beam._recv_pin.val/65536.0)),10))
        pygame.draw.line(surface, (255,0,0), (130+int(105*(self.robot.break_beams.r_beam._thres/65536.0)), 75), (130+int(105*(self.robot.break_beams.r_beam._thres/65536.0)),80))
        
    def update(self, events):
        pass