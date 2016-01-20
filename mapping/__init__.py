import threading
import time

import numpy as np
import pygame

def to_cv(val):
    """ np array to integer tuple """
    try:
        l = len(val)
    except Exception:
        return int(val)
    else:
        return tuple(val.astype(int))

class Mapper(object):
    def __init__(self, odometer, size=500, ppi=10):
        self.odometer = odometer
        self.ppi = ppi
        self.size = size

        self.screen = None

        t = threading.Thread(target=self._run)
        t.daemon = True
        t.start()

    def redraw(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pass

        self.screen.fill([255,255,255])

        for vlinex in range(-4, 4, 1):
            pygame.draw.line(self.screen, (255,0,0), ((vlinex*12*self.ppi)+(self.size/2.0),0), ((vlinex*12*self.ppi)+(self.size/2.0),self.size), 1)
        for hliney in range(-4, 4, 1):
            pygame.draw.line(self.screen, (255,0,0), (0,(hliney*12*self.ppi)+(self.size/2.0)), (self.size,(hliney*12*self.ppi)+(self.size/2.0)), 1)


        data = self.odometer.val

        pos = np.array([data.x, -data.y])
        dir = np.array([np.cos(data.theta), -np.sin(data.theta)])

        draw_pos = (self.ppi * pos + self.size/2)

        pygame.draw.aaline(self.screen, (0,0,0), to_cv(draw_pos), to_cv(draw_pos + self.ppi * 10*dir))
        pygame.draw.circle(self.screen, (0,0,0), to_cv(draw_pos), to_cv(self.ppi * 8), 1)

        pygame.display.flip()

    def _run(self):
        pygame.init()
        self.screen = pygame.display.set_mode([self.size,self.size])
        pygame.display.set_caption("Mapper")
        while True:
            self.odometer.update()
            time.sleep(0.05)
            self.redraw()

