import threading
import time
import vision
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
    def __init__(self, odometer, size=500, ppi=5):
        self.odometer = odometer
        self.ppi = ppi
        self.size = size

        self.screen = None

        self.cubes = []
        
        t = threading.Thread(target=self._run)
        t.daemon = True
        t.start()
        
    def setCubePositions(self, cubes):
        self.cubes = cubes
        
    @property
    def robot_matrix(self):
        data = self.odometer.val


        return np.array([
            [ np.cos(data.theta), np.sin(data.theta), 0, data.x],
            [-np.sin(data.theta), np.cos(data.theta), 0, data.y],
            [                  0,                  0, 1,      0],
            [                  0,                  0, 0,      1]
        ])


    def redraw(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pass

        self.screen.fill([255,255,255])

        for lpos in range(-(self.size/self.ppi/12), (self.size/self.ppi/12), 1):
            pygame.draw.line(self.screen, (255,0,0), ((lpos*12*self.ppi)+(self.size/2.0),0), ((lpos*12*self.ppi)+(self.size/2.0),self.size), 1)
            pygame.draw.line(self.screen, (255,0,0), (0,(lpos*12*self.ppi)+(self.size/2.0)), (self.size,(lpos*12*self.ppi)+(self.size/2.0)), 1)

        for cube in self.cubes:
            pos = self.robot_matrix.dot(cube.pos)
            print pos
            print cube.pos
            pygame.draw.rect(self.screen, vision.Colors.to_rgb(cube.color), pygame.rect.Rect(((pos[0]*self.ppi)+(self.size/2.0), 
                                                                                                (-pos[1]*self.ppi)+(self.size/2.0)),
                                                                                                   (2*self.ppi,2*self.ppi)), 0)

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

