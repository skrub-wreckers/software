import threading
import time
import numpy as np
import pygame

from ..vision import Colors
from ..gui import Context

def to_cv(val):
    """ np array to integer tuple """
    try:
        l = len(val)
    except Exception:
        return int(val)
    else:
        return tuple(val.astype(int))

class Mapper(object):
    def __init__(self, odometer=None, size=500, ppi=2, map=None):
        self.odometer = odometer
        self.ppi = ppi
        self.size = size

        self.name = "Mapper"

        self.path_surface = pygame.surface.Surface((self.size, self.size), pygame.SRCALPHA)
        self.path_surface.fill([0,0,0,0])
        self.last_pos = None

        self.map = map
        self.cubes = []

    def set_size(self, size):
        self.size = size
        
    def setCubePositions(self, cubes):
        self.cubes = cubes

    @property
    def robot_matrix(self):
        if self.odometer is not None:
            data = self.odometer.val

            return np.array([
                [ np.cos(data.theta), np.sin(data.theta), 0, data.x],
                [-np.sin(data.theta), np.cos(data.theta), 0, data.y],
                [                  0,                  0, 1,      0],
                [                  0,                  0, 0,      1]
            ])

        else:
            return np.array([[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]])

    def update(self, events):
        pass

    def draw(self, surface):
        ctx = Context(surface)
        ctx.translate(250, 250)
        ctx.scale(self.ppi, self.ppi)

        # inches
        ctx.translate(-5*24, -5*24)

        surface.fill([255,255,255])

        bounds = np.array([[0,0,1], [self.size,self.size,1]]).T
        bounds = np.linalg.inv(ctx.matrix).dot(bounds)
        xmin, xmax = sorted(bounds[0,:])
        ymin, ymax = sorted(bounds[1,:])

        # grid size
        d = 12
        for lpos in np.arange(np.floor(xmin/d), np.ceil(xmax/d)):
            ctx.line(
                (128, 0, 0) if lpos % 4 == 0 else (255, 0, 0),
                (lpos * d, ymin),
                (lpos * d, ymax),
                1
            )

        for lpos in np.arange(np.floor(ymin/d), np.ceil(ymax/d)):
            ctx.line(
                (128, 0, 0) if lpos % 4 == 0 else (255, 0, 0),
                (xmin, lpos * d),
                (xmax, lpos * d),
                1
            )


        for cube in self.cubes:
            pos = self.robot_matrix.dot(cube.pos)
            ctx.rect(
                Colors.to_rgb(cube.color),
                pygame.rect.Rect(
                    cube.pos[:2] - [1, 1],
                    cube.pos[:2] + [1, 1]
                ),
                0
            )

        if self.odometer is not None:
            data = self.odometer.val

            surface.blit(self.path_surface, [0,0])

            ctx.save()
            ctx.translate(data.pos[0], data.pos[1])
            ctx.rotate(data.theta)

            ctx.line((0,0,0), [0, 0], 10*data.dir)
            ctx.circle((0,0,0), [0, 0], 8, 1)
            ctx.restore()

            if self.last_pos is not None:
                if (self.last_pos != data.pos).any():
                    ctx.apply_to(self.path_surface).line(
                        (100,100,100),
                        data.pos,
                        draw_pos,
                        2
                    )
            self.last_pos = data.pos

        if self.map is not None:
            for wall in self.map.walls:
                ctx.line(
                    (0,0,255),
                    (wall.x1 * 24, wall.y1 * 24),
                    (wall.x2 * 24, wall.y2 * 24),
                    2
                )

                ctx._apply((wall.x1 * 24, wall.y1 * 24))

            for stack in self.map.stacks:
                pass