import time
import threading

from tamproxy.devices import Servo
from . import HardwareDevice
from .. import pins

class Arm(HardwareDevice):
    """
    A loose wrapper of a servo device, that deals with the up and down
    trajectories we need
    """
    def __init__(self, tamp, servo_pin, lower, upper):
        self.servo = Servo(tamp, servo_pin, lower, upper)
        self.servo.write(0)

    def up(self):
        for angle in range(0, 40, 4):
            self.servo.write(angle)
            time.sleep(0.1)

        self.servo.write(180)

    def down(self):
        self.servo.write(0)


class Arms(HardwareDevice):
    def __init__(self, tamp):
        self.green = Arm(tamp, pins.l_arm, lower=620, upper=2350)
        self.red = Arm(tamp, pins.r_arm, lower=2320, upper=760)