import threading
import time

import numpy as np
import cv2

from vision.window import Window


def to_cv(val):
    """ np array to integer tuple """
    try:
        l = len(val)
    except Exception:
        return int(val)
    else:
        return tuple(val.astype(int))

class Mapper(object):
    def __init__(self, odometer, size=500, ppi=10):
        self.odometer = odometer
        self.ppi = ppi
        self.size = size

        t = threading.Thread(target=self._run)
        t.daemon = True
        t.start()

    def redraw(self):
        surf = np.ones((self.size, self.size, 3))
        data = self.odometer.val

        pos = np.array([data.x, -data.y])
        dir = np.array([np.cos(data.theta), -np.sin(data.theta)])

        draw_pos = (self.ppi * pos + self.size/2)
        cv2.line(surf,
            to_cv(draw_pos),
            to_cv(draw_pos + self.ppi * 10*dir),
            (0,0,0)
        )
        cv2.circle(surf, to_cv(draw_pos), to_cv(self.ppi * 8), (0,0,0))

        self.window.show(surf)
        cv2.waitKey(1)

    def _run(self):
        self.window = Window('Map')
        while True:
            self.odometer.update()
            time.sleep(0.05)
            self.redraw()

