"""
Hardware Access Layer
"""

class HardwareDevice:
    """a device needing a connection through the arduino"""
    def __init__(obj, conn):
        self._conn = conn


class Drive(HardwareDevice):
    def go(self, *, fwd, steer=0):
        """both arguments measured in [-1 1], steer is CCW"""
        pass

    def stop(self):
        self.go(fwd=0)


class Arm(HardwareDevice):
    def up(self):
        pass

    def down(self):
        pass


class Arms:
    def __init__(self, conn):
        self.green = Arm(conn)
        self.red = Arm(conn)


class Robot:
    def __init__(self, conn):
        self.arms = Arms(conn)
        self.drive = Drive(conn)
