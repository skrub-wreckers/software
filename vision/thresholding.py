import numpy as np

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
