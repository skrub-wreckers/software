import numpy as np

from .colors import Colors

class Thresholder(object):
    """ Threshold object, representing a plane """
    def __init__(self, normal, d):
        self.normal = np.array(normal) / np.linalg.norm(normal)
        self.d = d

    def apply(self, frame):
        return np.dot(frame, self.normal) > self.d


thresh_red   = Thresholder([1, -0.65,  -0.65], 16)
thresh_green = Thresholder([-0.9, 1, -0.3], 4)
thresh_blue  = Thresholder([-0.3, -0.9, 1], 8)
thresh_black = Thresholder([-1, -1, -1], -130)

class ColorDetectResult(object):
    """
    Processes an image into colored regions
    .im is a 1-channel image, where each pixel is according to the values in
    vision.Colors
    """
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

    def mask_out(self, mask):
        self.im[mask] |= Colors.NONE

    @property
    def debug_frame(self):
        # convert color ids to rgb
        frame = Colors.to_rgb(self.im)
        frame[self.im & Colors.NONE != 0] //= 8
        return frame
