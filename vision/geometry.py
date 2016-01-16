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

        return super(Geometry, cls).__new__(cls, w, h, np.radians(wfov), np.radians(hfov), matrix)

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

    def projection_on(self, ray, normal, d):
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

    # below is a WIP



    @property
    def projection_matrix(self):
        # project a 3d point onto the image plane at unit distance with centered origin
        camera_to_plane = np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 0, 1]
        ])


        plane_w = 2*np.tan(self.wfov/2)
        plane_h = 2*np.tan(self.hfov/2)

        # project from centered origin to bottom left origin in [0,1]^2
        plane_to_planerel = np.array([
            [1/plane_w, 0, 0.5],
            [0, 1/plane_h, 0.5],
            [0, 0, 1]
        ])

        # convert to pixel coordinates
        planerel_to_pixel = np.array([
            [self.w, 0, 0],
            [0, self.h, 0],
            [0, 0, 1]
        ])

        return planerel_to_pixel * plane_to_planerel

    @property
    def other_matrix(self):
        """
        the matrix such that m * [px py 1] = [x y z 0]

        Uses homogenous coordinates
        """
        tw = np.tan(self.wfov/2)
        th = np.tan(self.hfov/2)
        return np.array([
            [2*tw/self.w, 0, -tw],
            [0, 2*th/self.h, -th],
            [0, 0, 1],
        ])


    @property
    def projection_matr(self):
        """
        the matrix such that m * [px py 1] = [x y z 0]

        Uses homogenous coordinates
        """
        tw = np.tan(self.wfov/2)
        th = np.tan(self.hfov/2)
        return np.array([
            [2*tw/self.w, 0, -tw],
            [0, 2*th/self.h, -th],
            [0, 0, 1],
            [0, 0, 0]
        ])
