import warnings

import numpy as np
import threading

from .geometry import Geometry

class Camera(object):
    def __init__(self, w=None, h=None, geom=None, id=1, debug=False):
        import cv2

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
        self.device.set(cv2.CAP_PROP_BUFFERSIZE, 2)
        w = self.device.get(cv2.CAP_PROP_FRAME_WIDTH)
        h = self.device.get(cv2.CAP_PROP_FRAME_HEIGHT)
        if w == 0 or h == 0:
            raise IOError('Camera initialization resulted in 0x0 resolution')

        # correct for unsupported resolutions
        if (geom.w, geom.h) != (w, h):
            warnings.warn("Cannot use resolution of {}x{}, using {}x{} instead".format(
                geom.w, geom.h, w, h))
            geom = geom._replace(w=w, h=h)

        if self.debug:
            cv2.namedWindow("Raw")

        self.geom = geom
        
        self.frame = None
        self.background_capture = threading.Thread(target=self._capture_frame)
        self.background_capture.daemon = True
        self.background_capture.start()

    def close(self):
        self.device.release()

    @property
    def shape(self):
        """ The same value as self.read().shape, for prealloacting frames """
        return self.geom.h, self.geom.w

    def read(self):
        """ return the RGB frame, or raise an exception if it could not be found """
        if self.frame is None:
            raise IOError('No frame')
        if self.debug:
            cv2.imshow("Raw", self.frame)
        return self.frame[...,::-1]
        
    def _capture_frame(self):
        while True:
            ret, self.frame = self.device.read()

