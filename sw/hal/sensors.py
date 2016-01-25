import time
import numpy as np

from tamproxy.devices import Color, DigitalInput

from . import HardwareDevice
from .. import constants
from ..vision import Colors

class _PatchedDigitalInput(DigitalInput):
    def __init__(self, *args, **kwargs):
        self.on_update = kwargs.pop('on_update')
        super(_PatchedDigitalInput, self).__init__(*args, **kwargs)

    def _handle_update(self, *args, **kwargs):
        super(_PatchedDigitalInput, self)._handle_update(*args, **kwargs)
        self.on_update()


class DigitalIR(HardwareDevice):
    ON_TIME = 0.2

    def __init__(self, tamp, pin):
        self._dev = _PatchedDigitalInput(tamp, pin, on_update=self._on_update)
        self.val = False
        self._last_time = None

    def _on_update(self):
        curr_time = time.time()

        # no reading
        if self._dev.val:
            self.val = False
            self._last_time = None

        # rising edge
        elif self._last_time is None:
            self._last_time = curr_time

        # high for long enough
        elif curr_time - self._last_time > self.ON_TIME:
            self.val = True


class ColorSensor(HardwareDevice):

    # parameters found using SVD in color-sensor/analyze.py
    ORIGIN = np.array([91.03845978,   80.88461304,   67.92308044,  229.65383911])
    WEIGHTS = np.array([
        [ 0.001995  ,  0.00139472,  0.00108591,  0.00418362],
        [ 0.00385208, -0.00279219, -0.00128208, -0.00057327]
    ])

    def __init__(self, tamp):
        self._dev = Color(tamp, integrationTime=Color.INTEGRATION_TIME_2_4MS, gain=Color.GAIN_60X)

    @property
    def val(self):
        raw = np.array([self._dev.r, self._dev.g, self._dev.b, self._dev.c])

        projected = (raw - self.ORIGIN).dot(self.WEIGHTS.T)

        if projected[0] < 0.1:
            return Colors.NONE
        elif projected[1] > 0:
            return Colors.RED
        else:
            return Colors.GREEN
