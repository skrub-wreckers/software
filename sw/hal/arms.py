import time
import threading
import itertools

from tamproxy.devices import Servo
from . import HardwareDevice
from .. import pins

class Arm(HardwareDevice):
    """
    A loose wrapper of a servo device, that deals with the up and down
    trajectories we need
    """
    def __init__(self, tamp, servo_pin, lower, upper, up_traj, down_traj):
        """
        lower:     servo us corresponding to 0 angle
        upper:     servo us corresponding to 180 angle
        up_traj:   list of (angle, dt) tuples for up trajectory
        down_traj: list of (angle, dt) tuples for down trajectory
        """
        self.servo = Servo(tamp, servo_pin, lower, upper)
        self.servo.write(0)

        self.up_traj = up_traj
        self.down_traj = down_traj

    def up(self):
        for angle, dt in self.up_traj:
            self.servo.write(angle)
            time.sleep(dt)

    def down(self):
        for angle, dt in self.down_traj:
            self.servo.write(angle)
            time.sleep(dt)


class Arms(HardwareDevice):
    def __init__(self, tamp):
        self.silo = Arm(tamp, pins.l_arm,
            lower=598,
            upper=2350,
            up_traj=zip(range(0, 40, 2), itertools.repeat(0.1)) + [(180, 1)],
            down_traj=[(0, 1)]
        )
        self.dump = Arm(tamp, pins.r_arm,
            lower=2350,
            upper=760,
            up_traj=zip(range(0, 40, 2), itertools.repeat(0.1)) + [(180, 1)],
            down_traj=[(0, 0.75)]
        )

        self.silo_door = Servo(tamp, pins.stack_door, 1550, 700)
        self.silo_door.write(0)
