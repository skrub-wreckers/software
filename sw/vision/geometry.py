from __future__ import division
from collections import namedtuple

import numpy as np

class lazy_property(object):
    '''
    meant to be used for lazy evaluation of an object attribute.
    property should represent non-mutable data, as it replaces itself.
    '''

    def __init__(self,fget):
        self.fget = fget
        self.func_name = fget.__name__

    def __get__(self,obj,cls):
        if obj is None:
            return None
        value = self.fget(obj)
        setattr(obj,self.func_name,value)
        return value


_Geometry = namedtuple('_Geometry', 'w h wfov hfov matrix')

class Geometry(_Geometry):
    def __new__(cls, w, h, wfov=None, hfov=None, matrix=np.eye(4)):
        """
        w:      image width in pixels
        h:      image height in pixels
        wfov:   horizontal field of view in radians
        hfov:   vertical field of view in radians
        matrix: transformation from camera to world coordinates
        """
        if not (w > 0 and h > 0):
            raise ValueError('Size must be positive')

        if not matrix.shape == (4, 4):
            raise ValueError('Matrix should be a homogeneous 4x4')

        return super(Geometry, cls).__new__(cls, w, h, wfov, hfov, matrix)

    def ray_at(self, x, y):
        """
        Returns the direction in world space, with components
        [forward, left, up], corresponding to a given pixel in the image.
        Uses homogeneous coordinates
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

        if t < 0:
            raise ValueError("Ray does not hit plane")

        return origin + ray*t

    @lazy_property
    def projection_matrix(self):
        """
        Returns a 3x4 matrix that transforms a point in space into pixel coordinates
        Uses homogeneous coordinates:

            res = g.projection_matrix.dot(pixel)
            res = res / res[-1]
        """
        # project a 3d point onto the image plane at unit distance with centered origin
        camera_to_plane = np.array([
            [0, -1, 0, 0],
            [0, 0, -1, 0],
            [1, 0, 0, 0]
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

        # XA = B => X = BA^-1 = solve(A.T, B.T).T
        return np.linalg.solve(
            self.matrix.T,
            planerel_to_pixel
                .dot(plane_to_planerel)
                .dot(camera_to_plane).T
        ).T

    def on_screen(self, point):
        """ return true if the homogeneous pixel coordinate is on_screen """
        p = point / point[-1]
        return  point[-1] > 0 and 0 <= p[0] <= self.w and 0 <= p[1] <= self.h