import warnings

import cv2
import numpy as np

import constants
import util
from .geometry import Geometry

class Camera(object):
    def __init__(self, w=None, h=None, geom=None, id=constants.cameraID, debug=constants.cameraDebug):
        # deal with simple arguments
        if h is not None and w is not None:
            geom = Geometry(w, h)

        if geom is None:
            raise ValueError("Either w and h or geom must be specified")

        self.device = cv2.VideoCapture(id)
        self.debug = debug

        # Not all resolutions are possible - check it applied
        self.device.set(cv2.CAP_PROP_FRAME_WIDTH, geom.w)
        self.device.set(cv2.CAP_PROP_FRAME_HEIGHT, geom.h)
        w = self.device.get(cv2.CAP_PROP_FRAME_WIDTH)
        h = self.device.get(cv2.CAP_PROP_FRAME_HEIGHT)
        if w == 0 or h == 0:
            raise IOError('Camera initialization resulted in 0x0 resolution')

        # correct for unsupported resolutions
        if (geom.w, geom.h) != (w, h):
            warnings.warn("Cannot use resolution of {}x{}, using {}x{} instead".format(
                geom.w, geom.h, w, h))
            geom.w = w
            geom.h = h

        if self.debug:
            cv2.namedWindow("Raw")

        self.geom = geom

    def close(self):
        self.device.release()

    @property
    def shape(self):
        """ The same value as self.read().shape, for prealloacting frames """
        return self.geom.h, self.geom.w

    def read(self):
        """ return the RGB frame, or raise an exception if it could not be found """
        ok, frame = self.device.read()
        if not ok:
            raise IOError('No frame')

        if self.debug:
            cv2.imshow("Raw", frame)
        return frame[...,::-1]

