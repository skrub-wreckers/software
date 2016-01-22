import threading
import time
import numpy as np
import pygame

from ..vision import Colors

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

        self.name = "Mapper"

        self.path_surface = pygame.surface.Surface((self.size, self.size), pygame.SRCALPHA)
        self.path_surface.fill([0,0,0,0])
        self.last_pos = None

        self.cubes = []

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

    def update(self, events):
        pass

    def draw(self, surface):
        surface.fill([255,255,255])

        for lpos in range(-int(self.size/self.ppi/12), int(self.size/self.ppi/12)+1, 1):
            pygame.draw.line(surface,
                (255,0,0),
                ((lpos*12*self.ppi)+(self.size/2.0),0),
                ((lpos*12*self.ppi)+(self.size/2.0),self.size),
                1
            )
            pygame.draw.line(surface,
                (255,0,0),
                (0,(lpos*12*self.ppi)+(self.size/2.0)),
                (self.size,(lpos*12*self.ppi)+(self.size/2.0)),
                1
            )

        for cube in self.cubes:
            pos = self.robot_matrix.dot(cube.pos)
            pygame.draw.rect(surface,
                Colors.to_rgb(cube.color),
                pygame.rect.Rect(
                    ((cube.pos[0]*self.ppi)+(self.size/2.0), (cube.pos[1]*self.ppi)+(self.size/2.0)),
                    (2*self.ppi,2*self.ppi)
                ),
                0
            )

        data = self.odometer.val

        pos = np.array([data.x, -data.y])
        dir = np.array([np.cos(data.theta), -np.sin(data.theta)])

        draw_pos = (self.ppi * pos + self.size/2)

        surface.blit(self.path_surface, [0,0])

        pygame.draw.aaline(surface, (0,0,0), to_cv(draw_pos), to_cv(draw_pos + self.ppi * 10*dir))
        pygame.draw.circle(surface, (0,0,0), to_cv(draw_pos), to_cv(self.ppi * 8), 1)

        if self.last_pos is not None:
            if (self.last_pos != draw_pos).any():
                pygame.draw.line(self.path_surface, (100,100,100), self.last_pos, draw_pos, 2)
        self.last_pos = draw_pos


