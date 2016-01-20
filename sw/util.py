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

class PID:
    def __init__(self, kP, kI, kD, setpoint=0):
        self.kP = kP
        self.kI = kI
        self.kD = kD
        self.setSetpoint(setpoint)
        self.last_time = time.time()

    def setSetpoint(self, setpoint):
        self.setpoint = setpoint
        self.prevErr = 0
        self.integral = 0

    def iterate(self, val, dVal = None):
        err = self.setpoint - val
        self.integral += err*(time.time()-self.last_time)
        if dVal is None:
            derivative = (err - self.prevErr)/(time.time()-self.last_time)
        else:
            derivative = -dVal
        self.last_time = time.time()
        self.prevErr = err
        return self.kP * err + self.kI * self.integral + self.kD * derivative
