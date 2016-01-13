import warnings
from collections import namedtuple

import numpy as np
import cv2
import scipy.ndimage
import scipy.signal

import util
import constants

from .colors import Colors

class Thresholder(object):
    """ Threshold object, representing a plane """
    def __init__(self, normal, d):
        normal = np.array(normal) / np.linalg.norm(normal)
        self.normal = normal
        self.d = d

    def apply(self, frame):
        return np.dot(frame, self.normal) > self.d


thresh_red   = Thresholder([1, -0.65,  -0.65], 16)
thresh_green = Thresholder([-0.9, 1, -0.3], 4)
thresh_blue  = Thresholder([-0.3, -0.9, 1], 8)
thresh_black = Thresholder([-1, -1, -1], -130)

class ColorDetectResult(object):
    def __init__(self, frame):
        im = Colors.WHITE * np.ones(frame.shape[:2], dtype=np.uint8)

        is_red = thresh_red.apply(frame)
        is_green = thresh_green.apply(frame)
        is_blue = thresh_blue.apply(frame)
        is_black = thresh_black.apply(frame)

        # priority order here
        im[is_black] = Colors.BLACK
        im[is_green] = Colors.GREEN
        im[is_blue] = Colors.BLUE
        im[is_red] = Colors.RED
        self.im = im

    @property
    def debug_frame(self):
        return Colors.to_rgb(self.im)


Blob = namedtuple('Blob', 'pos color area')

class BlobDetector(object):
    def __init__(self, color_detect_result):
        im = color_detect_result.im
        labelled, n_regions = scipy.ndimage.measurements.label(im)

        self.labelled = labelled
        self.n_regions = n_regions
        self.region_ids = range(n_regions)

        # count pixesl in each region
        self.areas = scipy.ndimage.measurements.sum(
            np.ones(labelled.shape),
            labels=labelled,
            index=self.region_ids
        ).astype(np.uint32)

        # get the color of each region
        self.colors = scipy.ndimage.measurements.labeled_comprehension(
            im,
            labels=labelled,
            index=self.region_ids,
            func=lambda x: x[0],
            out_dtype=np.uint8, default=-1
        )


        ok_blobs = np.flatnonzero(
            ((self.colors == Colors.RED  ) & (self.areas > 20)) |
            ((self.colors == Colors.GREEN) & (self.areas > 20)) |
            ((self.colors == Colors.BLUE ) & (self.areas > 20))
        )
        # ok_blobs = self.region_ids

        coms = scipy.ndimage.measurements.center_of_mass(
            np.ones(labelled.shape),
            labels=labelled,
            index=list(ok_blobs)
        )

        self.blobs = [
            Blob(*x) for x in zip(
                coms,
                self.colors[ok_blobs],
                self.areas[ok_blobs]
            )
        ]

    @property
    def debug_frame(self):
        frame = np.dstack((
            (self.labelled * 15) % 180,
            np.ones(self.labelled.shape) * 128,
            np.ones(self.labelled.shape) * 255
        )).astype(np.uint8)
        print(frame.shape)

        frame = cv2.cvtColor(frame, cv2.COLOR_HLS2BGR)
        return frame



class Camera(object):
    def __init__(self, w, h, id=constants.cameraID, debug=constants.cameraDebug):
        self.device = cv2.VideoCapture(id)
        self.debug = debug

        # Not all resolutions are possible - check it applied
        self.device.set(cv2.CAP_PROP_FRAME_WIDTH, w)
        self.device.set(cv2.CAP_PROP_FRAME_HEIGHT, h)
        self.width = self.device.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.device.get(cv2.CAP_PROP_FRAME_HEIGHT)
        if (w, h) != (self.width, self.height):
            warnings.warn("Cannot use resolution of {}x{}, using {}x{} instead".format(
                w, h, self.width, self.height))

        if self.debug:
            cv2.namedWindow("Raw")

    def close(self):
        self.device.release()

    @property
    def shape(self):
        return self.height, self.width

    def read(self):
        ok, frame = self.device.read()
        if not ok:
            raise IOError('No frame')

        if self.debug:
            cv2.imshow("Raw", frame)
        return frame[...,::-1]


    def getColorGroups(self):
        frame = self.read()

        colorGroups = {}
        for color in constants.planes:
            colorGroups[color] = np.ones(frame.shape)
            for plane in constants.planes[color]:
                colorGroups[color] = colorGroups[color] and util.threshold(plane, frame)

        return colorGroups

    def getBlobs(self, colorGroups):
        pass