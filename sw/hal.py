"""
Hardware Access Layer
"""
import time
import math
import threading
import warnings
from collections import namedtuple, deque
import logging

import tamproxy
from tamproxy.devices import *
import numpy as np

from . import util
from . import pins
from . import constants
from .vision import Colors

logger = logging.getLogger('sw.hal')

class HardwareDevice(object):
    """a device needing a connection through the arduino"""
    def __init__(obj, tamp):
        pass


class Drive(HardwareDevice):
    def __init__(self, tamp):
        self.lMotor = Motor(tamp, pins.l_motor_dir, pins.l_motor_pwm)
        self.lMotor.write(1,0)
        self.rMotor = Motor(tamp, pins.r_motor_dir, pins.r_motor_pwm)
        self.rMotor.write(1,0)

        self.r_enc = Encoder(tamp, pins.r_encoder_a, pins.r_encoder_b, continuous=False)
        self.l_enc = Encoder(tamp, pins.l_encoder_a, pins.l_encoder_b, continuous=False)

        
        self.distPID = util.PID(constants.motorDistP, constants.motorDistI, constants.motorDistD)
        self.anglePID = util.PID(constants.motorAngleP, constants.motorAngleI, constants.motorAngleD)
        
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


class RegulatedDrive(Drive):
    MoveOp = namedtuple('MoveOp', 'pos')
    TurnOp = namedtuple('TurnOp', 'angle')

    def __init__(self, tamp):
        super(RegulatedDrive, self).__init__(tamp)

        self._dist_pid = util.PID(constants.motorDistP, constants.motorDistI, constants.motorDistD)
        self._angle_pid = util.PID(constants.motorAngleP, constants.motorAngleI, constants.motorAngleD)


        self.busy_lock = threading.Condition()
        self.op_done = threading.Condition()

        self.op = None

        self.bg_thread = threading.Thread(target=self._background)
        self.bg_thread.daemon = True

        self.bg_thread.start()

    def _background(self):
        while True:
            # get the next operation, threadsafely
            with self.busy_lock:
                while self.op is None:
                    self.busy_lock.wait()
                op = self.op

                if isinstance(op, self.TurnOp):
                    self._background_turn(op.angle)
                elif isinstance(op, self.MoveOp):
                    self._background_move(op.pos)

                with self.op_done:
                    self.op_done.notify_all()
                    self.op = None


    def turn_to(self, angle, fix=True):
        """ turn to the absolute angle specified"""
        if fix:
            angle = self._fix_angle(angle)

        with self.busy_lock:
            self.busy_lock.notify()
            self.op = self.TurnOp(angle)

        with self.op_done:
            self.op_done.wait()

    def _background_turn(self, angle):
        pid = self._angle_pid
        pid.reset()
        pid.setpoint = angle

        while True:
            sensor = self.odometer.val
            steer = pid.iterate(sensor.theta, dval=sensor.omega)
            self.go(steer=util.clamp(steer, -0.4, 0.4))
            time.sleep(0.05)

            if pid.at_goal(err_t=np.radians(2), derr_t=np.radians(5)):
                break

        self.stop()

    def go_to(self, pos):
        """ go in a straight line to pos """
        pos = np.array(pos)

        with self.busy_lock:
            self.busy_lock.notify()
            self.op = self.MoveOp(pos)

        with self.op_done:
            self.op_done.wait()

    def _background_move(self, goal_pos):
        start_reading = self.odometer.val
        start_pos = np.array([start_reading.x, start_reading.y])

        # find the parallel and perpendicular directions
        dir = goal_pos - start_pos
        dir = dir / np.linalg.norm(dir)
        left_dir = np.array([[0, 1], [-1, 0]]).dot(dir)
        if np.isnan(dir).any():
            return

        # choose the angle that results in the least turn from the current angle
        target_angle = self._fix_angle(np.arctan2(dir[1], dir[0]))

        a_pid = self._angle_pid
        d_pid = self._dist_pid

        a_pid.reset()
        d_pid.reset()

        d_pid.setpoint = 0


        # go straight
        while True:
            sensor = self.odometer.val
            curr_pos = np.array([sensor.x, sensor.y])
            facing = np.array([np.cos(sensor.theta), np.sin(sensor.theta)])
            curr_vel = facing * sensor.v

            # error perpendicular to and along line
            perp_err = (curr_pos - goal_pos).dot(left_dir)
            perp_err_dt = curr_vel.dot(left_dir)
            dist_left = (curr_pos - goal_pos).dot(dir)
            dist_left_dt = curr_vel.dot(dir)

            # correct target angle based on position deviation
            # TODO: full PID here
            angle_corr = 0.1*perp_err
            a_pid.setpoint = target_angle + np.clip(angle_corr, np.radians(-30), np.radians(+30))

            steer    = a_pid.iterate(sensor.theta, dval=sensor.omega)
            throttle = d_pid.iterate(dist_left, dval=dist_left_dt) * dir.dot(facing)

            self.go(steer=np.clip(steer, -0.4, 0.4),
                throttle=np.clip(throttle, -0.2, 0.2))
            time.sleep(0.05)

            if d_pid.at_goal(err_t=0.25, derr_t=0.5):
                break

        self.stop()

    def _fix_angle(self, angle):
        """ Adjusts the angle by 2n*pi to make it at most pi from the current angle """
        theta = self.odometer.val.theta
        while angle < theta - np.pi:
            angle += 2*np.pi
        while angle > theta + np.pi:
            angle -= 2*np.pi
        return angle



class Arm(HardwareDevice):
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

class Arms:
    def __init__(self, conn):
        self.green = Arm(conn, pins.l_arm, lower=620, upper=2350)
        self.red = Arm(conn, pins.r_arm, lower=2320, upper=760)

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
        
class Robot:
    def __init__(self, tamp):
        self.tamp = tamp
        if not self.tamp.started: self.tamp.start()
        self.arms = Arms(self.tamp)
        self.drive = Drive(self.tamp)
        self.color_sensor = ColorSensor(self.tamp)
        self.camera = Camera(*constants.cameraResolution)

