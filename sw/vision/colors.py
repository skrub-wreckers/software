import numpy as np

class Colors(object):
    """Codes used to represent colors"""
    BLACK = 0
    RED = 1
    GREEN = 2
    BLUE = 4
    WHITE = 7
    NONE = 8

    @staticmethod
    def to_rgb(color):
        return (np.stack((
            color & Colors.RED,
            color & Colors.GREEN,
            color & Colors.BLUE,
        ), axis=-1) != 0) * np.uint8(255)

    @staticmethod
    def name(color):
        if color == Colors.RED:   return "red"
        if color == Colors.GREEN: return "green"

