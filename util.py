from __future__ import print_function
import time

def clamp(value, min, max):
	if value < min: 
		return min
	elif value > max:
		return max
	else:
		return value

class Timer(object):
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

	def iterate(self, val):
		err = self.setpoint - val
		self.integral += err*(time.time()-self.last_time)
        self.last_time = time.time()
		derivative = (err - self.prevErr)
		self.prevErr = err
		return self.kP * err + self.kI * self.integral + self.kD * derivative