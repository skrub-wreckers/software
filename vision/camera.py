import warnings

import cv2
import numpy as np

import constants
import util

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
        """ The same value as self.read().shape, for prealloacting frames """
        return self.height, self.width

    def read(self):
        """ return the RGB frame, or raise an exception if it could not be found """
        ok, frame = self.device.read()
        if not ok:
            raise IOError('No frame')

        if self.debug:
            cv2.imshow("Raw", frame)
        return frame[...,::-1]