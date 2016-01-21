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
        self.reset()

    def reset(self):
        self._last_err = 0
        self._last_time = None
        self._integral = 0
        self._last_derror = 0

    @property
    def error(self):
        return self._last_err

    @property
    def derror(self):
        return self._last_derror


    def at_goal(self, err_t, derr_t=None):
        ok = abs(self.error) < err_t
        if derr_t is not None:
            ok = ok and abs(self.derror) < derr_t
        return ok



    def iterate(self, val, dval=None):
        this_time = time.time()

        # P
        err = self.setpoint - val

        # I
        if self._last_time is not None:
            self._integral += err*(this_time - self._last_time)

        # D
        if dval is not None:
            # TODO: include d/dt(setpoint)?
            derr = -dval
        elif self._last_time is not None:
            derr = (err - self._last_err)/(this_time - self._last_time)
        else:
            derr = 0

        self._last_time = this_time
        self._last_err = err
        self._last_derror = derr
        return self.kP * err + self.kI * self._integral + self.kD * derr
