import numpy as np
from tamproxy.devices import Odometer as TAMPOdometer
from . import HardwareDevice




class Odometer(HardwareDevice):

    class Reading(TAMPOdometer.Reading):
        @property
        def pos(self):
            return np.array([self.x, self.y])

        @property
        def dir(self):
            return np.array([np.cos(self.theta), np.sin(self.theta)])

        @property
        def vel(self):
            return self.dir * self.v

    def __init__(self, odometer):
        self._dev = odometer

        # Converts odometer reference space into world space
        # this matrix transforms vectors of [x, y, theta, 1]
        self._ref_to_world = np.eye(4)

    @property
    def val(self):
        """ transform the`val based on our matrix """
        reading = self._dev.val
        res = np.dot(self._ref_to_world, np.array([reading.x, reading.y, reading.theta, 1]))
        return self.Reading._make(reading)._replace(x=res[0], y=res[1], theta=res[2])

    def override_position(self, x, y, theta):
        """
        Tell the robot that its current position is actually a different value.
        All future readings will be measured consistent to this position

        Note that this happens entirely python-side, so that we don't end up
        a issue with non-atomic read-modify-write operations. 
        """
        # transform from pose-relative to world
        pose_to_world = np.array([
            [ np.cos(theta), -np.sin(theta), 0,     x],
            [ np.sin(theta),  np.cos(theta), 0,     y],
            [             0,              0, 1, theta],
            [             0,              0, 0,     1]
        ])

        data = self._dev.val
        robot_to_ref = np.array([
            [ np.cos(data.theta), -np.sin(data.theta), 0, data.x    ],
            [ np.sin(data.theta),  np.cos(data.theta), 0, data.y    ],
            [                   0,                  0, 1, data.theta],
            [                   0,                  0, 0,          1]
        ])

        # we require that ref_to_world @ robot_to_ref = pose_to_world
        # so                             ref_to_world = pose_to_world @ inv(robot_to_ref)

        self._ref_to_world = np.dot(pose_to_world, np.linalg.inv(robot_to_ref))

    @property
    def robot_matrix(self):
        """ returns a matrix that multiplies 2D robot space to world space """
        data = self.val

        return np.array([
            [ np.cos(data.theta), np.sin(data.theta), data.x],
            [-np.sin(data.theta), np.cos(data.theta), data.y],
            [                  0,                  0,      1]
        ])

    @property
    def robot_matrix3(self):
        """ returns a matrix that multiplies 3D robot space to world space """
        res = np.eye(4)
        i = np.array([0,1,3]).reshape(1, -1)
        res[i.T,i] = self.robot_matrix
        return res


