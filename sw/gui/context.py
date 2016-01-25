import numpy as np
import pygame

class Context(object):
    def __init__(self, surface=None):
        self.surf = surface
        self.matrix = np.eye(3)
        self.old_transforms = []

    def apply_to(self, new_surface):
        m = Context(new_surface)
        m.matrix = self.matrix
        return m

    def save(self):
        self.old_transforms.append(self.matrix)

    def restore(self):
        self.matrix = self.old_transforms.pop()

    def transform(self, matrix):
        self.matrix = self.matrix.dot(matrix)

    def rotate(self, theta):
        self.transform(np.array([
            [ np.cos(theta), -np.sin(theta), 0],
            [ np.sin(theta), np.cos(theta), 0],
            [             0,             0, 1],
        ], dtype=np.float32))

    def scale(self, sx, sy=None):
        if sy is None:
            sx = sy
        self.transform(np.array([
            [sx, 0, 0],
            [0, sy, 0],
            [0,  0, 1],
        ], dtype=np.float32))

    def translate(self, x, y):
        self.transform(np.array([
            [1, 0, x],
            [0, 1, y],
            [0, 0, 1],
        ], dtype=np.float32))

    def _apply(self, pt):
        if np.isscalar(pt):
            return int(np.sqrt(np.linalg.norm(self.matrix[:2,:2])) * pt)

        pt = np.asarray(pt)
        if len(pt) == 2:
            pt = np.append(pt, [1])

        res = self.matrix.dot(pt)
        return res[:2].astype(int)

    def circle(self, color, pos, radius, width=0):
        pygame.draw.circle(
            self.surf,
            color,
            self._apply(pos),
            self._apply(radius),
            width
        )

    def line(self, color, start_pos, end_pos, width=1):
        pygame.draw.line(self.surf, color, self._apply(start_pos), self._apply(end_pos), width)


    def lines(self, color, closed, pointlist, width=1):
        pygame.draw.lines(self.surf, color, closed,
            [tuple(self._apply(p)) for p in pointlist],
            width)

    def polygon(self, color, pointlist, width=0):
        pygame.draw.polygon(self.surf, color,
            [tuple(self._apply(p)) for p in pointlist],
            width
        )


    def rect(self, color, rect, width=0):
        self.polygon(
            color=color,
            pointlist=[
                [rect.left, rect.top],
                [rect.right, rect.top],
                [rect.right, rect.bottom],
                [rect.left, rect.bottom],
            ],
            width=width
        )