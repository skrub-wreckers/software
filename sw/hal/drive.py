import math
import threading
import time
import warnings

import numpy as np
from tamproxy.devices import Motor, Encoder, Odometer, Gyro

from . import HardwareDevice
from .. import pins
from .. import constants
from .. import util

class Drive(HardwareDevice):
    def __init__(self, tamp):
        self.lMotor = Motor(tamp, pins.l_motor_dir, pins.l_motor_pwm)
        self.lMotor.write(1,0)
        self.rMotor = Motor(tamp, pins.r_motor_dir, pins.r_motor_pwm)
        self.rMotor.write(1,0)

        self.r_enc = Encoder(tamp, pins.r_encoder_a, pins.r_encoder_b, continuous=False)
        self.l_enc = Encoder(tamp, pins.l_encoder_a, pins.l_encoder_b, continuous=False)

        self.odometer = Odometer(
            tamp,
            self.l_enc,
            self.r_enc,
            Gyro(tamp, pins.gyro_cs, integrate=False),
            constants.odometer_alpha
        )

    def _set_speeds(self, left, right):
        if np.isnan(left) or np.isnan(right):
            left = right = 0
            warnings.warn("tried to use nan as a velocity!")

        self.lMotor.write(left>0, util.clamp(abs(255 * left), 0, 255))
        self.rMotor.write(right>0, util.clamp(abs(255 * right), 0, 255))


    def go(self, throttle=0, steer=0):
        """both arguments measured in [-1 1], steer=-1 is full speed CW"""
        lPow = rPow = throttle
        lPow -= steer
        rPow += steer
        self._set_speeds(lPow, rPow)

    def turnIP(self, throttle):
        """turn in place arg is in [-1 1] with -1 full speed CW"""
        self.go(0, steer=throttle)

    def stop(self):
        self.go(throttle=0)

    def go_distance(self, dist):
        self.go(throttle= math.copysign(0.2, dist))
        time.sleep(abs(dist) * 0.12)
        self.stop()

    def turn_angle(self, angle):
        self.go(steer=math.copysign(0.2, angle))
        time.sleep(abs(angle) / (math.pi*2)*4.45)
        self.stop()

