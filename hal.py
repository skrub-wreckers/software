"""
Hardware Access Layer
"""
from constants import *
import tamproxy
from tamproxy.devices import Motor

class HardwareDevice:
	"""a device needing a connection through the arduino"""
	def __init__(obj, tamp):
		pass


class Drive(HardwareDevice):
	def __init__(self, tamp):
		self.lMotor = tamproxy.devices.Motor(tamp, lMotorDirPin, lMotorPWMPin)
		self.lMotor.write(1,0)
		self.rMotor = tamproxy.devices.Motor(tamp, rMotorDirPin, rMotorPWMPin)
		self.rMotor.write(1,0)
		
	def go(self, throttle, steer=0):
		"""both arguments measured in [-1 1], steer=-1 is CW"""
		lPow = rPow = throttle
		lPow -= steer
		rPow += steer
		self.lMotor.write(lPow>0, 255 * (lPow+2)/4)
		self.rMotor.write(rPow>0, 255 * (rPow+2)/4)

	def stop(self):
		self.go(throttle=0)

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
	def __init__(self, tamp):
		self.tamp = tamp
		if not self.tamp.started: self.tamp.start()
		self.arms = Arms(self.tamp)
		self.drive = Drive(self.tamp)
