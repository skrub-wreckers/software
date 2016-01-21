from tamproxy.devices import AnalogInput

from . import HardwareDevice
from .. import constants
from ..vision import Colors

class ColorSensor(HardwareDevice):
    def __init__(self, tamp):
        self.photo_resistor = AnalogInput(tamp, pins.photo_resistor)

    def read(self):
        self.photo_resistor.update()
        v = self.photo_resistor.val
        if v > constants.nothing_cutoff:
            return Colors.NONE
        elif v > constants.green_cutoff:
            return Colors.GREEN
        else:
            return Colors.RED
