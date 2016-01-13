import cv2

class Window(object):
    def __init__(self, name):
        self.name = name

        cv2.namedWindow(self.name)
        cv2.setMouseCallback(self.name, self._on_mouse)

    def _on_mouse(self, event, x, y, flags, param):
        pass

    def show(self, im):
        """show an rgb image"""
        cv2.imshow(self.name, im[...,::-1])

    def close(self):
        cv2.destroyWindow(self.name)
