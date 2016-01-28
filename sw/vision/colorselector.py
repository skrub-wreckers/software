import os.path

import cv2
import numpy as np

from .window import Window

_edge_kernel = np.array([
    [0, 1, 0],
    [1, 0, 1],
    [0, 1, 0]
])

def _highlight_region(frame, mask, color):
    """ adds a colored border around a mask in an image """
    import scipy.signal

    color = np.array(color)
    bmask = mask.astype(np.bool)


    border = bmask & (scipy.signal.convolve2d(mask, _edge_kernel, mode='same') != 4)
    mod = np.copy(frame)
    mod[bmask, :] = mod[bmask, :] * 0.5 + color * 0.25 + 0.25
    mod[border,:] = color
    return mod


class ColorData(object):
    def __init__(self, name, ui_bgr, shape):
        self.ui_bgr = np.array(ui_bgr)
        self.name = name
        self.cv_mask = np.zeros(shape, np.uint8)
        self.matches = []

    @property
    def mask(self):
        return self.cv_mask.astype(np.bool)


class ColorSelector(Window):
    """
    A ui for labelling colors of a camera stream manually, and recording all
    colors that occur at the labelled locations
    """
    def __init__(self, shape, name='Color selection'):
        super(ColorSelector, self).__init__(name)

        self.colors = [
            ColorData('red',   [255, 0, 0], shape),
            ColorData('green', [0, 255, 0], shape),
            ColorData('yellow', [255, 255, 0], shape),
            ColorData('blue',  [0, 0, 255], shape),
            ColorData('black',  [32, 32, 32], shape),
            ColorData('white',  [192, 192, 192], shape)
        ]

        self.i = 0

        self._active_cmd = None

    def next_color(self):
        self.i = (self.i + 1) % len(self.colors)

    @property
    def active_color(self):
        return self.colors[self.i]


    def _on_mouse(self, event, x, y, flags, param):
        """ clear the current color on right drag, set it on left drag """
        mask = self.colors[self.i].cv_mask

        if event == cv2.EVENT_LBUTTONDOWN:
            self._active_cmd = 'set'
        elif event == cv2.EVENT_RBUTTONDOWN:
            self._active_cmd = 'right'

        elif event == cv2.EVENT_MOUSEMOVE:
            if self._active_cmd != None:
                cv2.circle(mask, (x,y), 5, 1 if self._active_cmd == 'set' else 0, -1)

        elif event == cv2.EVENT_LBUTTONUP:
            cv2.circle(mask, (x,y), 5, 1 if self._active_cmd == 'set' else 0, -1)
            self._active_cmd = None

        elif event == cv2.EVENT_RBUTTONUP:
            cv2.circle(mask, (x,y), 5, 1 if self._active_cmd == 'set' else 0, -1)
            self._active_cmd = None

    def show(self, frame):
        mod = frame
        for color in self.colors:
            mod = _highlight_region(mod, color.mask, color.ui_bgr)

        super(ColorSelector, self).show(mod)

    def record(self, frame):
        for c in self.colors:
            c.matches.append(frame[c.mask,:])

    def save(self, path='.'):
        if not os.path.exists(path):
            os.mkdir(path)
        for c in self.colors:
            all_data = np.concatenate(c.matches)
            if len(all_data) > 0:
                np.save(os.path.join(path, c.name), all_data)

    def clear(self):
        for c in self.colors:
            c.matches = []

