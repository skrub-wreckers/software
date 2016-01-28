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

class CubeStack(namedtuple('CubeStack', 'pos colors')):
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

    @property
    def color(self):
        """ deprecated """
        return self.colors[0]

    @property
    def height(self):
        return len(self.colors)


    def __str__(self):
        if len(self.colors) > 1:
            return "<{} stack at {:.1f}, {:.1f}, {:.1f}>".format(
                ','.join(Colors.name(c) for c in self.colors), self.pos[0], self.pos[1], self.pos[2])
        else:
            return "<{} cube at {:.1f}, {:.1f}, {:.1f}>".format(
                Colors.name(self.color), self.pos[0], self.pos[1], self.pos[2])

# deprecated
Cube = CubeStack

class CameraPanel(object):
    def __init__(self, vision, size = 500):
        self.vision = vision
        self.size = size
        self.name = "Camera"
        # self.vision.update()

    def set_size(self, size):
        self.size = size

    def draw(self, surface):
        surface.fill((50,50,50))
        if self.vision.frame is not None:
            pygame.surfarray.blit_array(
                surface.subsurface([10, 10, self.vision.frame.shape[1],self.vision.frame.shape[0]]),
                np.transpose(self.vision.frame,(1,0,2)))
            pygame.surfarray.blit_array(
                surface.subsurface([10, 250, self.vision.frame.shape[1],self.vision.frame.shape[0]]),
                np.transpose(self.vision.color_detect.debug_frame,(1,0,2)))
            if self.vision.blobs is not None:
                for blob in self.vision.blobs:
                    pygame.draw.circle(surface, Colors.to_rgb(blob.color), (int(blob.pos[1]+10), int(blob.pos[0]+10)), 5)

    def update(self, events):
        self.vision.update()

class Vision(object):
    """Takes an image and returns the angle to blobs"""

    def __init__(self, cam):
        self.cam = cam
        self.ray = None
        self.angle_to = None
        self.frame = None

        # import this now, rather than losing time during something important
        # but not at global scope either, because then all our programs wait for it
        import scipy.ndimage

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

        rays_by_blob = {
            blob: self.cam.geom.ray_at(blob.pos[1], blob.pos[0])
            for blob in all_blobs
        }

        stacks = []

        def update_stacks(blob, ray):
            for i in [2, 1, 0]:
                h = 1+2*i  # height off ground
                try:
                    pos = self.cam.geom.project_on(ray=ray, normal=[0, 0, 1, 0], d=h)
                except ValueError:
                    # no projection onto the plane
                    continue

                for stack in stacks:
                    if stack.height == i and np.linalg.norm(pos[:2] - stack.pos[:2]) < 2:
                        stack.colors.append(blob.color)
                        return
                else:
                    if i == 0:
                        stacks.append(CubeStack(pos=pos, colors=[blob.color]))

        # Iterate over rays, starting from those pointing msot down
        for blob, ray in sorted(rays_by_blob.items(), key=lambda (r, b): r[2]):
            update_stacks(blob, ray)


        self.blobs = all_blobs
        self.cubes = stacks

        #self.debug_win.show(self.color_detect.debug_frame)

    def filter_blue(self, frame):
        import scipy.ndimage as ndimage

        # for now
        structure = np.ones((5,5))
        is_blue = (frame.im == Colors.BLUE)
        is_blue = ndimage.binary_erosion(is_blue, structure, border_value=1)
        is_blue = ndimage.binary_dilation(is_blue, structure, border_value=0)
        is_blue = ndimage.binary_dilation(is_blue, structure, border_value=0)
        is_blue = ndimage.binary_erosion(is_blue, structure, border_value=1)

        x, y = np.meshgrid(np.arange(frame.im.shape[1]), np.arange(frame.im.shape[0]))

        # find all pixels with no blue pixels below them
        blue_below = np.cumsum(is_blue[::-1], axis=0)[::-1]
        frame.mask_out((blue_below > 0) & ~is_blue)

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