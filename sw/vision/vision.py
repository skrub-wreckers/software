import math
from collections import namedtuple

from .camera import Camera
from .colors import Colors
from .blobdetection import BlobDetector
from .thresholding import ColorDetectResult
from .window import Window

import pygame
import numpy as np
import scipy.ndimage as ndimage

class Cube(namedtuple('Cube', 'pos color')):
    @property
    def angle_to(self):
        """ Planar angle """
        return math.atan2(self.pos[1], self.pos[0])

    @property
    def distance(self):
        """ Planar distance """
        return np.linalg.norm(self.pos[:2])

    @property
    def pos2(self):
        return self.pos[:2]

    def __str__(self):
        return "<{} cube at {:.1f}, {:.1f}, {:.1f}>".format(Colors.name(self.color), self.pos[0], self.pos[1], self.pos[2])

class CameraPanel(object):
    def __init__(self, vision, size = 500):
        self.vision = vision
        self.size = size
        self.name = "Camera"
        
    def set_size(self, size):
        self.size = size
        
    def draw(self, surface):
        if self.vision.frame is not None:
            pygame.surfarray.blit_array(surface.subsurface([10, 10, self.vision.frame.shape[1],self.vision.frame.shape[0]]), np.transpose(self.vision.frame,(1,0,2)))
            pygame.surfarray.blit_array(surface.subsurface([10, 250, self.vision.frame.shape[1],self.vision.frame.shape[0]]), np.transpose(self.vision.color_detect.debug_frame,(1,0,2)))
            if self.vision.blobs is not None:
                for blob in self.vision.blobs:
                    pygame.draw.circle(surface, Colors.to_rgb(blob.color), (int(blob.pos[1]+10), int(blob.pos[0]+10)), 5)
        
    def update(self, events):
        pass#self.vision.update()

class Vision(object):
    """Takes an image and returns the angle to blobs"""

    def __init__(self, cam):
        self.cam = cam
        self.ray = None
        self.angle_to = None
        self.frame = None
        #self.debug_win = Window('vision debug')

    def update(self):
        self.frame = self.cam.read()
        self.color_detect = self.filter_blue(ColorDetectResult(self.frame))
        red_blobs = BlobDetector(self.color_detect, Colors.RED, 100).blobs
        green_blobs = BlobDetector(self.color_detect, Colors.GREEN, 100).blobs

        all_blobs = red_blobs + green_blobs

        # TODO:
        #   filter out cubes above the wall
        #   detect cubes in a stack
        #   look at cube area

        cubes = []
        for blob in all_blobs:
            try:
                pos = self.cam.geom.project_on(
                    ray=self.cam.geom.ray_at(blob.pos[1], blob.pos[0]),
                    normal=[0, 0, 1, 0],
                    d=1  # center of the cube is 1in off the ground
                )
            except ValueError:
                # no projection onto the plane
                pass
            else:
                cubes.append(Cube(pos=pos, color=blob.color))
        
        self.blobs = all_blobs
        self.cubes = cubes

        #self.debug_win.show(self.color_detect.debug_frame)

    def filter_blue(self, frame):
        return frame

        # for now
        is_blue = (frame.im == Colors.BLUE)
        is_blue = ndimage.binary_opening(is_blue, structure=np.ones((5,5)))
        is_blue = ndimage.binary_closing(is_blue, structure=np.ones((5,5)))

        x, y = np.meshgrid(np.arange(frame.im.shape[1]), np.arange(frame.im.shape[0]))

        blue_above = np.cumsum(is_blue, axis=0)
        frame.mask_out(blue_above == 0)
        return frame

    def nearest_cube(self, color=None):
        """ get the nearest cube, by cartesian distance, optionally of a specific color """
        filtered = self.cubes
        if color is not None:
            filtered = (c for c in self.cubes if c.color == color)

        try:
            return min(filtered, key=lambda c: c.distance)
        except ValueError:
            return None