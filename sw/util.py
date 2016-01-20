from __future__ import print_function
import time

def clamp(value, min, max):
    if value < min: 
        return min
    elif value > max:
        return max
    else:
        return value
class Profiler(object):
    def __init__(self, name, indent=''):
        self.name = name
        self.indent = indent
        self.has_children = False

    def __enter__(self):
        self.t = time.time()
        print(self.indent +'Timing {}... '.format(self.name), end='')
        return self

    def __exit__(self, *args):
        if self.has_children:
            print()
            print(self.indent + '  ' + str(time.time() - self.t))
        else:
            print(str(time.time() - self.t))

    def __call__(self, name):
        print()
        self.has_children = True
        return Timer(name, self.indent + '  ')

class PID(object):
    def __init__(self, kP, kI, kD, setpoint=0):
        self.kP = kP
        self.kI = kI
        self.kD = kD
        self.setpoint = setpoint
        self._last_time = None

    @property
    def setpoint(self):
        return self._setpoint

    @setpoint.setter
    def setpoint(self, value):
        self._setpoint = value
        self._last_err = 0
        self._integral = 0

    def iterate(self, val, dVal = None):
        err = self.setpoint - val
        this_time = time.time()
        self._integral += err*(this_time - self._last_time)
        if dVal is None:
            derivative = (err - self._last_err)/(this_time - self._last_time)
        else:
            derivative = -dVal
        self._last_time = this_time
        self._last_err = err
        return self.kP * err + self.kI * self.integral + self.kD * derivative
