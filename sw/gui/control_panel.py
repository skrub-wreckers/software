from .window import Window
from ..hal import ColorSensor, BreakBeams, DigitalIR, LimitSwitch
from ..vision import Colors
from .. import util
from tamproxy.devices import LongIR, DigitalInput
import pygame
import numpy as np
import os
import pygame
import time

PANEL_BG = (150, 150, 150)

START_COLORS = {True:[200,0,0], False:[0,200,0]}
START_RECT = (330,100,160,160)

class ControlPanel(object):
    def __init__(self, robot, size = 500):
        self.robot = robot
        self.size = size
        self.name = "Control"
        pygame.font.init()
        self.font = pygame.font.Font(None, 60)
        self.end_time = None

        self.color_data = {}
        for c in [Colors.RED, Colors.GREEN, Colors.NONE]:
            path = os.path.join(os.path.dirname(__file__), '../../tests/color-sensor', Colors.name(c) + '.npy')
            raw = np.load(path).reshape((-1, 4))

            self.color_data[c] = ColorSensor.project(raw)

        self.started = False

    def set_size(self, size):
        self.size = size

    def draw(self, surface):
        surface.fill((50,50,50))
        pygame.draw.rect(surface, START_COLORS[self.started], START_RECT)
        if self.end_time is not None:
            t_surf = self.font.render(str(int(self.end_time - time.time())), True, (0,0,0))
            surface.blit(t_surf, (int(START_RECT[0]+(START_RECT[2]/2.0)-(t_surf.get_width()/2.0)),int(START_RECT[1]+(START_RECT[3]/2.0)-(t_surf.get_height()/2.0))))

        self.draw_ir(surface)
        self.draw_colorsensor(surface)
        self.draw_breakbeams(surface)

    def draw_ir(self, surface):
        pygame.draw.rect(surface, PANEL_BG, (250,10,150,80))
        for id, sensor in enumerate((self.robot.left_long_ir, self.robot.right_long_ir, self.robot.left_short_ir, self.robot.right_short_ir, self.robot.left_bumper, self.robot.right_bumper)):
            if type(sensor) is LongIR:
                d = sensor.distInches
                if not np.isfinite(d):
                    d = 24
                pygame.draw.rect(surface, (255,255,255), (325, 15+12*id, int((d/24.0)*50), 10))
                for tick in range(0, 4):
                    pygame.draw.line(surface, (255,0,0), (325+(int(((tick+1)*0.25)*50)), 20+12*id), (325+(int(((tick+1)*0.25)*50)), 25+12*id))
                #surface.blit(self.font.render(str(sensor.distInches)[:5], True, (255,255,255)), [325, 15+15*id])
            elif type(sensor) is DigitalIR:
                pygame.draw.rect(surface, (255,255,255), (325, 15+12*id, int(sensor.val*50), 12))
            elif type(sensor) is LimitSwitch:
                pygame.draw.rect(surface, (0,0,0), (325, 15+12*id, int(sensor.val*50), 12))

    def draw_colorsensor(self, surface):
        pygame.draw.rect(surface, PANEL_BG, (410, 10, 80, 80))
        pygame.draw.rect(surface, Colors.to_rgb(self.robot.color_sensor.val), (415,15,70,70))

        center = [60, 170]
        scale = 100
        pygame.draw.rect(surface, PANEL_BG, (10, 100, 310, 160))

        for c, points in self.color_data.items():
            c = Colors.to_rgb(c)
            for pos in points:
                pos = (pos*scale + center).astype(np.int)
                pygame.draw.circle(surface, c, pos, 3)

        curr = self.robot.color_sensor.raw_val
        pos = ColorSensor.project(curr)
        pos = (pos*scale + center).astype(np.int)
        pygame.draw.circle(surface, (255, 255, 255), pos, 3)

    def draw_breakbeams(self, surface):
        pygame.draw.rect(surface, PANEL_BG, (10,10,230,80))
        if self.robot.break_beams.l_beam.broken:
            pygame.draw.rect(surface, (255,255,255), (15,15,105,50))
        #pygame.draw.rect(surface, (255,255,255), (15,70,int(105*(self.robot.break_beams.l_beam._recv_pin.val/65536.0)),10))
        #pygame.draw.line(surface, (255,0,0), (15+int(105*(self.robot.break_beams.l_beam._thres/65536.0)), 75), (15+int(105*(self.robot.break_beams.l_beam._thres/65536.0)),80))
        if self.robot.break_beams.r_beam.broken:
            pygame.draw.rect(surface, (255,255,255), (130,15,105,50))
        #pygame.draw.rect(surface, (255,255,255), (130,70,int(105*(self.robot.break_beams.r_beam._recv_pin.val/65536.0)),10))
        #pygame.draw.line(surface, (255,0,0), (130+int(105*(self.robot.break_beams.r_beam._thres/65536.0)), 75), (130+int(105*(self.robot.break_beams.r_beam._thres/65536.0)),80))

    def update(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if util.point_in(event.pos, START_RECT):
                    print "Start button pressed"
                    self.started = not self.started
                    self.end_time = time.time()+constants.round_time