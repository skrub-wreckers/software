from collections import namedtuple

import numpy as np

_Geometry = namedtuple('_Geometry', 'w h wfov hfov matrix')

class Geometry(_Geometry):
    def __new__(cls, w, h, wfov=None, hfov=None, matrix=np.eye(4)):
        """
        w:      image width in pixels
        h:      image height in pixels
        wfov:   horizonal field of view in degrees
        hfov:   vertical field of view in degrees
        matrix: transformation from camera to world coordinates
        """
        if not (w > 0 and h > 0):
            raise ValueError('Size must be positive')

        if not matrix.shape == (4, 4):
            raise ValueError('Matrix should be a homogenous 4x4')

        return super(Geometry, cls).__new__(cls, w, h, wfov, hfov, matrix)

    def ray_at(self, x, y):
        """
        Returns the direction in world space, with components
        [forward, left, up], corresponding to a given pixel in the image.
        Uses homogenous coordinates
        """
        if self.wfov is None or self.hfov is None:
            raise ValueError('FOV not specified')

        # convert to [-1 1]
        xrel = 2*x/self.w - 1
        yrel = 2*y/self.h - 1

        return self.matrix.dot(np.array([
            1,
            -xrel * np.tan(self.wfov / 2),
            -yrel * np.tan(self.hfov / 2),
            0
        ]))

    def project_on(self, ray, normal, d):
        """
        Project the ray extending from (x,y) onto the plane of the equation
        dot(v, normal) = d

        Where v = c_origin + t*ray
        """
        normal = np.array(normal) / np.linalg.norm(normal)

        # camera origin in world coordinates
        origin = self.matrix.dot(np.array([0, 0, 0, 1]))

        ray /= np.linalg.norm(ray)

        t = (d - np.dot(origin, normal)) / (np.dot(ray, normal))

        return origin + ray*t
