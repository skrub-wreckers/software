import time

from tamproxy.devices import AnalogInput
from tamproxy.devices import DigitalOutput

from . import HardwareDevice
from .. import constants
from ..vision import Colors

class ColorSensor(HardwareDevice):
    # Strobes LED
    # Determines color by range of values during one strobe
    def __init__(self, tamp):
        self.photo_resistor = AnalogInput(tamp, pins.photo_resistor)
        self.led = DigitalOutput(tamp, pins.led)

    def read(self):
        self.led.write(True)
        self.photo_resistor.update()
        vMin = self.photo_resistor.val
        
        time.sleep(1)

        self.led.write(False)
        self.photo_resistor.update()
        vMax = self.photo_resistor.val

        vDiff = vMax - vMin

        if vDiff > 0:
            if abs(vDiff - constants.nothingRange) < constants.colorRangeTolerance:
                return Colors.NONE
            elif abs(vDiff - constants.greenRange) < constants.colorRangeTolerance:
                return Colors.GREEN
            elif abs(vDiff - constants.redRange) < constants.colorRangeTolerance:
                return Colors.RED
            else:
                return Colors.AMBIGUOUS
        else:
            return Colors.AMBIGUOUS

        time.sleep(1)
