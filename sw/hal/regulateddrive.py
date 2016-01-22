import warnings
from collections import namedtuple
import threading
import time

import numpy as np

from . import Drive
from .. import constants
from .. import util

class RegulatedDrive(Drive):
    """
    A controlled version of the drive that uses the odometer
    """
    def __init__(self, tamp):
        super(RegulatedDrive, self).__init__(tamp)

        self._dist_pid = util.PID(constants.motorDistP, constants.motorDistI, constants.motorDistD)
        self._angle_pid = util.PID(constants.motorAngleP, constants.motorAngleI, constants.motorAngleD)

        # contains the current operation. Setting this is locked through
        # busy_lock. Upon completion, this is cleared locked on op_done.
        self.op = None
        self.busy_lock = threading.Condition()
        self.op_done = threading.Condition()

        # kick off the background thread
        self.bg_thread = threading.Thread(target=self._background)
        self.bg_thread.daemon = True
        self.bg_thread.start()

    # types for queuing commands
    MoveOp = namedtuple('MoveOp', 'pos')
    TurnOp = namedtuple('TurnOp', 'angle')

    def _background(self):
        """ run in the background """
        while True:
            # lock on busy_lock to prevent the main thread from changing the
            # command without it being looked at
            with self.busy_lock:
                # get the next operation when notified by the main thread
                while self.op is None:
                    self.busy_lock.wait()
                op = self.op

                # delegate to the appropriate control method
                if isinstance(op, self.TurnOp):
                    self._background_turn(op.angle)
                elif isinstance(op, self.MoveOp):
                    self._background_move(op.pos)

                # notify the main thread that we finished the command
                with self.op_done:
                    self.op_done.notify_all()
                    self.op = None

    def turn_to(self, angle, fix=True):
        """
        Turn to the absolute angle specified

        When fix is True, ensure the robot does not rotate more than 180.
        Set to false when enforcing a specific direction, ie:

            turn_to(odometer.angle + pi*1.5)
        """
        if fix:
            angle = self._fix_angle(angle)

        # wait until the background thread is ready
        with self.busy_lock:
            self.busy_lock.notify()
            self.op = self.TurnOp(angle)

        # wait until the background thread is done
        with self.op_done:
            self.op_done.wait()

    def _background_turn(self, angle):
        """ called in the background after turn_to """
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

        # wait until the background thread is ready
        with self.busy_lock:
            self.busy_lock.notify()
            self.op = self.MoveOp(pos)

        # wait until the background thread is done
        with self.op_done:
            self.op_done.wait()

    def _background_move(self, goal_pos):
        """ called in the background after go_to """
        # read the odometer
        start_reading = self.odometer.val
        start_pos = start_reading.pos

        # find the parallel and perpendicular directions
        dir = goal_pos - start_pos
        dir = dir / np.linalg.norm(dir)
        left_dir = np.array([[0, 1], [-1, 0]]).dot(dir)
        if np.isnan(dir).any():
            return

        # choose the angle that results in the least turn from the current angle
        target_angle = self._fix_angle(np.arctan2(dir[1], dir[0]))

        # clear the state in the pid controllers
        a_pid = self._angle_pid
        d_pid = self._dist_pid
        a_pid.reset()
        d_pid.reset()

        # d_pid is given the distance to go, since it's not 1D
        d_pid.setpoint = 0

        while True:
            # promote sensor data to vectors
            sensor = self.odometer.val
            curr_pos = sensor.pos
            facing = sensor.dir
            curr_vel = sensor.vel

            # find error perpendicular to and along line
            perp_err = (curr_pos - goal_pos).dot(left_dir)
            perp_err_dt = curr_vel.dot(left_dir)
            dist_left = (curr_pos - goal_pos).dot(dir)
            dist_left_dt = curr_vel.dot(dir)

            # choose throttle based on forward error, and scale based on direction
            throttle = d_pid.iterate(dist_left, dval=dist_left_dt) * dir.dot(facing)

            # choose target angle based on transverse error
            # TODO: full PID here
            angle_corr = 0.1*perp_err
            a_pid.setpoint = target_angle + np.clip(angle_corr, np.radians(-30), np.radians(+30))

            # choose steer based on target angle
            steer = a_pid.iterate(sensor.theta, dval=sensor.omega)

            # control the motors
            self.go(
                throttle=np.clip(throttle, -0.2, 0.2),
                steer=np.clip(steer, -0.4, 0.4)
            )
            time.sleep(0.05)

            # ignore transverse distance when terminating, since it's hard to get right
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
