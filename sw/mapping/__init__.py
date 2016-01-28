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

        if map and odometer:
            odometer.override_position(map.start[0]*12, map.start[1]*12, 0)

    def set_size(self, size):
        self.size = size

    def update_cubes_from(self, vision):
        self.cubes = v.cubes
        self.cubes_mat = self.robot_matrix

    @property
    def robot_matrix(self):
        if self.odometer is not None:
            data = self.odometer.val

            return np.array([
                [ np.cos(data.theta), -np.sin(data.theta), 0, data.x],
                [ np.sin(data.theta), np.cos(data.theta), 0, data.y],
                [                  0,                  0, 1,      0],
                [                  0,                  0, 0,      1]
            ])

        else:
            return np.array([[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]])

    def update(self, events):
        pass

    def _draw_robot(self, ctx):
        ctx.line((0,0,0), [0, 0], [10, 0])

        points = [
            (0, 0)
        ]
        n = 20
        r = 8
        for i in range(n+1):
            f = float(i) / n
            theta = np.pi *.25 *f + np.pi * 1.75 * (1-f)
            points.append([r*np.cos(theta), r*np.sin(theta)])

        ctx.polygon([255, 255, 0], points)


    def draw(self, surface):
        ctx = Context(surface)
        ctx.translate(250, 250)
        ctx.scale(self.ppi, -self.ppi)

        # translate the map to be centered, if it exists
        if self.map:
            all_xs = [x for wall in self.map.walls for x in [wall.x1, wall.x2]]
            all_ys = [y for wall in self.map.walls for y in [wall.y1, wall.y2]]

            c_x = (max(all_xs) + min(all_xs)) / 2.0
            c_y = (max(all_ys) + min(all_ys)) / 2.0
            ctx.translate(-c_x*12, -c_y*12)

        surface.fill([0,0,0])

        bounds = np.array([[0,0,1], [self.size,self.size,1]]).T
        bounds = np.linalg.inv(ctx.matrix).dot(bounds)
        xmin, xmax = sorted(bounds[0,:])
        ymin, ymax = sorted(bounds[1,:])

        # grid size
        d = 12
        for lpos in np.arange(np.floor(xmin/d), np.ceil(xmax/d)):
            ctx.line(
                (128, 128, 128) if lpos % 4 == 0 else (64, 64, 64),
                (lpos * d, ymin),
                (lpos * d, ymax),
                1
            )

        for lpos in np.arange(np.floor(ymin/d), np.ceil(ymax/d)):
            ctx.line(
                (128, 128, 128) if lpos % 4 == 0 else (64, 64, 64),
                (xmin, lpos * d),
                (xmax, lpos * d),
                1
            )

        for stack in self.map.stacks:
            for i,cube in enumerate(stack.cubes):
                ctx.circle(Colors.to_rgb(cube)*0.5, (stack.x*12, stack.y*12), (2*(3-i)))

        for cube in self.cubes:
            pos = self.cubes_mat.dot(cube.pos)
            for i, c in list(enumerate(cube.colors)):
                size = np.ones(2) * (3.0 - i)
                ctx.rect(
                    Colors.to_rgb(c),
                    pygame.rect.Rect(
                        pos[:2] - size / 2,
                        size
                    ),
                    0
                )

        if self.odometer is not None:
            data = self.odometer.val
        else:
            from ..hal import Odometer
            data = Odometer.Reading(0, 12*5, 12*5, 0, 0, 0)

        surface.blit(self.path_surface, [0,0])

        ctx.save()
        ctx.translate(data.pos[0], data.pos[1])
        ctx.rotate(data.theta)
        self._draw_robot(ctx)
        ctx.restore()

        if self.last_pos is not None:
            if (self.last_pos != data.pos).any():
                ctx.apply_to(self.path_surface).line(
                    (255,255,0),
                    data.pos,
                    self.last_pos,
                    2
                )
        self.last_pos = data.pos

        if self.map is not None:
            for wall in self.map.walls:
                ctx.line(
                    (0,0,255),
                    (wall.x1 * 12, wall.y1 * 12),
                    (wall.x2 * 12, wall.y2 * 12),
                    2
                )

                ctx._apply((wall.x1 * 12, wall.y1 * 12))
